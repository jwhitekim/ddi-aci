# A 채점 확인표 (선택)

A의 채점기는 Gemini 3.5 Flash 하나다 (`eval_spec.md` 0장). 아래는 Flash 추출 결과와 자동 판정이고, 사람이 다시 볼 때 쓴다.
Sonnet 5.5 추출 결과는 일치율 참고용이다 (추출 일치 3/10, 성공 여부 판정 10/10 일치).

사람 판정 칸: O(정답과 같은 효과·방향을 말함) / X(말하지 않음 또는 다르게 말함)

## q01 — Saquinavir이랑 Bepridil 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 69):** The therapeutic efficacy of Bepridil can be decreased when used in combination with Saquinavir.
- **Flash 추출 (채택):** The risk or severity of QTc prolongation can be increased when Saquinavir is combined with Bepridil.; The metabolism of Bepridil can be decreased when combined with Saquinavir.; The serum concentration of Bepridil can be increased when it is combined with Saquinavir.
- **자동 판정:** 실패
- 참고 — Sonnet 추출: Saquinavir may increase the QTc-prolonging activities of Bepridil.; Saquinavir may increase the atrioventricular blocking (AV block) activities of Bepridil.; The metabolism of Bepridil can be decreased when combined with Saquinavir.; Saquinavir may increase the bradycardic activities of Bepridil.; The serum concentration of Bepridil can be increased when it is combined with Saquinavir. (Flash와 다름)
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

# Saquinavir + Bepridil 상호작용 예측

## 결론
**병용 금기 또는 가능한 한 피할 것 (위험도: 높음, 중대한 상호작용)**

## 기전

**1. 약동학적 상호작용 (CYP3A4)**
- Saquinavir는 CYP3A4의 기질이면서 강한 억제제입니다. 실제로는 대부분 ritonavir와 함께 부스팅해서 쓰므로 CYP3A4 억제가 더 강해집니다.
- Bepridil은 CYP3A4와 CYP2D6로 대사됩니다.
- 따라서 bepridil의 대사가 억제되어 혈중 농도가 상승하고, 독성 위험이 커질 것으로 예측됩니다.

**2. 약력학적 상호작용 (QT 연장)**
- Saquinavir는 용량 의존적으로 QT 및 PR 간격을 연장시킬 수 있습니다.
- Bepridil은 QT 연장 작용이 강하고 torsades de pointes(TdP) 위험이 잘 알려져 있습니다. 이 때문에 미국에서는 시장에서 철수했고, 일본 등 일부 국가에서만 제한적으로 사용됩니다.
- 두 약물의 효과가 상가적 또는 상승적으로 작용합니다.

## 예상되는 임상 결과
- QTc 연장
- Torsades de pointes 등 치명적 심실성 부정맥
- 서맥, 방실차단 (PR 연장 효과가 더해짐)
- 어지러움, 실신, 심장사 가능성

## 위험 요인 (위험이 더 커지는 경우)
- 저칼륨혈증, 저마그네슘혈증
- 선천성 또는 후천성 QT 연장
- 구조적 심질환, 서맥
- 고령, 여성
- 다른 QT 연장 약물이나 CYP3A4 억제제 병용
- Ritonavir 부스팅 용법

## 권고 사항
1. **병용을 피합니다.** Ritonavir 제품 라벨에도 bepridil은 병용 금기 약물로 오래 기재되어 왔습니다.
2. 대안을 고려합니다.
   - 협심증: β-차단제, 또는 상호작용이 덜한 칼슘채널차단제(CYP3A4 상호작용은 용량 조절 필요)
   - HIV 치료: QT 영향이 적은 integrase inhibitor 기반 요법(dolutegravir 등)으로 변경 가능성 검토
3. 부득이하게 병용해야 한다면
   - 투여 전과 투여 중 ECG로 QTc를 모니터링합니다.
   - K⁺, Mg²⁺, Ca²⁺ 수치를 교정하고 유지합니다.
   - bepridil을 최소 용량으로 시작합니다.
   - 실신, 심계항진 등 증상이 생기면 즉시 중단하고 평가합니다.

## 참고
이 내용은 약물 기전과 약물 라벨 정보에 근거한 예측입니다. saquinavir와 bepridil 단독 병용에 대한 대규모 임상시험 자료는 제한적입니다. 실제 처방 시에는 최신 라벨, Lexicomp, Micromedex, Liverpool HIV Drug Interactions 등으로 확인하시길 권합니다.

</details>

## q02 — Cyclophosphamide이랑 Gemcitabine 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 14):** Cyclophosphamide may increase the cardiotoxic activities of Gemcitabine.
- **Flash 추출 (채택):** The therapeutic efficacy of Cyclophosphamide can be increased when used in combination with Gemcitabine.; Cyclophosphamide may increase the immunosuppressive activities of Gemcitabine.; Cyclophosphamide may increase the myelosuppressive activities of Gemcitabine.; Cyclophosphamide may increase the hepatotoxic activities of Gemcitabine.
- **자동 판정:** 실패
- 참고 — Sonnet 추출: The therapeutic efficacy of Cyclophosphamide can be increased when used in combination with Gemcitabine.; The therapeutic efficacy of Gemcitabine can be increased when used in combination with Cyclophosphamide.; Gemcitabine may increase the myelosuppressive activities of Cyclophosphamide.; Cyclophosphamide may increase the myelosuppressive activities of Gemcitabine.; Gemcitabine may increase the hepatotoxic activities of Cyclophosphamide.; Cyclophosphamide may increase the hepatotoxic activities of Gemcitabine. (Flash와 다름)
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

