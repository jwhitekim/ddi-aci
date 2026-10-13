# Tasks

## 1. 질문과 정답

- [x] 1.1 `eval/scripts/make_questions.py`로 seed 42의 10문항(서로 다른 관계 10개, 두 약물 모두 fold0 train·약물 사전에 있음, 저장 순서대로 적기, 공통 안내 문장)을 만든다. 확인: 두 번 실행한 결과가 같고, 관계 번호 10개가 모두 다르다
- [x] 1.2 `eval/scripts/make_ground_truth.py`(서버 코드 미사용, `ddi-runtime` 컨테이너)로 10쌍을 두 순서 모두 계산해 `eval/questions/questions.jsonl`을 만든다. 확인: 모든 문항에 두 순서의 정답과 `label`이 있고, 예측 서버 값과의 확률 차이가 1e-4 이하다

## 2. 채점기

- [x] 2.1 `eval/scripts/score.py`의 정규화(이름 → ID, 문장 → 효과·누가·누구에게)를 만든다. 확인: 스모크 결과(`runs/sonnet_C2`, `runs/sonnet_B30`, `runs/sonnet_B`)의 모든 행이 해석되고, B 30턴의 관계 6 행이 "관계 5의 이웃 번호" 문장으로 잡힌다
- [x] 2.2 방향별 ①②③ 판정, 성공·부분 정답, 실패 원인, 지표와 결과 파일을 만든다. 확인: 스모크 Warfarin–Aspirin 결과로 C는 부분 정답(한 방향만 보고), B 10턴은 방향 오류, B 30턴은 모델 선택·번호 체계·방향 오류로 판정된다

## 3. A 실행기

- [x] 3.1 `eval/scripts/run_baseline_a.py`(게이트웨이로 질문만 전송)와 A 답에서 효과·방향을 뽑는 채점(채점기 모델 두 개는 설정값, 불일치는 사람 확인 목록)을 만든다. 확인: 질문 1개로 실제 실행해 답과 추출 결과가 저장된다

## 4. 실행

- [x] 4.1 `eval_spec.md`와 `eval/` 코드를 커밋한다(결과 보기 전 기준 고정). 확인: `git log`에 커밋이 있다
- [x] 4.2 `eval/scripts/run_batch.py`로 10문항을 B·C로 실행하고, A도 10문항을 실행한다. 확인: B·C 실행 폴더 20개와 A 답 10개가 생기고 각 실행의 종료 상태·턴·토큰이 기록된다

## 5. 결과

- [x] 5.1 세 조건을 채점하고 결과와 실제 비용을 정리한다 (사람 확인은 선택 사항으로 변경, `eval_spec.md` 4장). 확인: `eval/RESULTS.md`에 조건별 지표 표, 실패 원인, 실제 비용이 적혀 있다
- [x] 5.2 `ddi_draft.md` 6장(질문, 정답, 지표)을 `eval_spec.md`와 맞추고, 9장에 참고 벤치마크(ScienceAgentBench, CORE-Bench, SUPER)를 추가한다. 확인: 6장의 질문 개수와 지표가 `eval_spec.md`와 같다
