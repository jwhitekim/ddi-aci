"""결과 저장: 채점용 CSV."""
import csv

from .drugs import _key

CSV_COLUMNS = ['drug_a', 'drug_b', 'relation', 'prob', 'model_used', 'description']


def _rows_for_csv(results):
    if isinstance(results, dict) and 'top' in results:  # predict() 결과: 상위 관계마다 한 행
        a, b = _key(results['drug_a']), _key(results['drug_b'])
        return [{'drug_a': a, 'drug_b': b, 'relation': t['relation'], 'prob': t['prob'],
                 'model_used': results['model_used'], 'description': t['description']} for t in results['top']]
    if hasattr(results, 'to_dict'):  # DataFrame
        results = results.to_dict('records')
    return [{c: r.get(c) for c in CSV_COLUMNS} for r in results]


def save_results(results, path):
    """predict / predict_many 결과(또는 같은 칼럼의 표)를 채점용 CSV로 저장하고 경로를 돌려준다."""
    rows = _rows_for_csv(results)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow({c: ('' if r[c] is None or r[c] != r[c] else r[c]) for c in CSV_COLUMNS})
    return path
