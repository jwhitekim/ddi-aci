# 저장소 구조

| 폴더 | 역할 |
|---|---|
| `ddi-agent/` | 에이전트 실행기. `run_agent.py` 가 조건 B·C 로 OpenHands 0.62.0 CodeActAgent 를 띄우고, `llm_main.py` 가 LLM 캐싱을 켠 뒤 OpenHands 를 시작한다 |
| `ddi-tools/ddi/` | 도구 인터페이스. 에이전트 IPython 에 import 되는 `ddi` 패키지 (`client.py` 가 예측 서버에 요청) |
| `ddi-tools/server/` | 도구 뒷단. 원 DSN-DDI 모델을 감싼 예측 서버 (Python 3.7) |
| `ddi-tools/microagent/` | 조건 C 작업 폴더에 넣는 `ddi` 사용법 |
| `ddi-runtime/` | 런타임 이미지 `ddi-runtime`(B·C), `ddi-specialist`(C), 재현 기록 |
| `benchmarks/ddi/` | 평가 정의: `run_infer.py`(실행), `eval_infer.py`(채점), `prompts/`, `data/`, `scripts/` |
| `eval_outputs/` | 실행 출력. 공개한 평가 `v1/`, `v2/`(보고서, 채점, `raw/` 원자료)만 git 에 올린다 |
| `third_party/DSN-DDI/` | 원 DSN-DDI 저장소 (submodule, 커밋 `6f23522`) |
| `tests/` | `tools/`(도구, 컨테이너 안), `runtime/`(OpenHands 런타임), `layout/`(저장소 구조) |

- 원 DSN-DDI 와 OpenHands 소스는 고치지 않는다. 동작을 바꿀 때는 감싸는 코드(`llm_main.py` 등)를 쓴다.
- 새 실행의 출력은 `eval_outputs/ddi/` 에 쌓는다. 공개하기로 정한 평가만 `eval_outputs/v3/` 처럼 이름을 붙이고 `.gitignore` 예외에 추가한다.
- 공개한 `eval_outputs/v*/raw/` 는 기록이므로 고치지 않는다.
- 폴더나 파일 이름을 바꾸면 `tests/layout/` 의 기대 목록과 옛 이름 목록, README 두 개의 구조 표를 같이 고친다.