# Cyclophosphamide + Gemcitabine 상호작용 예측

## 1. 요약
| 구분 | 예측 |
|---|---|
| 약동학(PK) 상호작용 | **거의 없음~낮음** |
| 약력학(PD) 상호작용 | **중등도** (독성 중첩, 일부 상승효과 가능) |
| 임상적 의미 | 병용 금기는 아님. **골수억제 중심으로 모니터링 필요** |

## 2. 약동학적 측면

**Cyclophosphamide**
- 전구약물로 간 CYP2B6 (주), 2C9, 2C19, 3A4에 의해 4-OH-CP로 활성화되고, 이후 phosphoramide mustard와 acrolein이 생성됩니다.
- ALDH와 GST로 해독되고, 신장으로 배설됩니다.

**Gemcitabine**
- CYP 대사 경로가 아닙니다.
- dCK에 의해 dFdCMP → dFdCDP → dFdCTP로 활성화되고, cytidine deaminase(CDA)에 의해 dFdU로 불활성화됩니다.

**예측**
- 두 약물은 대사 경로가 겹치지 않고, gemcitabine은 CYP를 유의하게 억제하거나 유도하지 않습니다.
- 따라서 CYP 매개 PK 상호작용 가능성은 낮습니다.
- 다만 개인 간 변동(CYP2B6 다형성, CDA 활성 차이)은 각각의 독성 편차에 영향을 줄 수 있습니다.

## 3. 약력학적 측면

**(1) 상승/시너지 가능성**
- Gemcitabine의 dFdCDP가 ribonucleotide reductase를 억제해 dNTP pool(특히 dCTP)이 감소합니다.
- 이로 인해 gemcitabine 활성체의 DNA 삽입이 늘고(self-potentiation), cyclophosphamide가 만든 DNA 교차결합의 복구가 방해될 수 있습니다.
- 저용량(metronomic) cyclophosphamide는 Treg를 감소시켜 면역 매개 항종양 효과를 보조할 수 있으며, 췌장암 면역치료 연구 등에서 이 개념이 쓰였습니다.
- 투여 순서와 간격에 따라 효과와 독성이 달라질 수 있습니다.

**(2) 독성 중첩**
| 독성 | Cyclophosphamide | Gemcitabine | 예측 |
|---|---|---|---|
| 골수억제 (호중구감소, 혈소판감소) | ++ | ++ | **가산~상승** (가장 중요) |
| 오심/구토 | ++ | + | 가산 |
| 간독성 (AST/ALT 상승) | + | + | 가산 |
| 폐독성 | 드묾 | 드묾~+ (pneumonitis, capillary leak) | 주의 |
| 신독성/TMA | 방광독성 (출혈성 방광염) | HUS/TMA, 단백뇨 | 다른 기전이지만 신·비뇨기계 모니터링 |
| 감염 위험 | ↑ (면역억제) | ↑ | 가산 |

## 4. 모니터링 및 관리 제안
- **CBC**: 각 주기 전에 확인하고, 필요하면 nadir 시점(보통 7~14일)에도 확인합니다. ANC와 혈소판 기준에 따라 용량 감량이나 지연을 고려합니다.
- **간기능, 신기능(Cr, 단백뇨)**: 기저치와 주기별로 확인합니다.
- **호흡기 증상**: 새로운 호흡곤란이나 기침이 있으면 약물 유발 폐렴을 의심합니다.
- **수분 섭취와 배뇨**: 방광 보호를 위해 충분한 수분을 섭취하고, 고용량이면 mesna를 고려합니다.
- **혈압, 부종, 용혈 징후**: gemcitabine에 의한 TMA/HUS를 감시합니다.
- **지지요법**: 필요시 G-CSF, 항구토제, 감염 예방을 사용합니다.
- **생백신은 피합니다.**
- 방사선 병행 시 gemcitabine의 방사선 증감 효과로 독성이 커질 수 있습니다.

## 5. 한계
- 이 내용은 약리학적 기전과 독성 프로파일에 근거한 **예측**이며, 특정 용량과 스케줄의 병용 데이터를 대체하지 못합니다.
- 실제 적용 시에는 환자 상태(골수 예비능, 간·신기능, 병용약), 암종, 프로토콜을 고려해야 합니다.
- Lexicomp, Micromedex, 해당 프로토콜 문헌과 종양내과 약사나 담당의와 확인하시길 권합니다.

특정 암종, 용량, 스케줄(예: metronomic 병용)이나 다른 병용약이 있으면 알려주세요. 더 구체적으로 분석해 드리겠습니다.

</details>

## q03 — Nevirapine이랑 Clopidogrel 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 25):** Nevirapine may decrease the antiplatelet activities of Clopidogrel.
- **Flash 추출 (채택):** Nevirapine may increase the antiplatelet activities of Clopidogrel.; The risk or severity of bleeding can be increased when Nevirapine is combined with Clopidogrel.; The serum concentration of Nevirapine can be increased when it is combined with Clopidogrel.; The serum concentration of the active metabolites of Clopidogrel can be increased when Clopidogrel is used in combination with Nevirapine.
- **자동 판정:** 실패
- 참고 — Sonnet 추출: The metabolism of Nevirapine can be decreased when combined with Clopidogrel.; Nevirapine may increase the antiplatelet activities of Clopidogrel.; The risk or severity of bleeding can be increased when Nevirapine is combined with Clopidogrel.; The serum concentration of the active metabolites of Clopidogrel can be increased when Clopidogrel is used in combination with Nevirapine. (Flash와 다름)
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

