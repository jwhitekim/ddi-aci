"""A·B·C 답변을 문항별로 나란히 비교하는 문서를 만든다 (Zero-shot Planner Figure 1 방식).

    python3 eval/scripts/make_comparison.py

입력: eval/questions/questions.jsonl, eval/baseline_a/a_answers.jsonl·a_claims.jsonl,
      eval/results/v2/{B,C}/q*.json, runs/eval/{B,C}/q*/trajectory.json
출력: eval/ANSWER_COMPARISON.md
"""
import csv
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EVAL = REPO / 'eval'
SHOW = 'q04'  # 대표 사례 (B가 방향을 틀린 문항)

with open(REPO / 'ddi' / 'data' / 'Interaction_information.csv', encoding='utf-8') as f:
    TEMPLATES = {int(r['Interaction type']): r['Description'] for r in csv.DictReader(f)}
with open(REPO / 'ddi' / 'data' / 'dbvocab.csv', encoding='utf-8') as f:
    NAMES = {r['DrugBank ID']: r['Common name'].strip() for r in csv.DictReader(f)}


def jsonl(path):
    return [json.loads(l) for l in open(path, encoding='utf-8')]


def sentence(t, d1, d2):
    return TEMPLATES[t].replace('#Drug1', NAMES.get(d1, d1)).replace('#Drug2', NAMES.get(d2, d2))


def final_answer(cond, qid):
    """에이전트가 마지막에 사용자에게 한 말 (finish의 최종 메시지, 없으면 마지막 메시지)."""
    ev = json.load(open(REPO / 'runs' / 'eval' / cond / qid / 'trajectory.json'))
    for e in reversed(ev):
        if e.get('source') != 'agent':
            continue
        if e.get('action') == 'finish' and e.get('args', {}).get('final_thought'):
            return e['args']['final_thought'].strip()
        if e.get('action') == 'message' and e.get('message'):
            return e['message'].strip()
    return '(최종 메시지 없음)'


def agent_row(cond, q):
    """질문 순서 방향의 대표 결과 문장과 판정."""
    r = json.load(open(EVAL / 'results' / 'v2' / cond / ('%s.json' % q['qid'])))
    order = '%s|%s' % tuple(q['drugs'])
    claims = [c for c in r['claims'] if c['checks']['order'] == order]
    desc = claims[0]['description'] if claims else '(질문 순서 결과 없음)'
    return desc, r['result'] == 'success', r['causes']


def a_row(q, item):
    claims = item['graders']['gemini-3.5-flash']
    sents = [sentence(t, d1, d2) for t, d1, d2 in claims]
    r = json.load(open(EVAL / 'results' / 'v2' / 'A' / ('%s.json' % q['qid'])))
    return ('; '.join(sents) if sents else '(86개 관계 중 해당하는 주장 없음)'), r['result'] == 'success'


def mark(ok):
    return '✅' if ok else '❌'


def main():
    qs = jsonl(EVAL / 'questions' / 'questions.jsonl')
    a_ans = {x['qid']: x['answer'] for x in jsonl(EVAL / 'baseline_a' / 'a_answers.jsonl')}
    a_claims = {x['qid']: x for x in jsonl(EVAL / 'baseline_a' / 'a_claims.jsonl')}
    rows = []
    for q in qs:
        a, b = q['drugs']
        gt = q['ground_truth']['%s|%s' % (a, b)]['top'][0]
        ad, aok = a_row(q, a_claims[q['qid']])
        bd, bok, bc = agent_row('B', q)
        cd, cok, _ = agent_row('C', q)
        rows.append(dict(q=q, gt=gt, a=(ad, aok), b=(bd, bok, bc), c=(cd, cok)))

    out = ['# A·B·C 답변 비교 (v2, 10문항)', '',
           '같은 질문을 세 조건에 주고, 각 조건이 최종적으로 내놓은 답을 원 DSN-DDI 모델의 예측(정답)과 나란히 비교한다. '
           '채점 기준은 `eval_spec.md` 0장, 수치는 `eval/RESULTS.md`. 이 문서는 `eval/scripts/make_comparison.py`로 만든다.', '',
           '- **과제:** 질문 → (A) LLM이 지식으로 답함 / (B·C) 에이전트가 DSN-DDI 모델을 실행하고 그 예측을 보고 답함',
           '- **정답:** 원 DSN-DDI 모델이 질문 순서의 약물 쌍에 대해 낸 1위 관계 문장',
           '- **비교 대상:** A는 답에서 채점기(Gemini 3.5 Flash)가 뽑은 주장, B·C는 결과 파일에 적은 질문 순서 방향의 문장', '']

    # 1. 대표 사례
    r = next(x for x in rows if x['q']['qid'] == SHOW)
    q = r['q']
    out += ['## 1. 대표 사례: %s — %s' % (q['qid'], q['question']), '',
            '| | 결과 문장 | 판정 |', '| --- | --- | --- |',
            '| **정답 (DSN-DDI 1위, 관계 %d)** | %s | |' % (r['gt']['relation'], r['gt']['description']),
            '| **A (LLM 단독)** | %s | %s |' % (r['a'][0], mark(r['a'][1])),
            '| **B (ACI 없음)** | %s | %s %s |' % (r['b'][0], mark(r['b'][1]), ', '.join(r['b'][2])),
            '| **C (DDI-ACI)** | %s | %s |' % (r['c'][0], mark(r['c'][1])), '']
    for label, text in (('A의 답 (앞부분)', a_ans[q['qid']][:1200].rstrip() + ' …'),
                        ('B의 최종 답변', final_answer('B', q['qid'])),
                        ('C의 최종 답변', final_answer('C', q['qid']))):
        out += ['**%s**' % label, '', '> ' + text.replace('\n', '\n> '), '']

    # 2. 전체 10문항
    out += ['## 2. 전체 10문항', '',
            '| 문항 | 질문 | 정답 (DSN-DDI 1위) | A | B | C |', '| --- | --- | --- | --- | --- | --- |']
    for r in rows:
        q = r['q']
        out.append('| %s | %s | %s | %s %s | %s %s | %s %s |' % (
            q['qid'], q['question'], r['gt']['description'],
            mark(r['a'][1]), r['a'][0], mark(r['b'][1]), r['b'][0], mark(r['c'][1]), r['c'][0]))
    n = len(rows)
    out += ['| **성공** | | | **%d/%d** | **%d/%d** | **%d/%d** |' % (
        sum(r['a'][1] for r in rows), n, sum(r['b'][1] for r in rows), n, sum(r['c'][1] for r in rows), n), '']

    # 3. 문항별 최종 답변 전문
    out += ['## 3. 문항별 최종 답변 전문', '']
    for r in rows:
        q = r['q']
        out += ['<details><summary>%s — %s</summary>' % (q['qid'], q['question']), '',
                '**정답:** %s' % r['gt']['description'], '',
                '**A의 답**', '', a_ans[q['qid']].strip(), '',
                '**B의 최종 답변**', '', final_answer('B', q['qid']), '',
                '**C의 최종 답변**', '', final_answer('C', q['qid']), '', '</details>', '']
    (EVAL / 'ANSWER_COMPARISON.md').write_text('\n'.join(out), encoding='utf-8')
    print('wrote', EVAL / 'ANSWER_COMPARISON.md')


if __name__ == '__main__':
    main()
