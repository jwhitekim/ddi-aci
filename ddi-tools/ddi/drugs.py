"""약물 식별: 이름·동의어·DrugBank ID·SMILES -> 표준 약물 정보."""
import csv
import os
import re

from .server import _post

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
_ID_RE = re.compile(r'^DB\d{5}$', re.IGNORECASE)


def _load():
    names, by_common, by_synonym = {}, {}, {}
    with open(os.path.join(_DATA, 'dbvocab.csv'), encoding='utf-8') as f:
        for row in csv.DictReader(f):
            dbid, common = row['DrugBank ID'], row['Common name'].strip()
            names[dbid] = common
            by_common.setdefault(common.lower(), set()).add(dbid)
            for syn in (row['Synonyms'] or '').split(' | '):
                if syn.strip():
                    by_synonym.setdefault(syn.strip().lower(), set()).add(dbid)
    with open(os.path.join(_DATA, 'dsn_drugs.txt')) as f:
        dsn = {line.strip() for line in f if line.strip()}
    return names, by_common, by_synonym, dsn


_NAMES, _BY_COMMON, _BY_SYNONYM, _DSN = _load()


def resolve_drug(x):
    """약물 표기를 표준 약물로 바꾼다. 모르는 약물이면 ValueError.

    반환: {'drugbank_id', 'name', 'smiles', 'is_new', 'in_dsn'}
    """
    text = str(x).strip()
    if _ID_RE.match(text):
        dbid = text.upper()
        if dbid not in _DSN:
            raise ValueError('%s은(는) DSN-DDI 데이터에 없는 약물이라 예측할 수 없습니다.' % dbid)
        return {'drugbank_id': dbid, 'name': _NAMES.get(dbid, dbid), 'smiles': None, 'is_new': False, 'in_dsn': True}

    key = text.lower()
    matches = _BY_COMMON.get(key) or _BY_SYNONYM.get(key) or set()
    if matches:
        in_dsn = sorted(m for m in matches if m in _DSN)
        if not in_dsn:
            raise ValueError('%r(%s)은(는) DSN-DDI 데이터에 없는 약물이라 예측할 수 없습니다.'
                             % (text, ', '.join(sorted(matches))))
        if len(in_dsn) > 1:
            cands = ', '.join('%s (%s)' % (m, _NAMES[m]) for m in in_dsn)
            raise ValueError('%r에 해당하는 약물이 여러 개입니다: %s. DrugBank ID로 지정하세요.' % (text, cands))
        dbid = in_dsn[0]
        return {'drugbank_id': dbid, 'name': _NAMES[dbid], 'smiles': None, 'is_new': False, 'in_dsn': True}

    if _post('/check_smiles', {'smiles': text}).get('valid'):
        return {'drugbank_id': None, 'name': 'the query compound', 'smiles': text, 'is_new': True, 'in_dsn': False}
    raise ValueError('%r을(를) 약물 이름, DrugBank ID, SMILES 어느 것으로도 찾을 수 없습니다.' % text)


def _label(x):
    """explain 에 넣을 약물 이름. DrugBank ID 면 대표 이름으로 바꾼다."""
    text = str(x).strip()
    return _NAMES.get(text.upper(), text) if _ID_RE.match(text) else text


def _key(drug):
    return drug['drugbank_id'] or drug['smiles']


def _payload(drug):
    return drug['drugbank_id'] if drug['drugbank_id'] else {'smiles': drug['smiles']}