# Nevirapine ↔ Clopidogrel 상호작용 예측

※ 직접적인 임상 연구는 거의 없어서, 약동학적 기전을 바탕으로 한 **예측**입니다.

## 1. 관련 대사 경로

| 약물 | 관련 효소 |
|---|---|
| **Clopidogrel** (프로드럭) | 약 85%는 CES1에 의해 불활성 대사체로 가수분해됩니다. 나머지는 CYP2C19(주), 3A4, 2B6, 1A2, 2C9에 의해 2-oxo-clopidogrel을 거쳐 활성 대사체가 됩니다. 또한 clopidogrel과 그 glucuronide는 **CYP2B6와 CYP2C8을 억제**합니다. |
| **Nevirapine** | CYP3A4와 2B6의 기질이면서 **이 두 효소의 유도제**입니다(자가유도 포함). CYP2C19에는 큰 영향이 없습니다. |

## 2. 예측되는 상호작용

**① Nevirapine → Clopidogrel (주된 방향)**
- Nevirapine이 CYP3A4/2B6를 유도하면 clopidogrel의 활성 대사체 생성이 **증가**할 수 있습니다.
- 그 결과 혈소판 억제가 커지고 **출혈 위험이 다소 높아질 가능성**이 있습니다. rifampin이 활성 대사체 노출을 크게 올린 것과 같은 방향이지만, nevirapine은 유도 강도가 약해 효과도 작을 것으로 예상합니다.
- 활성화의 주경로인 CYP2C19는 유도되지 않으므로 영향은 제한적일 것입니다.
- 효과 감소(항혈전 효능 저하)가 일어날 가능성은 낮습니다.

**② Clopidogrel → Nevirapine (부차적 방향)**
- Clopidogrel의 CYP2B6 억제로 nevirapine의 일부 대사(2B6 의존 수산화)가 줄어 nevirapine 농도가 **약간 상승**할 수 있습니다.
- 다만 nevirapine은 3A4 등 여러 경로로도 대사되고 자가유도도 있어 임상적 의미는 작을 것으로 봅니다.

## 3. 종합 평가
- **위험도: 낮음~중등도 (이론적)**
- 병용 금기는 아니며, 용량 조절이 일반적으로 필요하지도 않습니다.

## 4. 임상 관리 제안
- 출혈 징후(멍, 코피, 위장관 출혈, 흑색변)를 모니터링합니다.
- 특히 고령, 위장관 출혈 병력, 아스피린·NSAID·항응고제 병용 환자는 주의합니다.
- 필요하면 혈소판 기능 검사(VerifyNow 등)와 CYP2C19 유전자형을 참고합니다.
- Nevirapine 초기 14일 lead-in 기간과 유도가 안정화되는 시기(2~4주)에 특히 신경 씁니다.
- 간독성은 nevirapine의 주요 위험이므로 간기능을 모니터링합니다. 간기능 저하는 clopidogrel 활성화에도 영향을 줄 수 있습니다.
- Omeprazole/esomeprazole 같은 CYP2C19 억제 PPI는 피하고, 필요하면 pantoprazole을 사용합니다.

## 5. 대안 고려 시 참고
- **Ticagrelor**는 CYP3A4 기질이라 유도제와 병용하면 농도가 떨어질 수 있습니다. 강한 유도제는 피하도록 권고되므로 nevirapine과의 병용도 주의가 필요합니다.
- **Prasugrel**도 CYP3A4/2B6를 통해 활성화되지만 의존도가 낮아 상대적으로 영향이 적을 것으로 예상됩니다.

실제 처방 시에는 Liverpool HIV Drug Interactions, Lexicomp 등 최신 DB를 한 번 더 확인하시길 권합니다.

</details>

## q04 — Sulpiride이랑 Flupentixol 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 35):** Flupentixol may increase the antipsychotic activities of Sulpiride.
- **Flash 추출 (채택):** Sulpiride may increase the anticholinergic activities of Flupentixol.; Sulpiride may increase the adverse neuromuscular activities of Flupentixol.; Sulpiride may increase the orthostatic hypotensive activities of Flupentixol.; Sulpiride may increase the sedative activities of Flupentixol.; The risk or severity of QTc prolongation can be increased when Sulpiride is combined with Flupentixol.; The risk or severity of adverse effects can be increased when Sulpiride is combined with Flupentixol.; Sulpiride may increase the arrhythmogenic activities of Flupentixol.
- **자동 판정:** 실패
- 참고 — Sonnet 추출: Sulpiride may increase the QTc-prolonging activities of Flupentixol.; Sulpiride may increase the orthostatic hypotensive activities of Flupentixol.; Sulpiride may increase the sedative activities of Flupentixol.; The risk or severity of adverse effects can be increased when Sulpiride is combined with Flupentixol. (Flash와 다름)
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

# Sulpiride + Flupentixol 상호작용 예측

