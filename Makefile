# 이미지 빌드, 검증, 실행. 각 대상의 명령은 README 와 .claude/rules/verification.md 와 같다.
#   make images        런타임 이미지 두 개 빌드
#   make check         검증 전부 (구조, 도구, 런타임, 채점)
#   make try TASK=...  한 질문 실행 (CONDITION=B|C, 기본 C)
#   make eval          B·C 10문항 실행 후 채점 (eval_outputs/ddi/)

PY  := .venv-openhands/bin/python
SRV := ddi-srv
CONDITION ?= C
TASK ?= Warfarin이랑 Aspirin 상호작용 예측해줘

.PHONY: images venv check test-layout test-tools test-runtime test-score try eval rescore

images:
	docker build -f ddi-runtime/Dockerfile -t ddi-runtime .
	docker build -f ddi-runtime/Dockerfile.specialist -t ddi-specialist .

venv:
	python3.12 -m venv .venv-openhands
	.venv-openhands/bin/pip install -r ddi-agent/requirements.lock.txt

check: test-layout test-tools test-runtime test-score

# 폴더·파일 이름, 경로, 문서
test-layout:
	python3 tests/layout/layout_structure.py
	python3 tests/layout/layout_paths.py
	python3 tests/layout/layout_git.py

# ddi-tools/: 원 모델과 확률 일치, 경계 입력, ddi 공개 함수 (서버 컨테이너를 띄웠다가 지운다)
test-tools:
	docker run --rm --gpus all -v $(CURDIR):/w:ro ddi-runtime python /w/tests/tools/check_original.py
	docker rm -f $(SRV) > /dev/null 2>&1 || true
	docker run -d --gpus all -v $(CURDIR):/w:ro --name $(SRV) ddi-specialist > /dev/null
	until docker exec $(SRV) curl -sf http://127.0.0.1:8765/health > /dev/null 2>&1; do sleep 2; done
	docker exec -w /opt/DSN-DDI $(SRV) python /w/tests/tools/check_edges.py; s1=$$?; \
	docker run --rm --network container:$(SRV) -v $(CURDIR):/w -w /w python:3.11 python tests/tools/check_ddi.py; s2=$$?; \
	docker rm -f $(SRV) > /dev/null; [ $$s1 -eq 0 ] && [ $$s2 -eq 0 ]

# ddi-agent/, ddi-runtime/ (LLM 없이 런타임만)
test-runtime:
	$(PY) tests/runtime/check_runtime.py --condition B --out eval_outputs/scratch/check_B
	$(PY) tests/runtime/check_runtime.py --condition C --out eval_outputs/scratch/check_C

# 채점 코드: 공개한 v2 채점이 그대로 나오는지
test-score: rescore
	git diff --exit-code -- eval_outputs/v2

try:
	$(PY) ddi-agent/run_agent.py --condition $(CONDITION) --task-suffix benchmarks/ddi/prompts/task_suffix.txt \
	    --task "$(TASK)" --out eval_outputs/try_$(CONDITION)_$$(date +%Y%m%d_%H%M%S_%N)

eval:
	bash benchmarks/ddi/scripts/run_eval.sh

rescore:
	python3 benchmarks/ddi/eval_infer.py
