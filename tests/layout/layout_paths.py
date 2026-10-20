"""코드·문서의 경로가 새 구조와 맞는지 확인. 실행: python3 tests/layout/layout_paths.py

범위
- 파이썬 코드가 만드는 저장소 경로(REPO, BENCH, AGENT_DIR 등 / '...')가 실제로 있다 (eval_outputs 아래 출력 경로 제외)
- 확인 스크립트가 sys.path 에 넣는 폴더에 불러올 코드가 있다
- Docker 이미지가 복사하는 파일, 일괄 실행 스크립트가 부르는 파일이 있다
- 확인 스크립트(check_*.py)는 tests/ 아래에만 있다
- 현재 쓰는 문서·코드에 옛 경로가 남지 않는다
"""
import os
import re
from pathlib import Path

from _common import REPO, check, find_refs, finish, path

BASES = {'REPO': '', 'BENCH': 'benchmarks/ddi', 'RESULTS': 'results', 'AGENT_DIR': 'ddi-agent',
         'DDI_DIR': 'ddi-tools/ddi', 'SERVER_DIR': 'ddi-tools/server',
         'MICROAGENT': 'ddi-tools/microagent/ddi.md'}
PY = [os.path.join(r, f) for d in ('ddi-agent', 'benchmarks', 'tests/tools', 'tests/workspace', 'ddi-tools')
      for r, _, fs in os.walk(path(d)) for f in fs if f.endswith('.py')]

# 1. REPO / '...' 경로
for fp in PY:
    src = open(fp, encoding='utf-8').read()
    names = '|'.join(BASES)
    for base, parts in re.findall(r"\b(" + names + r")((?:\s*/\s*'[^'%]+')+)", src):
        rel = os.path.join(BASES[base], *re.findall(r"'([^']+)'", parts))
        if rel.startswith('eval_outputs'):
            continue
        check('%s → %s 있음' % (os.path.relpath(fp, REPO), rel), os.path.exists(path(rel)))

# 2. sys.path 에 넣는 폴더
NEEDS = {'check_ddi.py': 'ddi/__init__.py', 'check_edges.py': 'predictor.py', 'check_original.py': 'predictor.py',
         'check_runtime.py': 'run_agent.py', 'run_baseline_a.py': 'eval_infer.py'}
for fp in PY:
    name = os.path.basename(fp)
    if name not in NEEDS:
        continue
    m = re.search(r'sys\.path\.insert\(0,\s*(.+)\)\s*$', open(fp, encoding='utf-8').read(), re.M)
    env = {'os': os, 'Path': Path, '__file__': fp, 'str': str,
           'REPO': Path(REPO), 'BENCH': Path(path('benchmarks', 'ddi'))}
    inserted = str(eval(m.group(1), env)) if m else ''
    check('%s 가 %s 를 찾음' % (name, NEEDS[name]), os.path.isfile(os.path.join(inserted, NEEDS[name])), inserted)

# 3. Docker 복사 대상, 일괄 실행 스크립트
for df in ('Dockerfile', 'Dockerfile.specialist'):
    for src in re.findall(r'^COPY\s+(.+?)\s+\S+$', open(path('ddi-runtime', df)).read(), re.M):
        for s in src.split():
            check('%s 복사 대상 %s 있음' % (df, s), os.path.exists(path(s)))
sh = open(path('benchmarks', 'ddi', 'scripts', 'run_eval.sh'), encoding='utf-8').read()
check('run_eval.sh 에 절대 경로 없음', not re.findall(r'/(?:home|Users)/\S+', sh))
for ref in sorted(set(re.findall(r'\b(benchmarks/[\w./-]+\.py)\b', sh))):
    check('run_eval.sh → %s 있음' % ref, os.path.isfile(path(ref)))

# 4. check_*.py 위치
stray = [os.path.relpath(os.path.join(r, f), REPO)
         for r, _, fs in os.walk(REPO)
         for f in fs if f.startswith('check_') and f.endswith('.py')
         and not os.path.relpath(r, REPO).startswith(('tests', '.git', '.venv-openhands', 'third_party', 'paper',
                                                      'eval_outputs', 'openspec'))]
check('check_*.py 는 tests/ 아래에만', not stray, stray)

# 5. 옛 경로 참조 (앞에 / . - 글자가 없는 옛 최상위 폴더)
OLD = r'(?<![\w/.-])(?:eval|runs|agent|agent_pkg|agent-pkg|agent-server|docker|tool|server|ddi)/(?!\*)'
refs = [r for r in find_refs(OLD, regex=True)]
check('옛 최상위 폴더 경로 참조 없음', not refs, refs)
for old in ('oh_main', 'ddi-workspace', 'c_workspace', 'benchmarks/ddi/agent', "REPO / 'eval'", "REPO / 'runs'", r'(?<![\w/])Drug-Interaction-Research'):
    refs = find_refs(old, regex=True)
    check('옛 이름 %s 참조 없음' % old, not refs, refs)

finish()
