---
paths:
  - "ddi-agent/**"
  - "ddi-runtime/**"
  - "benchmarks/ddi/prompts/**"
  - "benchmarks/ddi/run_infer.py"
  - "benchmarks/ddi/scripts/run_baseline_a.py"
---

# 비교 조건 A·B·C

| | A. LLM 단독 | B. ACI 없는 에이전트 | C. DDI-ACI 에이전트 |
|---|---|---|---|
| 실행 | `run_baseline_a.py` (LLM API 만) | `run_agent.py --condition B` | `run_agent.py --condition C` |
| 이미지 | 없음 | `ddi-runtime` | `ddi-specialist` |
| ACI | 없음 | 없음 | `ddi` 패키지, 예측 서버, micro agent |

- B 와 C 는 ACI 외의 모든 설정이 같아야 한다: 같은 LLM, temperature 0.0, 추론 강도 기본값(설정하지 않음), 최대 30턴, GPU, 웹 브라우징·MCP 끔, 같은 과제문.
- 과제문 = 질문 + `benchmarks/ddi/prompts/task_suffix.txt` (`--task-suffix` 로 붙임). 이 파일을 바꾸면 B·C 모두 다시 실행해야 비교가 유지된다.
- B·C 차이는 기본 이미지, C 전용 마운트(현재 `ddi-tools/ddi`, `ddi-tools/server` 를 읽기 전용으로 이미지의 옛 사본 위에 덮음), C 작업 폴더의 `.openhands/microagents/ddi.md` 뿐이다.
- B 컨테이너에는 `ddi` 패키지, 예측 서버, micro agent 가 없어야 한다. B 도 DSN-DDI 환경(`/opt/conda/envs/dsn/bin/python`, `/opt/DSN-DDI`)과 GPU 는 쓸 수 있다.
- `ddi-runtime` 이미지는 B·C 공통 재료(DSN-DDI 코드, 가중치 2개, 압축 푼 데이터, `ddi-tools/ddi/data/` 에서 복사한 설명 파일과 DrugBank 약물 이름 사전)만 담고 ACI 는 담지 않는다. 데이터는 LFS 포인터가 아닌 실제 파일이어야 한다.
- DSN-DDI 환경은 Python 3.7, PyTorch 1.9.0(CUDA 10.2), PyG 2.0.3, rdkit 2020.09.2 이고 인터프리터는 `/opt/conda/envs/dsn/bin/python` 에 고정한다. 원 `drugbank_test/transductive_test.py`, `inductive_test.py` 가 코드 수정 없이 GPU 에서 논문 수치를 재현해야 한다 (`ddi-runtime/REPRODUCTION.md`).
- `run_info.json` 에는 OpenHands 버전, 조건, 질문, 종료 상태, 턴 수, 걸린 시간, 토큰 사용량을 남긴다.
- 어떤 조건도 정답(label)을 조회할 수 없어야 한다.
- 실행 한 번은 `run_infer.py` 에서 20분 제한이 있고, 넘기면 문항 폴더에 `TIMEOUT` 을 남긴다. 30턴을 넘기면 `run_info.json` 상태가 `max_iterations` 다.
