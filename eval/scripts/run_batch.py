"""평가 질문을 B 또는 C 조건으로 실행한다 (문항마다 agent/run_agent.py 호출).

    .venv-openhands/bin/python eval/scripts/run_batch.py --condition B --workers 2

결과: runs/eval/<조건>/<qid>/ (이미 있는 문항은 건너뜀)
"""
import argparse
import json
import os
import signal
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TIMEOUT_SECONDS = 20 * 60


def run_one(condition, q):
    out = REPO / 'runs' / 'eval' / condition / q['qid']
    if out.exists():
        return q['qid'], 'skip'
    cmd = [sys.executable, str(REPO / 'agent' / 'run_agent.py'), '--condition', condition,
           '--task', q['question'], '--out', str(out)]
    # 문항마다 새 프로세스 그룹으로 실행해, 시간 초과 시 OpenHands·빌드 등 하위 프로세스까지 함께 정리한다
    proc = subprocess.Popen(cmd, cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    try:
        proc.wait(timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
        out.mkdir(parents=True, exist_ok=True)
        (out / 'TIMEOUT').write_text('timeout after %d s\n' % TIMEOUT_SECONDS)
        return q['qid'], 'timeout'
    info = out / 'run_info.json'
    return q['qid'], json.loads(info.read_text()).get('status') if info.exists() else 'no_run_info'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--condition', choices=['B', 'C'], required=True)
    p.add_argument('--workers', type=int, default=1)
    args = p.parse_args()
    questions = [json.loads(l) for l in open(REPO / 'eval' / 'questions' / 'questions.jsonl', encoding='utf-8')]
    with ThreadPoolExecutor(args.workers) as pool:
        for qid, status in pool.map(lambda q: run_one(args.condition, q), questions):
            print(args.condition, qid, status, flush=True)


if __name__ == '__main__':
    main()
