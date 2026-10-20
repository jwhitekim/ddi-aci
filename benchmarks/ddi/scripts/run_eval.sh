#!/bin/bash
# B·C 10문항 실행 후 채점 (터미널 세션과 분리해 nohup 으로 돌려도 됨). 저장소 어디서든 실행 가능:
#   nohup bash benchmarks/ddi/scripts/run_eval.sh &
# 원자료: eval_outputs/ddi/{B,C}/, 실행 기록: eval_outputs/ddi/logs/, 채점: eval_outputs/ddi/scores/
P=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=$P/eval_outputs/ddi
LOGS=$OUT/logs
LOG=$LOGS/orchestrate.log
cd "$P"
mkdir -p "$LOGS"
docker ps -aq --filter name=openhands-runtime | xargs -r docker rm -f > /dev/null 2>&1
echo "$(date '+%H:%M') 평가 시작" >> "$LOG"
.venv-openhands/bin/python benchmarks/ddi/run_infer.py --condition C --workers 1 --output-dir "$OUT" > "$LOGS/batch_C.log" 2>&1 &
.venv-openhands/bin/python benchmarks/ddi/run_infer.py --condition B --workers 2 --output-dir "$OUT" > "$LOGS/batch_B.log" 2>&1 &
wait
echo "$(date '+%H:%M') 평가 끝, 채점 시작" >> "$LOG"
python3 benchmarks/ddi/eval_infer.py --runs-dir "$OUT" --out "$OUT/scores" > "$LOGS/score_output.txt" 2>&1
echo "done $(date '+%m-%d %H:%M')" >> "$LOGS/score_output.txt"
echo "$(date '+%H:%M') 완료" >> "$LOG"
