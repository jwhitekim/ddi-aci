"""예측: 한 쌍(predict), 여러 쌍(predict_many)."""
from .drugs import _key, _payload, resolve_drug
from .relations import explain
from .client import _post


def predict(a, b, top_k=3):
    """두 약물의 상위 관계를 예측한다.

    반환: {'drug_a', 'drug_b', 'model_used', 'top': [{'relation', 'prob', 'description'}], 'warnings'}
    """
    da, db = resolve_drug(a), resolve_drug(b)
    res = _post('/predict', {'d1': _payload(da), 'd2': _payload(db), 'top_k': int(top_k)})
    warnings = []
    for drug, info in ((da, res['d1']), (db, res['d2'])):
        drug['in_train'] = info['in_train']
        if info['is_new']:
            warnings.append('%s은(는) 신약(SMILES 입력)이라 inductive 모델로 예측했습니다. 신뢰도가 낮을 수 있습니다.'
                            % drug['smiles'])
        elif not info['in_train']:
            warnings.append('%s(%s)은(는) 학습셋에 없는 약물이라 inductive 모델로 예측했습니다. 신뢰도가 낮을 수 있습니다.'
                            % (drug['name'], drug['drugbank_id']))
        if info['unknown_atoms']:
            warnings.append('%s에 모델이 모르는 원소(%s)가 있어 원자 특징이 Unknown으로 처리됐습니다. 예측을 신뢰하기 어렵습니다.'
                            % (drug['name'] if drug['drugbank_id'] else drug['smiles'], ', '.join(info['unknown_atoms'])))
    top = [{'relation': t['relation'], 'prob': t['prob'],
            'description': explain(t['relation'], da['name'], db['name'])} for t in res['top']]
    return {'drug_a': da, 'drug_b': db, 'model_used': res['model_used'], 'top': top, 'warnings': warnings}


def predict_many(pairs, relation=None, top_k=3):
    """여러 쌍을 예측해 쌍마다 한 행씩 돌려준다 (pandas 가 있으면 DataFrame).

    relation 에 관계 번호(하나 또는 목록)를 주면, 상위 top_k 안에 그 관계가 있는 쌍만 남기고
    그 행의 relation/prob/description 은 일치한 관계 중 확률이 가장 높은 것으로 채운다.
    식별이나 예측에 실패한 쌍은 error 칸에 이유를 적어 남긴다.
    """
    wanted = None if relation is None else {int(r) for r in (relation if isinstance(relation, (list, tuple, set)) else [relation])}
    rows = []
    for a, b in pairs:
        try:
            res = predict(a, b, top_k)
        except (ValueError, RuntimeError) as e:
            rows.append({'drug_a': str(a), 'drug_b': str(b), 'name_a': str(a), 'name_b': str(b),
                         'relation': None, 'prob': None, 'model_used': None, 'description': None,
                         'top_relations': None, 'warnings': '', 'error': str(e)})
            continue
        hits = [t for t in res['top'] if wanted is None or t['relation'] in wanted]
        if not hits:
            continue
        best = hits[0]
        rows.append({'drug_a': _key(res['drug_a']), 'drug_b': _key(res['drug_b']),
                     'name_a': res['drug_a']['name'], 'name_b': res['drug_b']['name'],
                     'relation': best['relation'], 'prob': best['prob'], 'model_used': res['model_used'],
                     'description': best['description'],
                     'top_relations': [(t['relation'], round(t['prob'], 4)) for t in res['top']],
                     'warnings': ' '.join(res['warnings']), 'error': ''})
    try:
        import pandas as pd
        return pd.DataFrame(rows)
    except ImportError:
        return rows
