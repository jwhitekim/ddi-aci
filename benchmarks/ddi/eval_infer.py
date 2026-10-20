"""평가 채점기 (eval_spec.md 4·5장). A·B·C 모두 같은 기준.

    python3 benchmarks/ddi/eval_infer.py  # 공개 원자료 results/v2/raw/{A,B,C} 채점 (A 는 A/a_claims.jsonl) → results/v2/
    python3 benchmarks/ddi/eval_infer.py --runs-dir eval_outputs/ddi --out eval_outputs/ddi/scores   # 새 실행 채점
    python3 benchmarks/ddi/eval_infer.py --questions benchmarks/ddi/data/questions/smoke_question.jsonl --run X=eval_outputs/scratch/sonnet_B30   # 임의 실행 채점

정규화: 약물 이름 -> DrugBank ID, 문장 -> (관계 종류 T, #Drug1, #Drug2).
판정(eval_spec.md 0장, v2): 질문 순서(데이터 저장 순서) 한 방향만 본다.
성공 = 그 방향의 결과 문장이 ② 모델 1위와 같은 효과이고 ③ 약물 방향도 맞음. 반대 순서는 보지 않음.
① relation 번호가 모델 1위와 같은지는 참고 지표(relation_match)로 따로 적는다.
"""
import argparse
import csv
import glob
import json
import re
from pathlib import Path

BENCH = Path(__file__).resolve().parent
REPO = BENCH.parents[1]
DATA = REPO / 'ddi-tools' / 'ddi' / 'data'
ID_RE = re.compile(r'^DB\d{5}$', re.I)


