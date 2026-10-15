"""DSN-DDI 관계 번호 → 설명 문장 규칙을 SSI-DDI 데이터와 독립적으로 대조한다.

규칙 (ddi/relations.py, make_ground_truth.py가 쓰는 것):
  DSN-DDI 번호 t → Interaction_information.csv에서 `Interaction type == t + 1` 인 행,
  그 행의 Subject == 2 이면 약물 순서를 뒤집는다.

이 스크립트는 규칙을 쓰지 않고, 두 데이터셋에 함께 있는 약물 쌍만으로 대응을 만든 뒤
규칙과 비교한다.
  - DSN-DDI 번호 t마다, 같은 쌍의 SSI-DDI 번호 s 중 가장 많은 것(s*)과 그 비율 (번호 일치율)
  - s*인 쌍 중 약물 순서가 DSN-DDI와 같은/반대인 비율, 많은 쪽의 비율 (방향 일치율)
  - s*의 설명 행(`DDI type {s*+1}`)이 규칙의 행(`Interaction type == t+1`)과 같은지
  - 많은 쪽 방향이 그 행의 Subject와 맞는지 (2 → 반대, 1·3 → 같음)

입력 (모두 인자로 받음)
  --dsn  DSN-DDI 데이터 drugbank/ddis.csv (d1,d2,type)
  --ssi  SSI-DDI data/ddis.csv (d1,d2,type), github.com/kanz76/SSI-DDI
  --info SSI-DDI data/Interaction_information.csv (= ddi/data/Interaction_information.csv)
출력: --out 대응표 CSV, 같은 이름의 .json 요약
"""
import argparse
import csv
import json
from collections import Counter, defaultdict


def read_pairs(path):
    with open(path, newline="") as f:
        return [(r["d1"], r["d2"], int(r["type"])) for r in csv.DictReader(f)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", required=True)
    ap.add_argument("--ssi", required=True)
    ap.add_argument("--info", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.info, newline="") as f:
        info = list(csv.DictReader(f))
    by_itype = {int(r["Interaction type"]): r for r in info}
    by_ddit = {int(r["DDI type"].split()[-1]): r for r in info}

    # SSI-DDI 쌍: 순서 없는 키 → [(d1, d2, s)]
    ssi = defaultdict(list)
    for d1, d2, s in read_pairs(args.ssi):
        ssi[frozenset((d1, d2))].append((d1, d2, s))

    dsn = read_pairs(args.dsn)
    n_pairs = Counter(t for _, _, t in dsn)
    # 한 쌍에 관계가 여러 개인 쌍(두 데이터 모두 406쌍)은 어느 관계끼리 대응하는지 알 수 없어 뺀다
    n_dsn_key = Counter(frozenset((d1, d2)) for d1, d2, _ in dsn)
    s_counts = defaultdict(Counter)          # t → Counter(s)
    orient = defaultdict(lambda: defaultdict(Counter))  # t → s → Counter(same/reversed)
    for d1, d2, t in dsn:
        key = frozenset((d1, d2))
        if n_dsn_key[key] != 1 or len(ssi.get(key, [])) != 1:
            continue
        e1, e2, s = ssi[key][0]
        s_counts[t][s] += 1
        orient[t][s]["same" if (e1, e2) == (d1, d2) else "reversed"] += 1

    rows = []
    for t in sorted(n_pairs):
        s_star, n_star = s_counts[t].most_common(1)[0]
        matched = sum(s_counts[t].values())
        o = orient[t][s_star]
        dom, n_dom = o.most_common(1)[0]
        rule_row = by_itype[t + 1]
        data_row = by_ddit[s_star + 1]
        subject = int(rule_row["Subject"])
        rows.append({
            "dsn_type": t,
            "interaction_type": t + 1,
            "ssi_type": s_star,
            "subject": subject,
            "n_dsn_pairs": n_pairs[t],
            "n_matched": matched,
            "type_agreement": round(n_star / matched, 4),
            "orientation": dom,
            "orientation_agreement": round(n_dom / n_star, 4),
            "row_matches_rule": data_row is rule_row,
            "orientation_matches_subject": dom == ("reversed" if subject == 2 else "same"),
            "description": rule_row["Description"],
        })

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    s_used = [r["ssi_type"] for r in rows]
    summary = {
        "n_relations": len(rows),
        "one_to_one": len(set(s_used)) == len(rows),
        "min_type_agreement": min(r["type_agreement"] for r in rows),
        "min_orientation_agreement": min(r["orientation_agreement"] for r in rows),
        "rule_row_matches": sum(r["row_matches_rule"] for r in rows),
        "orientation_matches_subject": sum(r["orientation_matches_subject"] for r in rows),
        "subject_counts": dict(Counter(r["subject"] for r in rows)),
        "matched_pairs": sum(r["n_matched"] for r in rows),
        "dsn_pairs": len(dsn),
    }
    with open(args.out.rsplit(".", 1)[0] + ".json", "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
