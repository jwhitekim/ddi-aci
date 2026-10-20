# DDI-ACI

**약물 상호작용 예측 모델을 운용하는 LLM 에이전트를 위한 에이전트-컴퓨터 인터페이스**

DDI-ACI는 LLM 에이전트가 약물 상호작용(DDI) 예측 모델 [DSN-DDI](https://github.com/microsoft/Drug-Interaction-Research/tree/DSN-DDI-for-DDI-Prediction)를 실행하고, 그 출력을 정확하게 전달하도록 돕는 모델 특화 에이전트-컴퓨터 인터페이스(ACI)입니다. DSN-DDI와 OpenHands CodeActAgent는 수정하지 않았습니다.

논문: *DDI-ACI: An Agent-Computer Interface for LLM Agents Operating a Drug–Drug Interaction Prediction Model*, Jun-Hee Kim, Sang-Woong Lee (가천대학교 School of Computing)

[English README](README.md)

## 왜 필요한가

LLM 에이전트는 DSN-DDI를 실행하는 데 성공하고도 틀린 답을 낼 수 있습니다. DSN-DDI는 관계 번호(0~85)만 출력하는데, 이 번호를 문장으로 바꾸려면 저장소 고유의 규약을 알아야 합니다. 이 규약을 무시해도 에러는 나지 않습니다.

- 설명 파일(SSI-DDI 제공)에 번호 칸이 두 개 있습니다. DSN-DDI 관계 `t`는 `DDI type N`이 아니라 `Interaction type == t + 1`인 행에 대응합니다.
- 86종 중 42종(`Subject == 2`)은 문장 틀의 약물 순서가 입력 순서와 반대입니다.
- 여러 쌍을 한 배치로 묶으면 예측이 달라집니다(이분 그래프의 `GATConv`가 다른 쌍의 원자끼리도 연결함). 그래서 쌍 하나씩 예측해야 합니다.

DDI-ACI는 이 규칙들을 도구 안에 담았습니다. 그래서 에이전트는 파일을 대조해 규칙을 알아낼 필요 없이, 방향이 맞춰진 문장을 바로 받습니다.

## 결과 (10문항, Claude Sonnet 5.5)

세 조건 모두 같은 LLM을 씁니다. B와 C는 에이전트(OpenHands 0.62.0 CodeActAgent), 과제 지시, temperature 0.0, 기본 추론 강도도 같고, 웹 브라우징과 MCP 도구는 껐습니다.

| | A. LLM 단독 | B. ACI 없는 에이전트 | C. DDI-ACI 에이전트 |
|---|---|---|---|
| **성공률** | 10% | 70% | **100%** |
| 결과 파일까지 실행 | — | 10/10 | 10/10 |
| 평균 턴 | — | 11.4 | 3.2 |
| 평균 프롬프트 토큰 (캐시 읽기 포함) | — | 384,776 | 42,419 |
| 문항당 비용 | 0.021달러 | 0.201달러 | 0.042달러 |

성공은 질문 순서 방향에서, 전달한 문장이 모델 1위 예측과 같은 효과이고 약물 방향도 맞은 경우입니다. 즉 모델 출력과 일치하는지를 재는 것이지, 임상적으로 맞는지를 재는 것이 아닙니다.

B는 10문항 모두 관계 번호는 맞게 얻었지만 3문항에서 틀렸습니다. q01·q02에서는 설명 파일의 한 행 앞 문장을 골랐고, q04에서는 약물 역할을 뒤집었습니다.

상세 결과: [`eval_outputs/v2/RESULTS.md`](eval_outputs/v2/RESULTS.md) · 평가 명세: [`benchmarks/ddi/eval_spec.md`](benchmarks/ddi/eval_spec.md) · 조건별 답변 비교: [`eval_outputs/v2/ANSWER_COMPARISON.md`](eval_outputs/v2/ANSWER_COMPARISON.md)

### 한계

- **규모:** 모델 하나(DSN-DDI), 10문항, seed 하나, 문항당 1회 실행인 예비 연구입니다.
- **통계:** B와 C의 차이는 통계적으로 유의하지 않습니다(정확 McNemar 검정 p = 0.25). 결과가 갈린 3문항은 모두 C가 맞혔고, B만 맞힌 문항은 없습니다.
- **검증하지 않은 것:** 반대 약물 순서, 방향이 없는 대칭 관계 7종(`Subject = 3`), C의 도구와 지시문 각각의 효과.
- **절차:** 과제 지시와 성공 기준은 예비 실행 뒤에 확정했고, 예비 실행 결과는 보고 결과에서 제외했습니다.

## 저장소 구성

| 경로 | 내용 |
|---|---|
| `ddi-agent/` | 에이전트 실행기: 조건 B·C로 OpenHands CodeActAgent를 띄움(`run_agent.py`), 설정 틀 |
| `ddi-tools/ddi/` | 에이전트가 부르는 도구 인터페이스: 에이전트의 IPython에 import되는 `ddi` 파이썬 패키지 |
| `ddi-tools/server/` | 도구 뒷단: 원 DSN-DDI 모델과 가중치를 감싼 예측 서버 (Python 3.7) |
| `ddi-tools/microagent/` | 조건 C에서 작업 폴더에 넣는 micro agent 프롬프트: `ddi` 함수 사용법 |
| `ddi-runtime/` | 런타임 이미지: `ddi-runtime`(B·C), `ddi-specialist`(C), 재현 기록 |
| `benchmarks/ddi/` | 평가: `run_infer.py`(실행), `eval_infer.py`(채점), `prompts/`(모든 질문 뒤에 붙이는 과제 지시), `data/`(질문, 정답, 관계 번호 대응표), `scripts/` |
| `eval_outputs/` | 실행 출력. 공개한 평가 `v1/`, `v2/`(보고서, 채점, `raw/`에 원자료)만 git에 올리고, 새 실행(`eval_outputs/ddi/`) 등 나머지는 git 제외 |
| `third_party/DSN-DDI/` | 원 DSN-DDI 저장소 (서브모듈) |
| `tests/` | 대상별 점검: `tools/`(`ddi` 패키지, 예측 서버. 컨테이너 안에서 실행), `runtime/`(OpenHands 런타임), `layout/`(저장소 구조) |
| `.claude/rules/` | 이 프로젝트 개발 규칙 (구조, 도구 규칙, 비교 조건, 평가, 검증) |

## `ddi` skill

```python
res = ddi.predict("Warfarin", "Aspirin")
res["top"][0]["description"]
# 'Acetylsalicylic acid may increase the anticoagulant activities of Warfarin.'
```

| 함수 | 하는 일 |
|---|---|
| `resolve_drug(x)` | 이름·동의어·DrugBank ID·SMILES → 표준 약물 정보 |
| `predict(a, b, top_k=3)` | 상위 관계, 관계별 확률, 방향이 반영된 문장, 경고 |
| `predict_many(pairs, relation=None)` | 여러 쌍을 하나씩 예측하고, 원하면 관계로 거름 |
| `explain(rel, a, b)` | 관계 번호 → 방향이 반영된 문장 |
| `save_results(res, path)` | 결과를 채점용 CSV로 저장 |

두 약물이 모두 학습셋에 있으면 transductive 가중치를 쓰고, 아니면 inductive 가중치로 바꾸면서 경고를 냅니다. 모르는 약물은 거부하고, 모델이 unknown으로 처리하는 원자 특징이 있으면 경고합니다. 확률은 관계마다 따로 계산한 sigmoid 값이라 86개의 합이 1이 아닙니다.

## 재현 방법

필요한 것: Linux, NVIDIA GPU가 있는 Docker(가중치가 CUDA 텐서로 저장되어 있음), OpenHands용 Python 3.12.

```bash
# 1. 이미지
docker build -f ddi-runtime/Dockerfile -t ddi-runtime .                 # B·C
docker build -f ddi-runtime/Dockerfile.specialist -t ddi-specialist .   # C 전용

# 2. OpenHands 환경
python3.12 -m venv .venv-openhands
.venv-openhands/bin/pip install -r ddi-agent/requirements.lock.txt
echo "AI_GATEWAY_API_KEY=..." > .env    # A 채점에는 GEMINI_API_KEY도 필요

# 3. 질문 하나 실행
.venv-openhands/bin/python ddi-agent/run_agent.py --condition C --task-suffix benchmarks/ddi/prompts/task_suffix.txt \
    --task "Warfarin이랑 Aspirin 상호작용 예측해줘" --out eval_outputs/try_C

# 4. 전체 평가
.venv-openhands/bin/python benchmarks/ddi/run_infer.py --condition C --workers 1
.venv-openhands/bin/python benchmarks/ddi/run_infer.py --condition B --workers 2
.venv-openhands/bin/python benchmarks/ddi/scripts/run_baseline_a.py --output-dir eval_outputs/ddi/A
python3 benchmarks/ddi/eval_infer.py --runs-dir eval_outputs/ddi --out eval_outputs/ddi/scores

# 공개한 v2 원자료(eval_outputs/v2/raw)를 다시 채점해 eval_outputs/v2 에 쓰기
python3 benchmarks/ddi/eval_infer.py
```

- 정답은 예측 서버와 독립적으로, 원 DSN-DDI 코드로 계산합니다: `benchmarks/ddi/scripts/make_ground_truth.py` (`docker run` 명령은 파일 첫머리 설명 참고)
- 관계 번호 규칙은 규칙 자체를 쓰지 않고 SSI-DDI 약물 쌍과 대조해 검증했습니다: `benchmarks/ddi/scripts/verify_relation_map.py` (86종 모두 일치, [`benchmarks/ddi/data/relation_map/`](benchmarks/ddi/data/relation_map/README.md) 참고)
- DSN-DDI 재현 기록(fold0 transductive ACC 0.973, 논문 0.969): [`ddi-runtime/REPRODUCTION.md`](ddi-runtime/REPRODUCTION.md)

## 데이터와 출처

- **DSN-DDI** — Li et al., *Briefings in Bioinformatics* 24(1), 2023. 모델·가중치·데이터는 `microsoft/Drug-Interaction-Research`(커밋 `6f23522`)에서 가져옴
- **SSI-DDI** — Nyamabo et al., *Briefings in Bioinformatics* 22(6), 2021. 관계 설명 파일(`Interaction_information.csv`)
- **DrugBank Vocabulary** (CC0) — 약물 이름 사전. `ferrangoeh/DrugLinker`의 사본 사용
- **OpenHands** (0.62.0), **CodeAct** — 에이전트 프레임워크와 행동 형식
- **SWE-agent** — 이 연구가 확장한 ACI 개념

이 연구는 과학기술정보통신부의 재원으로 한국연구재단의 지원을 받아 수행되었습니다(RS-2025-00520064).