## 요약
- **약동학(PK) 상호작용**: 거의 없음 또는 미미함
- **약력학(PD) 상호작용**: 중요함. 둘 다 D2 차단제라서 부작용이 **상가·상승**될 수 있음
- **임상적 중요도**: 중등도 (병용 자체가 금기는 아니지만 주의와 모니터링 필요)

---

## 1. 약동학적 측면
| 약물 | 주요 대사/배설 |
|---|---|
| Sulpiride | 대사 거의 없음, **신장으로 미변화체 배설** (CYP 비의존) |
| Flupentixol | 간 대사 (CYP2D6, CYP3A4, 글루쿠론산 포합) |

- 서로의 대사 경로가 겹치지 않아 CYP 매개 상호작용은 예상되지 않습니다.
- 다만 **신기능 저하 시 sulpiride 축적**으로 부작용이 커질 수 있습니다. 이는 약물 상호작용이 아니라 환자 요인입니다.

---

## 2. 약력학적 상호작용 (핵심)

**① 추체외로 증상(EPS) 및 지연성 운동이상증 위험 증가**
- Flupentixol은 D2 차단이 강한 typical 계열이고, sulpiride는 선택적 D2/D3 차단제입니다.
- 병용하면 총 D2 점유율이 올라 파킨슨증, 정좌불능, 근긴장이상 위험이 커집니다.

**② 고프로락틴혈증**
- Sulpiride는 항정신병약 중 프로락틴 상승 효과가 가장 큰 편이고 flupentixol도 이를 올립니다.
- 유즙분비, 무월경, 성기능장애, 골밀도 감소 위험이 있습니다.

**③ QT 연장 / 부정맥 위험**
- 두 약 모두 QT 연장 가능성이 있습니다. Sulpiride는 특히 용량 의존적이며 저칼륨혈증에서 위험이 커집니다.
- 다른 QT 연장 약물(macrolide, fluoroquinolone, ondansetron 등)이나 전해질 이상이 겹치면 위험이 더 증가합니다.

**④ 신경이완제 악성증후군(NMS)**
- 드물지만 병용 시 위험이 누적될 수 있습니다.

**⑤ 기타 상가 효과**
- 진정, 기립성 저혈압(flupentixol 쪽이 더 강함), 항콜린 효과(둘 다 약함)
- 경련 역치 저하 (flupentixol 쪽이 더 큼)
- 체중 증가와 대사 이상 (둘 다 중등도 이하)

---

## 3. 참고할 임상 상황
- **Deanxit®** (flupentixol + melitracen)과 **sulpiride**(예: Dogmatyl®)는 기능성 소화불량, 불안·우울 증상 등에서 **저용량으로 함께 처방되는 경우**가 있습니다.
- 저용량에서는 위험이 낮지만 **중복 D2 차단**이라는 점은 같으므로 장기 병용 시 EPS, 프로락틴, QT를 점검해야 합니다.
- Sulpiride는 저용량에서 오히려 활성화 효과가 있고, 고용량(>400 mg/day)에서 항정신병 효과와 부작용이 뚜렷해집니다.

---

## 4. 모니터링 및 관리
- **ECG**: 기저 QT 확인, 고용량이거나 위험 인자가 있으면 추적
- **전해질**: K, Mg
- **신기능**: eGFR에 따라 sulpiride 감량
- **EPS 평가**: 진전, 경직, 정좌불능, 구강 이상운동 (AIMS)
- **프로락틴 관련 증상** 확인 (필요 시 혈중 프로락틴 측정)
- 가능하면 **최저 유효용량, 최단 기간**으로 사용하고, 명확한 근거가 없으면 항정신병약 다중 병용을 피합니다.
- 고령자(특히 치매 환자)는 사망률과 뇌혈관 위험이 증가하므로 더 주의합니다.
- 위험 인자: QT 연장 병력, 서맥, 저칼륨혈증, 파킨슨병, 신부전, 고령

---

이 내용은 약리학적 근거에 기반한 **예측**입니다. 실제 처방 조정은 환자의 용량, 기저질환, 병용약을 고려해 담당 의사나 약사와 상의해야 합니다. 구체적인 용량이나 환자 상황을 알려주시면 더 맞춰서 설명드리겠습니다.

</details>

## q05 — Cinchocaine이랑 Pramipexole 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 31):** Cinchocaine may increase the sedative activities of Pramipexole.
- **Flash 추출 (채택):** (추출 없음)
- **자동 판정:** 실패
- 참고 — Sonnet 추출: Cinchocaine may increase the central nervous system depressant (CNS depressant) activities of Pramipexole.; The risk or severity of hypotension can be increased when Cinchocaine is combined with Pramipexole. (Flash와 다름)
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

# Cinchocaine(디부카인) ↔ Pramipexole 상호작용 예측

## 결론
**임상적으로 의미 있는 상호작용은 알려져 있지 않으며, 예측 위험도는 낮음(Low)입니다.** 아래는 알려진 데이터가 아니라 약리학적 특성에 근거한 추론입니다.

## 약물 특성 비교
| 항목 | Cinchocaine | Pramipexole |
|---|---|---|
| 분류 | 아마이드계 국소마취제 (Na⁺ 채널 차단) | 도파민 D2/D3 작용제 |
| 주 용도 | 치질 연고·좌제(주로 국소), 일부 척추마취 | 파킨슨병, 하지불안증후군 |
| 대사/배설 | 간 대사 | 대부분 신장에서 미변화체로 배설 (OCT2/MATE 수송체 관여), CYP 대사 거의 없음 |

