# 제목·초록 초안

작성일: 2026-10-12 · 상태: 초안 (v2 결과 반영, `eval/RESULTS.md`)

## 1. 제목 (확정)

> **DDI-ACI: A Domain-Specific Agent-Computer Interface for LLM Agents Operating a Drug–Drug Interaction Prediction Model**
>
> (DDI-ACI: 약물 상호작용 예측 모델을 운용하는 LLM 에이전트를 위한 도메인 특화 에이전트-컴퓨터 인터페이스)

- **중심:** 이 연구가 새로 만든 것은 DDI 전용 ACI 하나다. 모델(DSN-DDI)과 에이전트(OpenHands CodeActAgent)는 그대로 가져와 쓰고, 그 사이에 ACI만 넣었다. 그래서 이름과 제목 모두 ACI를 가리킨다
- **형식:** 에이전트 논문에서 흔한 "이름: 명사구" (예: OpenHands: An Open Platform for AI Software Developers as Generalist Agents)
- **이름 DDI-ACI:** DDI(약물 상호작용) + ACI(에이전트-컴퓨터 인터페이스). 약학 전반이 아니라 이 연구의 범위(약물 상호작용)에 한정된 이름
- **범위:** DSN-DDI 사례 하나에 맞춘 제목. "framework"처럼 일반화를 따로 증명해야 하는 표현은 쓰지 않음
- **비슷한 이름:** DDIAgents(2026, arXiv 2606.31085)는 DDI를 직접 예측하는 다중 에이전트 시스템으로, 접근이 다르다. 관련 연구에서 구분해 언급한다

## 2. 기여

1. **DDI 전용 ACI의 설계와 구현 (주 기여).** 원 DSN-DDI 모델을 감싼 예측 서버, 에이전트가 호출하는 도구(`ddi`: 약물 식별, 예측, 관계 해석, 결과 저장), 설명서(micro agent)로 구성한다. 모델에 숨어 있는 규칙(관계 번호 t → 설명 파일 t+1 행, 86개 관계 중 42개의 약물 순서 뒤집힘, transductive/inductive 모델 선택, 여러 쌍을 묶으면 값이 섞이므로 쌍 하나씩 계산)을 도구 안에서 처리한다
2. **ACI만 다르게 한 비교 실험.** 같은 LLM(Claude Sonnet 5.5)과 같은 에이전트 구조에서 LLM 단독(A), ACI 없는 에이전트(B), DDI-ACI를 갖춘 에이전트(C)를 비교한다. 정답은 원 모델 출력이고, 보고한 상호작용의 효과 종류와 약물 방향으로 채점한다
3. **실패 유형 분석.** ACI 없는 에이전트는 모델을 실행해 결과 파일까지 만들지만, 관계 번호를 한 칸 밀려 쓰거나 약물 방향을 뒤집거나 모델을 잘못 고르는 등 실행 오류 없이 해석이 틀린 결과를 낸다는 것을 보인다

## 3. 초록 (한국어)

LLM 에이전트는 기존 예측 모델 및 도메인 도구를 활용하여 과학 연구 환경과 상호작용하는 수단으로 적용 범위를 넓혀가고 있다. 소프트웨어 공학 환경에서는 에이전트-컴퓨터 인터페이스(ACI) 설계의 중요성이 확인되었으나, 도메인 특화 ACI가 과학 예측 모델 환경에서도 에이전트의 수행 능력에 미치는 영향은 아직 충분히 검증되지 않았다. 본 논문에서는 약물 상호작용 예측 모델인 DSN-DDI 환경에서 LLM 에이전트의 상호작용을 지원하는 도메인 특화 인터페이스인 DDI-ACI를 제안한다. DDI-ACI는 별도의 LLM 파인튜닝 없이 DDI 예측 모델의 입출력 처리를 추상화하여 에이전트에 해석 가능한 약물 간 상호작용 정보를 제공한다. 공개 DrugBank 테스트셋 10개 질의를 대상으로 Claude Sonnet 5.5를 사용한 단독 LLM, OpenHands 기반 ACI 미적용 에이전트, DDI-ACI 기반 에이전트의 예측 정합성과 작업 효율성을 비교하였다. 실험 결과, DDI-ACI 기반 에이전트는 100%의 성공률을 달성하여 단독 LLM(10%)과 ACI 미적용 에이전트(70%)를 상회하였으며, 평균 턴 수(3.2턴 대 11.4턴)와 프롬프트 토큰 소비량(약 4.2만 대 38만)을 줄였다. 이는 도메인 특화 ACI가 과학 예측 모델을 활용하는 LLM 에이전트의 수행 정확도와 작업 효율성을 개선할 수 있음을 시사한다.

