"""git 관리 상태 확인. 실행: python3 tests/layout/layout_git.py

범위
- 새 실행 원자료 eval_outputs/ 는 git 에서 빠지고, 공개 원자료 results/v2/raw/ 는 git 에 올라가 있다
- .gitignore 에 없는 파일을 가리키는 항목, 중복 규칙이 없다
- 캐시 파일이 git 에 없다
- 고정 패키지 목록에 이 컴퓨터에만 있는 경로가 없다
"""
import os
import re

from _common import check, finish, git, path

# 1. 원자료
check('eval_outputs/ 는 git 에서 빠짐', git('check-ignore', 'eval_outputs/x').strip() != '')
check('eval_outputs/ 아래 git 파일 없음', git('ls-files', 'eval_outputs').strip() == '')
check('results/v2/raw/ 가 git 에 있음', git('ls-files', 'results/v2/raw').strip() != '')

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
