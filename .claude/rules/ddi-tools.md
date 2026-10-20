---
paths:
  - "ddi-tools/**"
  - "tests/tools/**"
---

# ddi 도구와 예측 서버 규칙

이 규칙이 ACI 의 핵심이다. 바꾸면 조건 C 결과가 달라진다.

## 관계 번호 → 문장 (`explain`)
- DSN-DDI 관계 `t`(0~85)는 설명 파일(`Interaction_information.csv`)의 `Interaction type == t + 1` 행에 대응한다. `DDI type N` 칸은 쓰지 않는다.
- 그 행의 `Subject == 2`(86종 중 42종)이면 #Drug1 에 b, #Drug2 에 a 를 넣는다. 1 또는 3 이면 a, b 순서 그대로.

## 예측 서버 (`ddi-tools/server/`)
- 쌍 하나씩(배치 크기 1) 계산한다. 여러 쌍을 한 배치로 묶으면 이분 그래프 `GATConv` 가 쌍 사이 원자를 연결해 예측이 달라진다. 같은 쌍의 응답은 다른 요청과 상관없이 항상 같아야 한다.
- 결합이 없는 약물(원자 1개)도 예측할 수 있어야 한다.
- 시작할 때 transductive·inductive 가중치를 모두 GPU 에 올리고, 컨테이너 안 127.0.0.1 에서만 받는다.
- 두 약물이 모두 `drugbank/fold0/train.csv` 에 있으면 transductive, 아니면 inductive 모델을 쓰고 응답에 표시한다.
- 확률은 관계마다 따로 씌운 sigmoid 이다 (86개 합이 1 이 아님).
- SMILES 는 원 저장소 `atom_features` 방식으로 그래프를 만들고, `Unknown` 원자가 있으면 표시한다.

## `ddi` 패키지 (`ddi-tools/ddi/`)
- 공개 함수는 `resolve_drug`, `predict`, `predict_many`, `explain`, `save_results` 5개다 (`__all__`).
- `resolve_drug`: 이름·동의어(대소문자 무시, 전체 일치)·DrugBank ID·SMILES 를 받는다. 후보가 여럿이면 후보와 함께 에러, DSN-DDI 데이터에 없는 약물은 거부.
- `predict_many` 는 내부에서 쌍마다 따로 서버에 요청한다. 식별에 실패한 쌍은 빼지 않고 `error` 로 남긴다.
- 학습셋 밖 약물이나 SMILES 신약이면 inductive 사용·신뢰도 경고를 붙인다.
- `save_results(results, path)` 의 CSV 칼럼은 `drug_a, drug_b, relation, prob, model_used, description` 이다 (채점기가 읽는 형식).
- 데이터에 기록된 상호작용(label, 정답)을 돌려주는 함수를 만들지 않는다.
- `client.py` 는 C 컨테이너에서 import 될 때 서버가 없으면 백그라운드로 띄우고, 첫 요청 때 준비될 때까지 기다린다 (import 가 커널 시작을 막으면 OpenHands 런타임이 뜨지 않는다).
