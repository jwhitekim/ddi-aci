"""git 관리 상태 확인. 실행: python3 tests/layout/layout_git.py

범위
- eval_outputs/ 에서 공개한 평가 v1/, v2/ 만 git 에 있고, 새 실행(ddi/)·시험 실행(scratch/)은 빠진다
- .gitignore 에 없는 파일을 가리키는 항목, 중복 규칙이 없다
- 캐시 파일이 git 에 없다
- 고정 패키지 목록에 이 컴퓨터에만 있는 경로가 없다
"""
import os
import re

from _common import check, finish, git, path

# 1. 원자료
for d in ('ddi', 'scratch', 'x'):
    check('eval_outputs/%s/ 는 git 에서 빠짐' % d, git('check-ignore', 'eval_outputs/%s/f' % d).strip() != '')
tracked = set(f.split('/')[1] for f in git('ls-files', 'eval_outputs').split())
check('eval_outputs/ 아래 git 파일은 v1/, v2/ 만', tracked == {'v1', 'v2'}, tracked)
for v in ('v1', 'v2'):
    check('eval_outputs/%s/raw/ 가 git 에 있음' % v, git('ls-files', 'eval_outputs/%s/raw' % v).strip() != '')

# 2. .gitignore
rules = [l.strip() for l in open(path('.gitignore'), encoding='utf-8') if l.strip() and not l.startswith('#')]
literal = [r for r in rules if '.' in r and not r.startswith('!') and not any(c in r for c in '*?[')
           and not r.endswith('/')]
stale = [r for r in literal if not os.path.exists(path(r.lstrip('/')))]
check('.gitignore 에 없는 파일을 가리키는 항목 없음', not stale, stale)
check('규칙 중복 없음', len(rules) == len(set(rules)), rules)

# 3. 캐시 파일
cached = [f for f in git('ls-files').split() if '__pycache__' in f or f.endswith('.pyc')]
check('캐시 파일이 git 에 없음', not cached, cached)

# 4. 고정 패키지 목록
lock = open(path('ddi-agent', 'requirements.lock.txt'), encoding='utf-8').read().splitlines()
local = [l for l in lock if 'file://' in l or re.search(r'(^|\s)/(home|Users)/', l)]
check('requirements.lock.txt 에 로컬 경로 없음', not local, local)

finish()
