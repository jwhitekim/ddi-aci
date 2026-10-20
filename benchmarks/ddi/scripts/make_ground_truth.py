"""질문마다 두 순서의 정답(원 DSN-DDI 모델 출력)을 계산 (eval_spec.md 3장).

예측 서버 코드를 쓰지 않고 원 저장소 코드로 쌍 하나씩(배치 크기 1) 계산한다.
ddi-runtime 컨테이너(GPU)의 /opt/DSN-DDI 에서 실행:

    docker run --rm --gpus all -v $PWD/benchmarks/ddi:/w/bench -v $PWD/ddi-tools/server:/w/server:ro ddi-runtime \
        python /w/bench/scripts/make_ground_truth.py

출력: benchmarks/ddi/data/questions/questions.jsonl. --check-server 를 주면 예측 서버 값과 비교한다.
"""
import csv
import json
import sys

import pandas as pd
import torch
from torch_geometric.data import Batch, Data

sys.path.insert(0, 'drugbank_test')
import data_preprocessing as dp  # noqa: E402
import models  # noqa: E402,F401

DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'
TOP_K = 5

_train = pd.read_csv('drugbank_test/drugbank/fold0/train.csv')
TRAIN_DRUGS = set(_train['d1']) | set(_train['d2'])
MODELS = {n: torch.load('drugbank_test/%s_drugbank.pkl' % n, map_location=DEVICE).eval()
          for n in ('transductive', 'inductive')}
with open('Interaction_information.csv', encoding='utf-8') as f:
    RELATIONS = {int(r['Interaction type']): (r['Description'], int(r['Subject'])) for r in csv.DictReader(f)}
with open('drugbank_vocabulary.csv', encoding='utf-8') as f:
    NAMES = {r['DrugBank ID']: r['Common name'].strip() for r in csv.DictReader(f)}


def graph(drug):
    ei, x = dp.MOL_EDGE_LIST_FEAT_MTX[drug]
    if ei.numel() == 0:
        ei = torch.empty((2, 0), dtype=torch.long)
    return dp.drug_to_mol_graph[drug], ei, x


def probs(d1, d2):
    model_name = 'transductive' if d1 in TRAIN_DRUGS and d2 in TRAIN_DRUGS else 'inductive'
    mh, eh, xh = graph(d1)
    mt, et, xt = graph(d2)
    h = Data(x=xh.clone(), edge_index=eh)
    t = Data(x=xt.clone(), edge_index=et)
    b = dp.BipartiteData(dp.get_bipartite_graph(mh, mt), h.x, t.x)
    tri = [Batch.from_data_list([h]), Batch.from_data_list([t]),
           torch.LongTensor(list(range(86))).unsqueeze(0), Batch.from_data_list([b])]
    with torch.no_grad():
        p = torch.sigmoid(MODELS[model_name]([x.to(DEVICE) for x in tri])).cpu().tolist()
    return model_name, p


def sentence(rel, a, b):
    template, subject = RELATIONS[rel + 1]
    d1, d2 = (b, a) if subject == 2 else (a, b)
    return template.replace('#Drug1', NAMES[d1]).replace('#Drug2', NAMES[d2]), d1, d2


def answer(a, b):
    model_name, p = probs(a, b)
    ranked = sorted(range(86), key=lambda r: p[r], reverse=True)
    top = []
    for r in ranked[:TOP_K]:
        text, d1, d2 = sentence(r, a, b)
        top.append({'relation': r, 'prob': p[r], 'description': text, 'drug1': d1, 'drug2': d2})
    return {'model': model_name, 'top': top, 'probs': p}


def main():
    rows = [json.loads(l) for l in open('/w/bench/data/questions/questions_base.jsonl', encoding='utf-8')]
    with open('/w/bench/data/questions/questions.jsonl', 'w', encoding='utf-8') as out:
        for q in rows:
            a, b = q['drugs']
            q['ground_truth'] = {'%s|%s' % (a, b): answer(a, b), '%s|%s' % (b, a): answer(b, a)}
            out.write(json.dumps(q, ensure_ascii=False) + '\n')
            g = q['ground_truth']
            print(q['qid'], 'label', q['label'], '| A,B top', g['%s|%s' % (a, b)]['top'][0]['relation'],
                  '| B,A top', g['%s|%s' % (b, a)]['top'][0]['relation'])
    if '--check-server' in sys.argv:
        sys.path.insert(0, '/w/server')
        import predictor  # 검증용으로만 사용
        worst = 0.0
        for q in rows:
            for key, gt in q['ground_truth'].items():
                d1, d2 = key.split('|')
                sp = predictor.score_pair(d1, d2)['probs']
                worst = max(worst, max(abs(sp[r] - gt['probs'][r]) for r in range(86)))
        print('max |ground truth - server| = %.2e' % worst)
        assert worst <= 1e-4


if __name__ == '__main__':
    main()