## 가능한 상호작용 메커니즘

**1. 약동학적 (가능성 낮음)**
- Pramipexole은 CYP 대사를 거의 받지 않아 cinchocaine과의 CYP 경쟁 가능성이 낮습니다.
- 염기성 양이온성 약물인 cinchocaine이 신장 OCT2/MATE에서 pramipexole 분비를 약하게 경쟁할 수 있다는 이론은 있습니다. 그러나 국소 도포 시 전신 노출이 매우 적어 실제 의미는 거의 없을 것으로 보입니다.

**2. 약력학적 (상황에 따라 주의)**
- **저혈압:** pramipexole은 기립성 저혈압을 일으킬 수 있고, cinchocaine을 척추마취나 침윤마취로 쓰면 교감신경 차단으로 저혈압이 생길 수 있어 효과가 가산될 수 있습니다.
- **중추신경계:** pramipexole의 졸림이나 갑작스러운 수면 발작에, 전신 흡수된 국소마취제의 CNS 억제가 더해질 수 있습니다. 이는 과량이거나 점막 손상 부위에 넓게 도포한 경우에 해당합니다.
- **부정맥/QT:** 국소마취제 과량 시 심전도 영향이 가능하지만, pramipexole이 QT를 뚜렷하게 연장하지는 않아 의미 있는 상승효과는 예상되지 않습니다.

## 실무 권고
- 치질 연고·좌제 등 **국소 제형**은 용법대로 사용하면 병용에 큰 문제가 없습니다.
- **주사형(척추·침윤마취) 사용 시** 마취 전후 혈압 변화와 기립성 저혈압에 유의하세요.
- 신기능이 저하된 환자는 pramipexole 노출이 증가해 졸림과 저혈압이 심해질 수 있으므로 더 주의가 필요합니다.
- 어지러움, 심한 졸림, 입술 주위 저림, 이명, 맥박 이상이 나타나면 전신 흡수나 독성을 의심하고 의료진과 상의하세요.

실제 처방이나 복약 판단에는 Lexicomp, Micromedex, DrugBank 같은 상호작용 데이터베이스와 약사 확인을 함께 이용하시길 권합니다. 제형이나 환자 상황(신기능, 병용약)을 알려주시면 더 구체적으로 평가해 드릴게요.

</details>

## q06 — Azelastine이랑 Torasemide 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 28):** Azelastine may decrease the diuretic activities of Torasemide.
- **Flash 추출 (채택):** The risk or severity of QTc prolongation can be increased when Azelastine is combined with Torasemide.
- **자동 판정:** 실패
- 참고 — Sonnet 추출: The risk or severity of QTc prolongation can be increased when Azelastine is combined with Torasemide.; The risk or severity of hypotension can be increased when Azelastine is combined with Torasemide. (Flash와 다름)
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

## Azelastine + Torasemide 상호작용 예측

**결론: 임상적으로 유의한 상호작용 가능성은 낮음(경미~무시 가능)**

### 1. 약동학적 상호작용: 가능성 낮음
| 항목 | Azelastine | Torasemide |
|---|---|---|
| 분류 | 2세대 항히스타민제 (주로 비강 스프레이·점안액) | 루프 이뇨제 |
| 대사 | 간 CYP (3A4, 2D6 등)로 desmethylazelastine 생성 | 주로 CYP2C9 |
| 배설 | 주로 대변, 일부 신장 | 약 20~25% 신배설, 나머지 간대사 |

- 대사 경로가 거의 겹치지 않고, 서로 CYP를 강하게 억제하거나 유도한다는 근거도 없습니다.
- 비강·점안 제형은 전신 노출이 낮아 약동학적 상호작용 가능성은 더 낮습니다.

### 2. 약력학적 상호작용: 이론적·경미
1. **QT 연장 (이론적)**
   - Torasemide는 저칼륨혈증과 저마그네슘혈증을 유발할 수 있고, 이는 QT 연장과 부정맥의 위험 인자입니다.
   - Azelastine은 고용량 전신 노출 시 QT에 영향을 줄 가능성이 거론되지만, 일반적인 비강·점안 용량에서는 거의 문제가 되지 않습니다.
   - 따라서 위험은 낮지만, 심질환, 고령, 다른 QT 연장 약물 병용, 전해질 이상이 있으면 주의가 필요합니다.
2. **졸림·어지러움·저혈압 (가산 효과)**
   - Azelastine은 졸림과 어지러움을 일으킬 수 있고, torasemide는 체액 감소로 기립성 저혈압과 어지러움을 유발할 수 있습니다.
   - 특히 고령자에서 낙상 위험이 약간 증가할 수 있습니다.

### 3. 권고 사항
- 용량 조절은 일반적으로 필요하지 않습니다.
- 다음 경우에는 칼륨과 마그네슘 수치를 확인하고 필요하면 ECG를 고려하세요.
  - 심부전, 부정맥 병력
  - 다른 QT 연장 약물 병용 (macrolide, 항정신병약, 일부 항부정맥제 등)
  - 구토·설사, 고용량 이뇨제 사용
- 졸림이나 어지러움이 있으면 운전과 기계 조작에 주의하고, 알코올이나 다른 진정 작용 약물과의 병용을 피하세요.

> 이 내용은 약리학적 특성에 기반한 예측이며, 실제 처방 전에는 Lexicomp, Micromedex 등 상호작용 DB나 약사 확인을 권장합니다.

