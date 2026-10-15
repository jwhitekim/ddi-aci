# DSN-DDI 관계 번호 → 설명 문장 규칙 검증

`eval/scripts/verify_relation_map.py`가 만든 결과. 규칙(`Interaction type == t + 1`, Subject 2면 순서 반대)을 쓰지 않고, DSN-DDI와 SSI-DDI에 함께 있는 약물 쌍만으로 대응을 만든 뒤 규칙과 비교한다.

- `dsn_relation_map.csv`: 관계 86종마다 대응한 SSI-DDI 번호, 번호·방향 일치율, 규칙과 같은지
- `dsn_relation_map.json`: 요약 (86종 1:1, 번호·방향 일치율 최소 100%, 규칙 행 86/86, Subject와 방향 86/86)

입력

| 인자 | 파일 | 출처 |
| --- | --- | --- |
| `--dsn` | DSN-DDI `drugbank/ddis.csv` (sha256 `40d5e743…6d01f50`) | `DSN-DDI-dataset.zip` (LFS) |
| `--ssi` | SSI-DDI `data/ddis.csv` (sha256 `e177db20…3d12ca1`) | github.com/kanz76/SSI-DDI 커밋 `23e958f` |
| `--info` | `ddi/data/Interaction_information.csv` | SSI-DDI `data/Interaction_information.csv`와 같은 파일 |

한 쌍에 관계가 여러 개인 쌍(두 데이터 모두 406쌍)은 대응을 정할 수 없어 뺐다. 대조한 쌍은 190,856쌍(DSN-DDI 191,808쌍 중).

```
python3 eval/scripts/verify_relation_map.py --dsn <DSN-DDI ddis.csv> --ssi <SSI-DDI ddis.csv> \
  --info ddi/data/Interaction_information.csv --out eval/relation_map/dsn_relation_map.csv
```
