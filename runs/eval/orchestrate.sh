#!/bin/bash
# v2: B·C 10문항 재실행 후 채점 (Claude Code 세션과 분리, 맥북을 닫아도 진행). 이미지는 v1 때 만든 것을 그대로 씀
P=/home/prml/workspace/ddi-agent
LOG=$P/runs/eval/orchestrate.log
cd $P
docker ps -aq --filter name=openhands-runtime | xargs -r docker rm -f > /dev/null 2>&1
echo "$(date '+%H:%M') v2 평가 시작" >> $LOG
.venv-openhands/bin/python eval/run_batch.py --condition C --workers 1 > runs/eval/batch_C.log 2>&1 &
.venv-openhands/bin/python eval/run_batch.py --condition B --workers 2 > runs/eval/batch_B.log 2>&1 &
wait
echo "$(date '+%H:%M') 평가 끝, 채점 시작" >> $LOG
python3 eval/score.py > runs/eval/score_output.txt 2>&1
echo "done $(date '+%m-%d %H:%M')" >> runs/eval/score_output.txt
echo "$(date '+%H:%M') 완료" >> $LOG