## 3.1 Abstract (English)

LLM agents are increasingly being used to interact with scientific research environments by leveraging existing predictive models and domain tools. While the importance of agent-computer interface (ACI) design has been established in software engineering environments, the effect of domain-specific ACIs on agent performance within scientific prediction model environments remains insufficiently explored. In this paper, we propose DDI-ACI, a domain-specific interface that supports LLM agent interaction within the DSN-DDI drug-drug interaction prediction environment. Without fine-tuning the LLM, DDI-ACI abstracts the input and output processing of the DDI prediction model to provide the agent with interpretable drug–drug interaction information. Using Claude Sonnet 5.5 across 10 queries from a public DrugBank test set, we compared the prediction consistency and task efficiency of a standalone LLM, an OpenHands agent without an ACI, and the same agent equipped with DDI-ACI. Experimental results showed that the DDI-ACI-based agent achieved a 100% success rate, outperforming the standalone LLM (10%) and the agent without ACI (70%), while reducing average interaction turns (3.2 vs. 11.4) and prompt token consumption (~42k vs. ~380k). These results suggest that domain-specific ACI design can improve the execution accuracy and task efficiency of LLM agents utilizing scientific prediction models.

## 4. 수치와 근거

| 수치 | 출처 | 상태 |
| --- | --- | --- |
| 성공률 A 10% / B 70% / C 100% | `eval/RESULTS.md` (v2, 기준은 `eval_spec.md` 0장) | A q08은 채점기 불일치 사람 확인 후 확정 |
| 턴 3.2 vs 11.4, 프롬프트 토큰 약 4.2만 vs 38만 | `eval/results/summary.json` | 확정 |
| B 실패 유형 (문장 행 어긋남 2, 방향 1) | `eval/RESULTS.md` 2장 | 확정 |

## 5. 메모

- 초록·제목은 참고 논문(SWE-agent, OpenHands, CodeAct, AgenticIR)의 요점을 정리해 프롬프트로 주고, Gemini 3.5 Flash가 판단·작성했다. 흐름: 에이전트·AI for science → SWE-agent의 ACI → 연구 질문 → DDI-ACI → 실험 → 결과 → 의의
- 초록 근거 문헌(본문 인용 예정): 첫 문장 — ChemCrow(Bran et al., Nat. Mach. Intell. 2024), Coscientist(Boiko et al., Nature 2023), Biomni(2025 preprint), AgenticIR(ICLR 2025), 과학 에이전트 서베이(arXiv 2503.24047) / ACI — SWE-agent(NeurIPS 2024), 후속은 코딩·컴퓨터 사용 중심(arXiv 2505.21055, 2510.04607 등) / 평가 방식 — CORE-Bench(TMLR 2024, 공개 연구 코드 결과 재현)
- "과학 예측 모델에 ACI를 적용·비교한 사례는 드물다"는 웹 검색 몇 번으로 확인한 범위라 "우리가 아는 한"으로 썼다. 관련 연구 정리 때 더 찾아봐야 한다
- 10문항 사례 연구라 결론은 "시사한다" 수준으로 썼다
- "에러 없이 틀린다", "silent" 같은 표현은 오해를 불러서 쓰지 않는다. 대신 "실행 오류는 없지만 해석이 틀린" (executability는 성공, correctness는 실패)으로 쓴다
- DSN-DDI의 배치 섞임 문제(원 평가 방식 때문에 점수가 부풀려짐)는 초록에 넣지 않았다. 다룬다면 한 문장 추가 가능
- 영어 초록(3.1)은 한국어 초록과 같은 내용이며, 수치는 함께 채운다
- 실행 규칙 (실험 설정에서 밝힘): B·C 모두 10문항, 문항당 1회. 시간 초과(20분)나 실행 횟수 한도(30회)에 걸리면 그 상태로 끝내고 다시 돌리지 않는다. 채점은 그때까지 저장된 결과 CSV 기준이다. B는 결과를 저장한 뒤 종료 도구(finish)를 부르지 않고 같은 보고를 반복해 한도에 걸린 문항이 많았고, 턴·시간·토큰은 이 반복이 포함된 값이다
