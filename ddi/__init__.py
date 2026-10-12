"""DDI skill: DSN-DDI 예측을 위한 함수 모음 (환경 ①에서 import).

    resolve_drug(x)                  약물 이름·동의어·DrugBank ID·SMILES -> 표준 약물 정보
    predict(a, b, top_k=3)           상위 관계, 관계별 확률, 방향이 반영된 문장, 경고
    predict_many(pairs, relation=None, top_k=3)
                                     여러 쌍을 한 번에 예측, relation(번호 또는 목록)으로 거름
    explain(rel, a, b)               DSN-DDI 관계 번호 -> 방향이 반영된 문장
    save_results(results, path)      채점용 CSV 저장 (drug_a, drug_b, relation, prob, model_used, description)

확률은 관계마다 따로 계산한 값(sigmoid)이라 86개의 합이 1이 아니다.
예측은 모델의 추정이며 기록된 사실이 아니다.
"""
from .drugs import resolve_drug
from .prediction import predict, predict_many
from .relations import explain
from .results import save_results

__all__ = ['resolve_drug', 'predict', 'predict_many', 'explain', 'save_results']

for _f in (resolve_drug, predict, predict_many, explain, save_results):
    _f.__module__ = __name__  # help()·채점 확인에서 예전처럼 ddi.<함수>로 보이게
del _f