환자 특성(연령, 신기능, 병용약, azelastine 제형)을 알려주시면 더 구체적으로 평가해 드리겠습니다.

</details>

## q07 — Pantoprazole이랑 Methylphenidate 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 17):** Pantoprazole can cause an increase in the absorption of Methylphenidate resulting in an increased serum concentration and potentially a worsening of adverse effects.
- **Flash 추출 (채택):** (추출 없음)
- **자동 판정:** 실패
- 참고 — Sonnet 추출: (추출 없음)
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

## 요약
**임상적으로 의미 있는 상호작용 가능성은 낮음 (minor)**입니다. 일반적으로 병용 가능하며 용량 조절은 보통 필요하지 않습니다.

## 1. 약동학적 상호작용
| 항목 | Methylphenidate | Pantoprazole |
|---|---|---|
| 주 대사 | **CES1(carboxylesterase 1)** 가수분해 → ritalinic acid (비활성) | CYP2C19(주), CYP3A4(부) |
| CYP 관여 | 거의 없음 | 있음 |
| CYP 억제/유도 | 임상적으로 미미 | CYP2C19 약한 억제 |

- Methylphenidate는 CYP 의존도가 낮고, pantoprazole은 CES1에 영향을 주지 않습니다. 따라서 대사 경로의 충돌은 예상되지 않습니다.
- Pantoprazole은 CYP2C19 억제 효과가 약해 methylphenidate 혈중농도에 영향을 줄 가능성이 매우 낮습니다.

## 2. 이론적으로 고려할 점: 위 pH 상승과 제형 의존성
Pantoprazole은 위 pH를 올리므로 **pH 의존적 방출 제형**에서는 흡수 양상이 달라질 수 있습니다.

- **pH 의존적 방출 제형**: Ritalin LA, Metadate CD, Focalin XR(dexmethylphenidate) 등입니다. 일부 제품 라벨에는 "제산제나 위산분비억제제가 방출에 영향을 줄 수 있다"고 기재되어 있습니다. 방출이 빨라지거나 늦어질 수 있으나, 임상적 영향은 대체로 작거나 불확실합니다.
- **pH 비의존적 제형**: Concerta 같은 OROS 제형과 속방정은 영향이 거의 없을 것으로 예상됩니다. 한국에서 흔히 쓰는 Concerta는 이 범주입니다.

## 3. 약력학적 상호작용
- 중추신경계, 심혈관계에서 겹치는 작용은 없습니다.
- Methylphenidate는 식욕저하, 복통, 소화불량, 오심을 일으킬 수 있어, 위장 증상 때문에 PPI를 함께 쓰는 경우는 있습니다. 이는 약물 간 상호작용이 아니라 병용 이유입니다.

## 4. 실무 권고
- 기본적으로 **병용 가능**하며, 용량 조정은 필요 없습니다.
- pH 의존적 ER 제형을 쓴다면 효과 지속시간이나 반응이 달라지는지 관찰합니다. 예를 들어 오후 효과가 갑자기 줄거나 초반 반응이 과해지는지 확인합니다.
- 증상 변화가 있으면 제형을 바꾸거나(예: OROS) 복용 시간을 조정하는 방법을 고려할 수 있습니다.
- 위장 증상이 지속되면 methylphenidate를 식후에 복용하는 등의 조정도 도움이 됩니다.

※ 위 내용은 약리학적 근거에 기반한 예측이며, 실제 처방과 복용 조정은 담당 의사나 약사와 상의하세요. 사용 중인 methylphenidate 제품명과 pantoprazole 복용 목적을 알려주시면 더 구체적으로 설명드릴 수 있습니다.

</details>

## q08 — Bupranolol이랑 Vilanterol 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 13):** Bupranolol may decrease the bronchodilatory activities of Vilanterol.
- **Flash 추출 (채택):** Bupranolol may decrease the bronchodilatory activities of Vilanterol.
- **자동 판정:** 성공
- 참고 — Sonnet 추출: Bupranolol may decrease the bronchodilatory activities of Vilanterol.; Bupranolol may increase the bronchoconstrictory activities of Vilanterol. (Flash와 다름)
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

# Bupranolol + Vilanterol 상호작용 예측

## 1. 요약
| 항목 | 내용 |
|---|---|
| 상호작용 유형 | 약력학적 길항작용 (수용체 수준) |
| 예상 중증도 | **주의~중등도 이상 (Major에 가까움, 특히 천식·COPD 환자)** |
| 핵심 | 비선택적 β차단제가 vilanterol의 β2 작용을 차단 |

## 2. 약물 특성
- **Bupranolol**: 비선택적 β1/β2 차단제로, 내인성 교감신경 활성(ISA)이 없습니다. 막안정화 작용이 있고, 고혈압·협심증에 경구로, 녹내장에는 점안제로 쓰입니다.
- **Vilanterol**: 초장기 작용 β2 작용제(LABA)로, 흡입제(fluticasone furoate/vilanterol, umeclidinium/vilanterol 등)로 쓰입니다. CYP3A4와 P-gp의 기질입니다.

## 3. 예측되는 상호작용 기전
1. **β2 수용체 경쟁적 길항**
   - Bupranolol이 기관지 평활근의 β2 수용체를 차단해 vilanterol의 기관지 확장 효과가 감소합니다.
   - 반대로 β2 차단 때문에 기관지 수축이 유발될 수 있습니다.
