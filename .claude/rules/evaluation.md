---
paths:
  - "benchmarks/**"
  - "eval_outputs/**"
---

# 평가

채점 기준의 원본은 `benchmarks/ddi/eval_spec.md` 다. 기준을 바꾸면 이 문서를 먼저 고친다.

- 질문: `make_questions.py` 가 seed 42 로 `drugbank/fold0/test.csv` 에서 10쌍을 뽑는다 (두 약물 모두 fold0 train 과 약물 사전에 있고, 관계 번호가 서로 다름). 질문은 `{A}이랑 {B} 상호작용 예측해줘`, 약물은 데이터 저장 순서.
- 정답: `make_ground_truth.py` 가 예측 서버 코드 없이 원 DSN-DDI 코드로, 쌍 하나씩, 두 순서 모두 계산한다. 결과는 `data/questions/questions.jsonl` 에 질문과 함께 저장.
- 채점(`eval_infer.py`): 질문 순서 한 방향만 본다. 답 문장이 모델 1위와 같은 효과이고 약물 방향도 맞으면 성공. 관계 번호 일치는 참고 지표. A·B·C 같은 기준.
- 실패한 문항은 원인을 하나 이상 기록한다 (실행 실패, 약물 식별 실패, 모델 선택 오류, 번호→문장 대응 오류, 방향 오류, 기록 베끼기 의심 등).
- 실행 순서: `run_infer.py --condition {B,C}` → `run_baseline_a.py` → `eval_infer.py --runs-dir eval_outputs/ddi --out eval_outputs/ddi/scores`. B·C 일괄 실행과 채점은 `scripts/run_eval.sh` (A 는 따로 실행).
- `eval_infer.py` 를 인자 없이 실행하면 공개한 `eval_outputs/v2/raw` 를 다시 채점해 `eval_outputs/v2` 에 쓴다. 채점 코드를 고친 뒤 이 결과가 바뀌면 의도한 변경인지 확인한다.
