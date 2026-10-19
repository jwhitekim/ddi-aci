# eval-set Specification

## Purpose

에이전트 평가에 쓸 질문 10문항과 정답을 정의한다. 질문은 DSN-DDI 테스트셋에서 자동으로 만들고, 정답은 원 DSN-DDI 모델을 쌍 하나씩, 두 순서 모두 실행한 결과로 둔다 (`eval_spec.md` 2·3장).

## Requirements

### Requirement: 질문 10문항을 고정된 seed로 자동 생성한다
질문 생성기는 seed 42로 `drugbank/fold0/test.csv`에서 10쌍을 뽑아야 한다(SHALL). 두 약물은 모두 fold0 train에 있고 DrugBank 약물 사전에 이름이 있어야 하며(SHALL), 10쌍의 테스트셋 관계 번호는 서로 달라야 한다(SHALL). 질문은 `{A}이랑 {B} 상호작용 예측해줘` 형식으로, 약물은 데이터 저장 순서대로 적고 순서를 지정하는 표현은 넣지 않아야 한다(SHALL). 모든 질문 뒤에는 B·C 공통 안내 문장을 붙여야 한다(SHALL).

#### Scenario: 재생성
- **WHEN** 같은 seed로 질문 생성기를 두 번 실행하면
- **THEN** 두 결과가 똑같다

#### Scenario: 서로 다른 관계
- **WHEN** 10문항의 테스트셋 관계 번호를 보면
- **THEN** 10개가 모두 다르다

### Requirement: 정답은 원 모델을 쌍 하나씩, 두 순서 모두 실행한 결과다
정답 생성기는 예측 서버 코드를 쓰지 않고 원 DSN-DDI의 데이터 처리 코드·모델·가중치로 계산해야 한다(SHALL). 쌍 하나씩(배치 크기 1) 계산하고 (A, B)와 (B, A)를 모두 계산해야 한다(SHALL). 순서마다 1위 관계, 확률, 방향이 반영된 문장(`Interaction type == t + 1`, `Subject == 2`이면 약물 순서를 뒤집음)을 저장해야 한다(SHALL).

#### Scenario: 예측 서버와 일치
- **WHEN** 정답 생성기와 예측 서버로 같은 쌍·같은 순서를 계산하면
- **THEN** 관계별 확률 차이가 1e-4 이하다

### Requirement: 질문과 정답은 한 파일에 저장한다
질문과 정답은 `eval/questions/questions.jsonl`에 한 줄에 한 문항으로 저장해야 한다(SHALL). 각 줄에는 `qid`, `question`, `drugs`(데이터 저장 순서의 DrugBank ID 두 개), 두 순서의 `ground_truth`(모델, 상위 관계·확률·문장), `label`(테스트셋의 실제 관계)이 있어야 한다(SHALL).

#### Scenario: 두 순서의 정답
- **WHEN** 문항 하나를 보면
- **THEN** (A, B)와 (B, A) 두 순서의 정답이 모두 있다