def load_vocab():
    by_name = {}
    with open(DATA / 'dbvocab.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            for n in [r['Common name']] + (r['Synonyms'] or '').split(' | '):
                if n.strip():
                    by_name.setdefault(n.strip().lower(), set()).add(r['DrugBank ID'])
    return by_name


def load_templates():
    out = {}
    with open(DATA / 'Interaction_information.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            t = int(r['Interaction type'])
            pat = re.escape(normalize(r['Description']))
            for tag in ('Drug1', 'Drug2'):
                esc = re.escape('#' + tag.lower())
                pat = pat.replace(esc, '(?P<%s>.+?)' % tag.lower(), 1).replace(esc, '(?P=%s)' % tag.lower())
            out[t] = re.compile('^' + pat + '$', re.I)
    return out


def normalize(text):
    text = ' '.join(str(text).replace(' ', ' ').split()).strip().rstrip('.').strip()
    return text.lower()


VOCAB = load_vocab()
TEMPLATES = load_templates()


def resolve(name, qdrugs):
    """이름/ID -> 질문의 약물 ID (질문 약물로 좁힘). 못 찾으면 None."""
    s = str(name or '').strip().strip('"\'').strip()
    if ID_RE.match(s):
        return s.upper() if s.upper() in qdrugs else None
    s = re.sub(r'\s*\(.*?\)\s*', ' ', s).strip()
    ids = VOCAB.get(s.lower(), set()) & set(qdrugs)
    return next(iter(ids)) if len(ids) == 1 else None


def parse_sentence(desc, qdrugs):
    """문장 -> (T, drug1, drug2). 질문의 두 약물로 해석되는 가장 긴 틀을 고른다."""
    text = normalize(desc)
    best = None
    for t, rx in TEMPLATES.items():
        m = rx.match(text)
        if not m:
            continue
        d1, d2 = resolve(m.group('drug1'), qdrugs), resolve(m.group('drug2'), qdrugs)
        if d1 and d2 and d1 != d2:
            if best is None or len(rx.pattern) > len(TEMPLATES[best[0]].pattern):
                best = (t, d1, d2)
    return best


def to_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def to_int(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None


def claims_from_csv(run_dir, qdrugs):
    """결과 CSV -> 방향별 대표 행(확률이 가장 높은 행)의 주장 목록."""
    rows = []
    for path in sorted(glob.glob(str(Path(run_dir) / 'results' / '*.csv'))):
        with open(path, encoding='utf-8', errors='replace') as f:
            rows += list(csv.DictReader(f))
    best = {}
    for r in rows:
        a, b = resolve(r.get('drug_a'), qdrugs), resolve(r.get('drug_b'), qdrugs)
        parsed = parse_sentence(r.get('description', ''), qdrugs)
        order = '%s|%s' % (a, b) if a and b and a != b else None
        key = order or ('?', len(best))
        prob = to_float(r.get('prob'))
        cand = {'order': order, 'relation': to_int(r.get('relation')), 'prob': prob,
                'model_used': r.get('model_used', ''), 'parsed': parsed, 'description': r.get('description', '')}
        if key not in best or (prob or -1) > (best[key]['prob'] or -1):
            best[key] = cand
    return rows, list(best.values())


def judge(claim, q):
    """주장 하나를 판정. 반환: (맞은 방향 key 또는 None, 원인 목록, ①②③)."""
    gt_all = q['ground_truth']
    parsed = claim.get('parsed')
    orders = [claim['order']] if claim.get('order') in gt_all else list(gt_all)  # 순서를 모르면 의미로 두 순서 모두 대조
    causes = []
    best_checks = None
    for order in orders:
        top = gt_all[order]['top'][0]
        c1 = claim.get('relation') == top['relation'] if claim.get('relation') is not None else None
        c2 = parsed is not None and parsed[0] == top['relation'] + 1
        c3 = parsed is not None and (parsed[1], parsed[2]) == (top['drug1'], top['drug2'])
        checks = {'order': order, 'model_top_relation': c1, 'effect': c2, 'direction': c3}
        if c2 and c3:
            return order, [], checks
        if best_checks is None or (c2, c1) > (best_checks['effect'], best_checks['model_top_relation']):
            best_checks = checks
    # 오답 원인
    order = best_checks['order']
    top = gt_all[order]['top'][0]
    rel = claim.get('relation')
    if parsed is None:
        causes.append('해석 불가')
    if 'induct' in str(claim.get('model_used', '')).lower() and gt_all[order]['model'] == 'transductive':
        causes.append('모델 선택 오류')
    if rel is not None and parsed is not None and rel == top['relation'] and parsed[0] == rel:
        causes.append('번호→문장 대응 오류(한 칸 밀림)')
    if parsed is not None and parsed[0] == top['relation'] + 1 and (parsed[1], parsed[2]) != (top['drug1'], top['drug2']):
        causes.append('방향 오류')
    if parsed is not None and parsed[0] - 1 == q['label'] and top['relation'] != q['label']:
        causes.append('기록 베끼기 의심')
    if not causes:
        causes.append('기타 오답')
    return None, causes, best_checks


def score_question(q, claims, has_output):
    if not has_output:
        return {'qid': q['qid'], 'result': 'fail', 'relation_match': None, 'causes': ['실행 실패'], 'claims': []}
    if not claims:
        return {'qid': q['qid'], 'result': 'fail', 'relation_match': None,
                'causes': ['약물 식별 실패 또는 해석 불가'], 'claims': []}
    judged = []
    for c in claims:
        ok, causes, checks = judge(c, q)
        gt = q['ground_truth'].get(checks['order'])
        note = []
        if ok and c.get('relation') is not None and c.get('prob') is not None:
            if abs(c['prob'] - gt['probs'][c['relation']]) > 1e-3:
                note.append('배치 섞임(확률 차이)')
        judged.append({**{k: c.get(k) for k in ('order', 'relation', 'prob', 'model_used', 'description')},
                       'parsed': c.get('parsed'), 'checks': checks, 'correct': bool(ok), 'causes': causes, 'notes': note})
    # 질문 순서 방향의 주장만 본다 (반대 순서는 보지 않음)
    primary = [j for j in judged if j['checks']['order'] == '%s|%s' % tuple(q['drugs'])]
    success = any(j['correct'] for j in primary)
    causes = [] if success else (sorted({c for j in primary for c in j['causes']}) or ['질문 순서 결과 없음'])
    rel = [j['checks']['model_top_relation'] for j in primary if j['checks']['model_top_relation'] is not None]
    return {'qid': q['qid'], 'result': 'success' if success else 'fail', 'relation_match': any(rel) if rel else None,
            'causes': causes, 'claims': judged}


def efficiency(run_dir):
    p = Path(run_dir) / 'run_info.json'
    if not p.exists():
        return {}
    d = json.loads(p.read_text())
    t = d.get('tokens') or {}
    return {'turns': d.get('turns'), 'seconds': d.get('seconds'), 'status': d.get('status'),
            'prompt_tokens': t.get('prompt_tokens'), 'cache_read_tokens': t.get('cache_read_tokens'),
            'completion_tokens': t.get('completion_tokens')}


def summarize(name, results):
    n = len(results)
    rel = [r['relation_match'] for r in results if r['relation_match'] is not None]
    causes = {}
    for r in results:
        for c in r['causes']:
            causes[c] = causes.get(c, 0) + 1
    eff = [r.get('efficiency', {}) for r in results]

    def avg(k):
        v = [e[k] for e in eff if e.get(k) is not None]
        return round(sum(v) / len(v), 1) if v else None
    return {
        'condition': name, 'n': n,
        'success_rate': sum(r['result'] == 'success' for r in results) / n if n else 0,
        'valid_execution_rate': sum('실행 실패' not in r['causes'] for r in results) / n if n else 0,
        'relation_match_rate': (sum(rel) / len(rel)) if rel else None,
        'failure_causes': causes,
        'avg_turns': avg('turns'), 'avg_seconds': avg('seconds'),
        'avg_prompt_tokens': avg('prompt_tokens'), 'avg_completion_tokens': avg('completion_tokens'),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--questions', default=str(BENCH / 'data' / 'questions' / 'questions.jsonl'))
    p.add_argument('--run', action='append', default=[], help='이름=실행폴더 (한 문항 질문 파일과 함께 사용)')
    p.add_argument('--runs-dir', default=str(REPO / 'results' / 'v2' / 'raw'), help='조건별 실행 폴더(<조건>/<qid>/)가 있는 곳')
    p.add_argument('--out', default=str(REPO / 'results' / 'v2'))
    args = p.parse_args()
    questions = [json.loads(l) for l in open(args.questions, encoding='utf-8')]
    out = Path(args.out)
    summaries = []

    if args.run:  # 임의 실행 채점 (스모크 검증용)
        q = questions[0]
        for spec in args.run:
            name, run_dir = spec.split('=', 1)
            rows, claims = claims_from_csv(run_dir, q['drugs'])
            r = score_question(q, claims, bool(rows))
            print(json.dumps({'run': name, 'result': r['result'], 'causes': r['causes'],
                              'claims': [(c['order'], c['relation'], c['parsed'], c['checks'], c['causes']) for c in r['claims']]},
                             ensure_ascii=False))
        return

    for cond in ('B', 'C'):
        results = []
        for q in questions:
            run_dir = Path(args.runs_dir) / cond / q['qid']
            if not run_dir.exists():
                continue
            rows, claims = claims_from_csv(run_dir, q['drugs'])
            r = score_question(q, claims, bool(rows))
            r['efficiency'] = efficiency(run_dir)
            results.append(r)
        if results:
            (out / cond).mkdir(parents=True, exist_ok=True)
            for r in results:
                (out / cond / ('%s.json' % r['qid'])).write_text(json.dumps(r, ensure_ascii=False, indent=2))
            summaries.append(summarize(cond, results))

    a_path = Path(args.runs_dir) / 'A' / 'a_claims.jsonl'
    if a_path.exists():
        results = []
        by_q = {json.loads(l)['qid']: json.loads(l) for l in open(a_path, encoding='utf-8')}
        for q in questions:
            if q['qid'] not in by_q:
                continue
            item = by_q[q['qid']]
            claims = [{'order': None, 'relation': None, 'prob': None, 'model_used': '', 'description': c.get('text', ''),
                       'parsed': (c['T'], c['drug1'], c['drug2'])} for c in item.get('claims', [])]
            r = score_question(q, claims, bool(item.get('answer')))
            r['graders_agree'] = item.get('graders_agree')
            results.append(r)
        (out / 'A').mkdir(parents=True, exist_ok=True)
        for r in results:
            (out / 'A' / ('%s.json' % r['qid'])).write_text(json.dumps(r, ensure_ascii=False, indent=2))
        summaries.append(summarize('A', results))

    out.mkdir(parents=True, exist_ok=True)
    (out / 'summary.json').write_text(json.dumps(summaries, ensure_ascii=False, indent=2))
    for s in summaries:
        print(json.dumps(s, ensure_ascii=False))


if __name__ == '__main__':
    main()