2. **기관지 경련 위험 증가**
   - 천식이나 COPD 환자에서 급성 악화가 올 수 있습니다.
   - 구제 흡입제(SABA)의 반응도 떨어질 수 있습니다.
3. **심혈관계 효과 상쇄**
   - Vilanterol의 β1 관련 빈맥·심계항진 효과는 약해집니다.
   - 한편 β2 매개 혈관 확장이 차단되어 혈압이 변할 수 있습니다.
4. **대사 측면**
   - Bupranolol이 CYP3A4나 P-gp에 의미 있게 작용한다는 근거는 없어, 약동학적 상호작용 가능성은 낮습니다.
5. **기타**
   - β차단제는 저혈당 증상(떨림, 빈맥)을 가릴 수 있습니다.
   - Vilanterol로 인한 저칼륨혈증이나 QT 연장 효과와 β차단제의 부정맥 억제 효과가 복합적으로 나타날 수 있습니다.

## 4. 임상 관리 권고
- **가능하면 병용을 피합니다.** 특히 천식이나 기관지 과민성이 있는 환자는 피해야 합니다.
- β차단제가 꼭 필요하면 **심장선택적 β1 차단제(bisoprolol, nebivolol, metoprolol 등)**로 바꾸는 것을 고려합니다. 이 경우에도 저용량으로 시작하고 모니터링합니다.
- 점안액(녹내장)도 전신 흡수가 되므로 호흡기 질환자는 주의합니다. 필요하면 β1 선택적 제제(betaxolol)나 비-β차단제 계열(prostaglandin analog 등)을 고려합니다.
- 모니터링 항목: 호흡 증상, 폐기능(FEV1, PEF), 구제약 사용 빈도, 심박수, 혈압, 혈중 칼륨.
- 환자 교육: 숨가쁨, 쌕쌕거림, 흉부 압박감이 생기면 바로 보고하도록 합니다.

## 5. 한계
이 내용은 약리학적 기전에 근거한 **예측**입니다. Bupranolol과 vilanterol 병용에 대한 직접적인 임상 시험 자료는 제한적이므로, 실제 처방 시에는 Lexicomp, Micromedex 같은 상호작용 데이터베이스와 약사 및 전문의 상담을 통해 확인하세요.

</details>

## q09 — Estrone이랑 Glycerol phenylbutyrate 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 69):** The therapeutic efficacy of Glycerol phenylbutyrate can be decreased when used in combination with Estrone.
- **Flash 추출 (채택):** The metabolism of Estrone can be increased when combined with Glycerol phenylbutyrate.
- **자동 판정:** 실패
- 참고 — Sonnet 추출: The metabolism of Estrone can be increased when combined with Glycerol phenylbutyrate.
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

# Estrone × Glycerol phenylbutyrate 상호작용 예측

## 요약
- **예상 상호작용 수준**: 경미~중등도 (이론적·예측 수준)
- **주된 기전**: 약물동태학적 (CYP3A4 유도 가능성)
- 두 약물 간 직접적인 임상 연구나 확립된 상호작용 보고는 제가 알기로 없습니다. 아래는 약리학적 근거에 따른 추론입니다.

## 약물 특성
| 구분 | Estrone | Glycerol phenylbutyrate (GPB) |
|---|---|---|
| 용도 | 에스트로겐 (호르몬 요법 등) | 요소회로 이상증 환자의 고암모니아혈증 치료 (질소 결합제) |
| 대사 | CYP3A4, CYP1A2 등에 의한 수산화, 17β-HSD에 의한 estradiol 전환, 황산·글루쿠론산 포합 | 췌장 리파아제로 phenylbutyrate가 되고, β-산화를 거쳐 phenylacetate가 된 뒤 glutamine과 포합되어 phenylacetylglutamine으로 소변 배설 |

## 예상되는 상호작용

### 1. CYP3A4 유도 가능성 (가장 중요)
- GPB는 CYP3A4를 약하게 유도할 수 있습니다. 이는 midazolam 노출이 감소한 데이터에 근거하며, 제품 정보에도 CYP3A4 기질 약물의 효과 감소를 모니터링하라고 되어 있습니다.
- Estrone은 부분적으로 CYP3A4로 대사되므로 다음이 예상됩니다.
  - Estrone 및 estradiol 노출의 **경미한 감소**
  - 증상 조절 저하나 불규칙 출혈 가능성
  - 피임 목적으로 에스트로겐 제제를 쓰는 경우 피임 효과가 떨어질 수 있음

### 2. 흡수 및 배설 경로
- 흡수, 단백결합, 배설 경로가 겹치지 않아 **직접적인 경쟁 가능성은 낮습니다**.
- GPB는 췌장 리파아제로 가수분해되므로, 췌장 기능이 심하게 저하된 환자에서는 GPB 쪽의 효과가 달라질 수 있습니다. 이는 estrone과는 무관합니다.

### 3. 약력학적 고려
- 에스트로겐은 직접적인 고암모니아혈증 유발 약물은 아닙니다.
- 다만 간기능 변화, 체액 저류, 혈전 위험 같은 에스트로겐 고유의 이상반응은 기저질환(요소회로 이상증, 간질환 등)이 있는 환자에서 별도로 평가해야 합니다.

