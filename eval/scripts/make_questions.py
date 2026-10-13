"""평가 질문 10문항 생성 (eval_spec.md 2장). ddi-runtime 컨테이너의 /opt/DSN-DDI 에서 실행:

    docker run --rm -v $PWD/eval:/w/eval -v $PWD/agent:/w/agent:ro ddi-runtime python /w/eval/scripts/make_questions.py

출력: eval/questions/questions_base.jsonl (정답 없이 질문만)
"""
import csv
import json
import random

SEED = 42
N_QUESTIONS = 10
TEMPLATE = '{a}이랑 {b} 상호작용 예측해줘'


def load_pairs(path):
    with open(path) as f:
        return [(r['d1'], r['d2'], int(r['type'])) for r in csv.DictReader(f)]


def main():
    train = load_pairs('drugbank_test/drugbank/fold0/train.csv')
    test = load_pairs('drugbank_test/drugbank/fold0/test.csv')
    train_drugs = {d for a, b, _ in train for d in (a, b)}
    with open('drugbank_vocabulary.csv', encoding='utf-8') as f:
        names = {r['DrugBank ID']: r['Common name'].strip() for r in csv.DictReader(f)}

    by_rel = {}
    for a, b, r in test:
        if a in train_drugs and b in train_drugs and a in names and b in names:
            by_rel.setdefault(r, []).append((a, b))

    rng = random.Random(SEED)
    relations = rng.sample(sorted(by_rel), N_QUESTIONS)  # 서로 다른 관계 10개
    suffix = open('/w/agent/task_suffix.txt', encoding='utf-8').read()
    with open('/w/eval/questions/questions_base.jsonl', 'w', encoding='utf-8') as out:
        for i, rel in enumerate(relations, 1):
            a, b = rng.choice(sorted(by_rel[rel]))
            question = TEMPLATE.format(a=names[a], b=names[b])  # 데이터 저장 순서대로
            out.write(json.dumps({
                'qid': 'q%02d' % i,
                'question': question,
                'question_with_suffix': question + suffix,
                'drugs': [a, b],
                'names': [names[a], names[b]],
                'label': rel,
            }, ensure_ascii=False) + '\n')
            print('q%02d' % i, rel, question)


if __name__ == '__main__':
    main()
