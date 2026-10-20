"""폴더 구조 확인 스크립트들이 같이 쓰는 도구."""
import os
import re
import subprocess

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# 옛 경로가 남아 있어도 되는 곳: 기록(실행 원자료, git 에 없는 실행 출력), 외부 코드, 논문(별도 관리)
_SKIP_DIRS = {'.git', '.venv-openhands', 'third_party', 'paper', '__pycache__'}
# 구조 확인 스크립트는 옛 경로를 검사 문자열로 가지므로 제외
_SKIP_PREFIXES = (os.path.join('eval_outputs', 'v1', 'raw'),
                  os.path.join('eval_outputs', 'v2', 'raw'), os.path.join('eval_outputs', 'ddi'),
                  os.path.join('eval_outputs', 'scratch'),
                  os.path.join('tests', 'layout'))
_TEXT_EXT = ('.py', '.md', '.txt', '.toml', '.j2', '.sh', '.yaml', '.yml', '.json', '.jsonl')

ok = True


def check(name, cond, detail=''):
    global ok
    ok &= bool(cond)
    print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, detail))


def finish():
    print('\n전체: %s' % ('OK' if ok else 'FAIL'))
    raise SystemExit(0 if ok else 1)


def path(*parts):
    return os.path.join(REPO, *parts)


def live_files():
    """현재 쓰는 문서·코드 파일 (기록·외부 코드 제외)."""
    for root, dirs, files in os.walk(REPO):
        rel = os.path.relpath(root, REPO)
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS
                   and not os.path.normpath(os.path.join(rel, d)).startswith(_SKIP_PREFIXES)]
        for f in files:
            if os.path.normpath(os.path.join(rel, f)).startswith(_SKIP_PREFIXES):
                continue
            if f.endswith(_TEXT_EXT) or f.startswith('Dockerfile'):
                yield os.path.join(root, f)


def find_refs(needle, regex=False):
    """needle(regex=True 면 정규식)이 나오는 '파일:줄' 목록."""
    match = re.compile(needle).search if regex else (lambda line: needle in line)
    hits = []
    for fp in live_files():
        try:
            with open(fp, encoding='utf-8') as fh:
                for i, line in enumerate(fh, 1):
                    if match(line):
                        hits.append('%s:%d' % (os.path.relpath(fp, REPO), i))
        except UnicodeDecodeError:
            pass
    return hits


def git(*args):
    return subprocess.run(['git', '-C', REPO, *args], capture_output=True, text=True).stdout
