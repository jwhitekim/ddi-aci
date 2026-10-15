# DDI-ACI

**약물 상호작용 예측 모델을 운용하는 LLM 에이전트를 위한 에이전트-컴퓨터 인터페이스**

DDI-ACI는 LLM 에이전트가 약물 상호작용(DDI) 예측 모델 [DSN-DDI](https://github.com/microsoft/Drug-Interaction-Research/tree/DSN-DDI-for-DDI-Prediction)를 실행하고, 그 출력을 정확하게 전달하도록 돕는 모델 특화 에이전트-컴퓨터 인터페이스(ACI)입니다. DSN-DDI와 OpenHands CodeActAgent는 수정하지 않았습니다.

논문: *DDI-ACI: An Agent-Computer Interface for LLM Agents Operating a Drug-Drug Interaction Prediction Model*, Jun-Hee Kim, Sang-Woong Lee (가천대학교 School of Computing)

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

B는 10문항 모두 관계 번호는 맞게 얻었지만 3문항에서 틀렸습니다. q01·q02에서는 설명 파일의 한 행 앞 문장을 골랐고, q04에서는 약물 역할을 뒤집었습니다. B는 접근할 수 있는 데이터 파일에서 기록된 라벨도 찾아봤습니다. 하지만 라벨과 모델 예측이 다른 q01·q03에서도 모델 예측 쪽을 답했습니다.

상세 결과: [`eval/RESULTS.md`](eval/RESULTS.md) · 평가 명세: [`eval/eval_spec.md`](eval/eval_spec.md) · 조건별 답변 비교: [`eval/ANSWER_COMPARISON.md`](eval/ANSWER_COMPARISON.md)

### 한계

- **규모:** 모델 하나(DSN-DDI), 10문항, seed 하나, 문항당 1회 실행인 예비 연구입니다.
- **통계:** B와 C의 차이는 통계적으로 유의하지 않습니다(정확 McNemar 검정 p = 0.25). 결과가 갈린 3문항은 모두 C가 맞혔고, B만 맞힌 문항은 없습니다.
- **검증하지 않은 것:** 반대 약물 순서, 방향이 없는 대칭 관계 7종(`Subject = 3`), C의 도구와 지시문 각각의 효과.
- **사후에 정한 것:** 다음 두 가지는 결과를 본 뒤에 정했습니다([`eval/eval_spec.md`](eval/eval_spec.md) 0장, [`eval/RESULTS_v1.md`](eval/RESULTS_v1.md) 참고).
  - A 채점기를 Gemini 3.5 Flash 하나로 정한 것: A의 출력을 본 뒤
  - 질문 순서 한 방향만 채점하는 기준: v1 실행 결과를 본 뒤

## 저장소 구성

| 경로 | 내용 |
|---|---|
| `ddi/` | DDI skill: 에이전트의 IPython에 import되는 `ddi` 파이썬 패키지 |
| `server/` | 원 DSN-DDI 모델과 가중치를 감싼 예측 서버 (Python 3.7) |
| `agent/` | OpenHands 실행기(`run_agent.py`), 설정 틀, micro agent 프롬프트, 과제 지시 |
| `docker/` | `ddi-runtime` 이미지(B·C), `ddi-specialist` 이미지(C), 재현 기록 |
| `eval/` | 질문, 정답, 채점, 결과, 조건 A, 관계 번호 규칙 검증 |
| `runs/eval/` | v2 실행 원자료: 대화 기록, 로그, 에이전트가 만든 CSV, 토큰 수 |
| `ddi/test/` | `ddi` 패키지 점검 |
| `Drug-Interaction-Research/` | 원 DSN-DDI 저장소 (서브모듈) |

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
docker build -f docker/Dockerfile -t ddi-runtime .                 # B·C
docker build -f docker/Dockerfile.specialist -t ddi-specialist .   # C 전용

# 2. OpenHands 환경
python3.12 -m venv .venv-openhands
.venv-openhands/bin/pip install -r agent/requirements.lock.txt
echo "AI_GATEWAY_API_KEY=..." > .env    # A 채점에는 GEMINI_API_KEY도 필요

# 3. 질문 하나 실행
.venv-openhands/bin/python agent/run_agent.py --condition C \
    --task "Warfarin이랑 Aspirin 상호작용 예측해줘" --out runs/try_C

# 4. 전체 평가
.venv-openhands/bin/python eval/scripts/run_batch.py --condition C --workers 1
.venv-openhands/bin/python eval/scripts/run_batch.py --condition B --workers 2
.venv-openhands/bin/python eval/scripts/run_baseline_a.py
python3 eval/scripts/score.py
```

- 정답은 예측 서버와 독립적으로, 원 DSN-DDI 코드로 계산합니다: `eval/scripts/make_ground_truth.py` (`docker run` 명령은 파일 첫머리 설명 참고)
- 관계 번호 규칙은 규칙 자체를 쓰지 않고 SSI-DDI 약물 쌍과 대조해 검증했습니다: `eval/scripts/verify_relation_map.py` (86종 모두 일치, [`eval/relation_map/`](eval/relation_map/README.md) 참고)
- DSN-DDI 재현 기록(fold0 transductive ACC 0.973, 논문 0.969): [`docker/REPRODUCTION.md`](docker/REPRODUCTION.md)

## 데이터와 출처

- **DSN-DDI** — Li et al., *Briefings in Bioinformatics* 24(1), 2023. 모델·가중치·데이터는 `microsoft/Drug-Interaction-Research`(커밋 `6f23522`)에서 가져옴
- **SSI-DDI** — Nyamabo et al., *Briefings in Bioinformatics* 22(6), 2021. 관계 설명 파일(`Interaction_information.csv`)
- **DrugBank Vocabulary** (CC0) — 약물 이름 사전. `ferrangoeh/DrugLinker`의 사본 사용
- **OpenHands** (0.62.0), **CodeAct** — 에이전트 프레임워크와 행동 형식
- **SWE-agent** — 이 연구가 확장한 ACI 개념

이 연구는 과학기술정보통신부의 재원으로 한국연구재단의 지원을 받아 수행되었습니다(RS-2025-00520064).
