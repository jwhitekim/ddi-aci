"""A 조건(LLM 단독): 도구 없이 질문만 보내고, 답에서 효과·방향 주장을 채점기 모델 두 개로 뽑는다.

    .venv-openhands/bin/python eval/run_baseline_a.py

출력: eval/a_answers.jsonl (답), eval/a_claims.jsonl (채점기 추출 결과, 불일치는 needs_human)
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

import litellm
from dotenv import load_dotenv

REPO = Path(__file__).resolve().parent.parent
load_dotenv(REPO / '.env')
sys.path.insert(0, str(REPO / 'eval'))
from score import resolve  # noqa: E402

ANSWER_MODEL = dict(model='openai/anthropic/claude-sonnet-5.5', base_url='https://ai-gateway.vercel.sh/v1',
                    api_key=os.environ.get('AI_GATEWAY_API_KEY'))
GRADERS = {
    'sonnet-5.5': ANSWER_MODEL,
    'gemini-3.5-flash': dict(model='gemini/gemini-3.5-flash', api_key=os.environ.get('GEMINI_API_KEY')),
}

with open(REPO / 'ddi' / 'data' / 'Interaction_information.csv', encoding='utf-8') as f:
    TEMPLATES = {int(r['Interaction type']): r['Description'] for r in csv.DictReader(f)}

GRADER_PROMPT = """Below is an answer about the interaction between two drugs: {a} and {b}.
Map every interaction the answer asserts between these two drugs to one of the numbered templates.
For each, give the template number and which drug fills #Drug1 and which fills #Drug2.
Only include interactions the answer actually states. If it states none, return an empty list.

Templates:
{templates}

Answer:
\"\"\"{answer}\"\"\"

Reply with JSON only: {{"claims": [{{"T": <number>, "drug1": "<drug name>", "drug2": "<drug name>"}}]}}"""


def complete(cfg, prompt, max_tokens=4000):
    r = litellm.completion(messages=[{'role': 'user', 'content': prompt}], temperature=0.0, max_tokens=max_tokens, **cfg)
    return r.choices[0].message.content or ''


def extract(cfg, q, answer):
    templates = '\n'.join('%d: %s' % (t, d) for t, d in sorted(TEMPLATES.items()))
    text = complete(cfg, GRADER_PROMPT.format(a=q['names'][0], b=q['names'][1], templates=templates, answer=answer))
    m = re.search(r'\{.*\}', text, re.S)
    claims = []
    for c in (json.loads(m.group(0)).get('claims', []) if m else []):
        d1, d2 = resolve(c.get('drug1'), q['drugs']), resolve(c.get('drug2'), q['drugs'])
        if d1 and d2 and d1 != d2 and int(c.get('T', 0)) in TEMPLATES:
            claims.append((int(c['T']), d1, d2))
    return sorted(set(claims))


def main():
    questions = [json.loads(l) for l in open(REPO / 'eval' / 'questions.jsonl', encoding='utf-8')]
    ans_path, claims_path = REPO / 'eval' / 'a_answers.jsonl', REPO / 'eval' / 'a_claims.jsonl'
    answers = {}
    if ans_path.exists():
        answers = {json.loads(l)['qid']: json.loads(l) for l in open(ans_path, encoding='utf-8')}
    with open(ans_path, 'a', encoding='utf-8') as f:
        for q in questions:
            if q['qid'] in answers:
                continue
            answers[q['qid']] = {'qid': q['qid'], 'question': q['question'], 'answer': complete(ANSWER_MODEL, q['question'])}
            f.write(json.dumps(answers[q['qid']], ensure_ascii=False) + '\n')
            print('A answered', q['qid'], flush=True)
    with open(claims_path, 'w', encoding='utf-8') as f:
        for q in questions:
            answer = answers[q['qid']]['answer']
            per = {name: extract(cfg, q, answer) for name, cfg in GRADERS.items()}
            vals = list(per.values())
            agreed = vals[0] == vals[1]
            adopted = vals[0] if agreed else []
            f.write(json.dumps({'qid': q['qid'], 'answer': answer, 'graders': per, 'needs_human': not agreed,
                                'claims': [{'T': t, 'drug1': a, 'drug2': b} for t, a, b in adopted]},
                               ensure_ascii=False) + '\n')
            print('A graded', q['qid'], 'agreed' if agreed else 'NEEDS HUMAN', per, flush=True)


if __name__ == '__main__':
    main()