## 임상적 권고
1. 병용은 일반적으로 **금기가 아니며**, 필요하면 병용 가능합니다.
2. 에스트로겐 반응(증상, 출혈 양상)을 모니터링하고, 필요하면 estradiol 혈중 농도를 확인합니다.
3. 피임 목적이라면 비호르몬 방법을 병행하거나 대체하는 것을 고려합니다.
4. GPB 투여 중 **혈중 암모니아 수치**는 평소대로 추적합니다.
5. 간기능과 혈전 위험인자를 함께 평가합니다.

※ 이 내용은 약리학적 추론에 기반한 예측이므로, 실제 처방 시에는 최신 약물 정보(Lexicomp, Micromedex, 제품 라벨)를 확인하고 약사나 담당 의사와 상의하시기 바랍니다.

</details>

## q10 — Protocatechualdehyde이랑 Mestranol 상호작용 예측해줘

- **정답 문장 (질문 순서, 모델 1위 관계 11):** Mestranol may decrease the anticoagulant activities of Protocatechualdehyde.
- **Flash 추출 (채택):** (추출 없음)
- **자동 판정:** 실패
- 참고 — Sonnet 추출: (추출 없음)
- **사람 판정:** [ ]

<details><summary>A의 답 전문</summary>

# Protocatechualdehyde × Mestranol 상호작용 예측

**결론 요약:** 두 물질 간에 문서화된 임상적 상호작용은 없습니다. 아래 내용은 구조와 대사 경로에 근거한 이론적 추정이며, 임상적 위험도는 낮거나 불확실한 수준으로 봅니다.

## 1. 각 물질의 특징
| | Protocatechualdehyde (3,4-dihydroxybenzaldehyde) | Mestranol |
|---|---|---|
| 성격 | 카테콜 구조의 페놀성 알데하이드. 단삼(*Salvia miltiorrhiza*) 등 식물 유래 | 에티닐에스트라디올(EE)의 3-methyl ether 전구약물 |
| 주요 작용 | 항산화, 항혈소판, 혈관보호 | 에스트로겐 작용 (ER 작용제) |
| 대사 | 산화로 protocatechuic acid 생성, COMT 메틸화, 포합(glucuronide/sulfate) | CYP2C9 등에 의한 O-탈메틸화로 EE 생성. 이후 CYP3A4 수산화, SULT·UGT 포합, COMT 메틸화 |

## 2. 예상되는 상호작용 기전

**① 약동학적 (가능성 낮음~중간 이하)**
- **CYP2C9 경쟁/억제:** Mestranol이 활성형 EE로 바뀌려면 탈메틸화가 필요합니다. Protocatechualdehyde가 CYP2C9를 유의하게 억제한다면 활성화가 약간 줄 수 있습니다. 다만 이 물질 자체의 CYP 억제는 약한 것으로 알려져 있고, 단삼의 tanshinone류가 더 강한 CYP 억제 성분입니다.
- **포합 경쟁 (SULT1E1, UGT1A1):** 페놀성 화합물은 EE의 황산/글루쿠론산 포합과 경쟁해 EE 노출을 약간 높일 수 있습니다. 이론적으로는 가능하지만 용량 의존적이며 임상적 의미는 불분명합니다.
- **COMT 경쟁:** 카테콜인 protocatechualdehyde와 EE의 카테콜 대사체(2-OH-EE)가 COMT를 두고 경쟁할 수 있습니다. 영향은 미미할 것으로 예상합니다.

**② 약력학적 (가장 현실적인 쟁점)**
- Mestranol/EE는 응고인자를 증가시켜 혈전 위험을 높입니다. Protocatechualdehyde는 항혈소판·항혈전 효과가 보고되어 있어 **작용 방향이 반대**입니다. 효과 상쇄 또는 부분 보호 가능성이 있으나, 항응고제처럼 출혈 위험이 커지는 수준은 아닐 것입니다.
- 항산화 작용으로 에스트로겐 카테콜 대사체의 산화(퀴논 형성)를 줄일 가능성은 가설 수준입니다.
- ER에 직접 결합하는 활성은 뚜렷하게 보고되어 있지 않아, 에스트로겐 효과를 직접 상승시키거나 길항할 가능성은 낮습니다.

## 3. 위험도 평가
| 항목 | 예측 |
|---|---|
| 임상적 중요도 | 낮음 (근거 부족) |
| 가장 가능성 있는 방향 | 대사 경쟁에 의한 경미한 EE 노출 변화 |
| 주의 상황 | 고용량 보충제나 단삼 추출물 병용 시 (tanshinone 등 다른 성분의 영향이 더 큼) |

## 4. 검증하려면
- **In vitro:** 사람 간 마이크로솜에서 mestranol→EE 전환 시 CYP2C9 억제 (IC50). SULT1E1/UGT1A1 억제 시험
- **세포 실험:** ER 리포터 assay (MCF-7, ERE-luc)에서 병용 효과
- **In silico:** CYP2C9, SULT1E1에 대한 docking과 PBPK 모델링
- **기능 평가:** 혈소판 응집이나 트롬빈 생성 assay로 약력학 평가

이 예측은 문헌에 직접 근거가 없는 추론입니다. 실제 복용이나 임상 판단이 목적이라면 약사나 의사와 상의하세요. 연구 목적이라면 어떤 방식(in silico, in vitro 등)으로 진행하시는지 알려주시면 더 구체적으로 도와드리겠습니다.

</details>
