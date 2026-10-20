# 검증

바꾼 곳에 따라 아래를 돌린다. 통과하면 로컬 커밋까지 하고, 원격 푸시는 사람 확인을 받는다.

| 바꾼 곳 | 검증 |
|---|---|
| 폴더·파일 이름, 경로, 문서 | `python3 tests/layout/layout_structure.py`, `layout_paths.py`, `layout_git.py` |
| `ddi-tools/ddi/` | `tests/tools/check_ddi.py` (예측 서버 컨테이너 네트워크에서, 명령은 파일 첫머리) |
| `ddi-tools/server/` | `tests/tools/check_original.py`(원 모델과 확률 일치), `check_edges.py`(경계 입력) |
| `ddi-agent/`, `ddi-runtime/` | `tests/runtime/check_runtime.py --condition {B,C} --out eval_outputs/scratch/check_{B,C}` (LLM 없이 런타임만) |
| 채점 코드 | 인자 없는 `eval_infer.py` 결과가 `eval_outputs/v2/` 와 같은지 (`git diff`) |
