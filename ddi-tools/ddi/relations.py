"""DSN-DDI 관계 번호 -> 방향이 반영된 문장."""
import csv
import os

from .drugs import _DATA, _label

N_RELATIONS = 86


def _load():
    relations = {}
    with open(os.path.join(_DATA, 'Interaction_information.csv'), encoding='utf-8') as f:
        for row in csv.DictReader(f):
            relations[int(row['Interaction type'])] = (row['Description'], int(row['Subject']))
    return relations


_RELATIONS = _load()


def explain(rel, a, b):
    """DSN-DDI 관계 번호 rel (0~85) 를 (a, b) 쌍의 문장으로 바꾼다.

    DSN-DDI 번호 t 는 설명 파일의 Interaction type == t + 1 행에 대응하고,
    그 행의 Subject 가 2 이면 #Drug1 에 b, #Drug2 에 a 가 들어간다 (86종 중 42종).
    """
    rel = int(rel)
    if not 0 <= rel < N_RELATIONS:
        raise ValueError('관계 번호는 0~85 사이여야 합니다: %d' % rel)
    template, subject = _RELATIONS[rel + 1]
    d1, d2 = (_label(b), _label(a)) if subject == 2 else (_label(a), _label(b))
    return template.replace('#Drug1', d1).replace('#Drug2', d2)
