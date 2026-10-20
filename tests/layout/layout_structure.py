"""루트 구조 확인. 실행: python3 tests/layout/layout_structure.py

목표 구조 (benchmarks/ddi/ 는 OpenHands/benchmarks 의 benchmarks/<이름>/ 형식을 따름)
    ddi-agent/            에이전트 실행기 (OpenHands 0.62.0 을 조건 B·C 로 띄움)
    ddi-tools/ddi/        도구 인터페이스 (에이전트 IPython 에 import 되는 ddi 패키지)
    ddi-tools/server/     도구 뒷단 예측 서버
    ddi-tools/microagent/ 조건 C 에서 작업 폴더에 넣는 ddi 사용법
    ddi-runtime/          런타임 Docker 이미지 (ddi-runtime, ddi-specialist), 재현 기록
    benchmarks/ddi/       평가 정의: run_infer.py, eval_infer.py, prompts/, data/, scripts/
    results/              버전별 공개 결과 (v2/RESULTS.md, v2/raw/{A,B,C}, v1/RESULTS.md)
    eval_outputs/         새 실행 원자료 (git 제외)
    third_party/DSN-DDI/  원 DSN-DDI 저장소 (submodule)
    tests/                tools/, runtime/, layout/

범위
- 위 폴더와 핵심 파일이 있고, 옛 폴더는 없다
- submodule 이 third_party/DSN-DDI 로 등록되어 있다
- README 두 개의 구조 표가 새 최상위 폴더를 모두 적는다
"""
import os

from _common import check, finish, git, path

FILES = {
    'ddi-tools/ddi': ('__init__.py', 'data/dbvocab.csv', 'data/dsn_drugs.txt', 'data/Interaction_information.csv'),
    'ddi-tools/server': ('app.py', 'predictor.py'),
    'ddi-runtime': ('Dockerfile', 'Dockerfile.specialist', 'REPRODUCTION.md'),
    'benchmarks/ddi': ('run_infer.py', 'eval_infer.py', 'eval_spec.md', 'prompts/task_suffix.txt',
                       'data/questions/questions.jsonl',
                       'data/relation_map/dsn_relation_map.csv', 'scripts/run_eval.sh'),
    'ddi-agent': ('run_agent.py', 'openhands_main.py', 'config.toml.j2', 'requirements.lock.txt'),
    'ddi-tools/microagent': ('ddi.md',),
    'results': ('v2/RESULTS.md', 'v1/RESULTS.md', 'v1/summary.json', 'v2/summary.json', 'v2/ANSWER_COMPARISON.md',
                'v2/raw/A/a_claims.jsonl', 'v2/raw/A/a_answers.jsonl', 'v2/raw/logs/score_output.txt'),
    'tests': ('tools/check_ddi.py', 'tools/check_edges.py', 'tools/check_original.py',
              'runtime/check_runtime.py'),
}
OLD = ('agent', 'ddi', 'server', 'docker', 'eval', 'runs', 'tool', 'tools', 'agent_pkg', 'agent-pkg',
       'agent-server', 'Drug-Interaction-Research', 'benchmarks/ddi/agent', 'ddi-workspace',
       'ddi-agent/c_workspace', 'tests/workspace', 'ddi-tools/ddi/server.py',
       'results/baseline_a', 'results/RESULTS.md')
TOP = ('ddi-agent/', 'ddi-tools/ddi/', 'ddi-tools/server/', 'ddi-tools/microagent/', 'ddi-runtime/', 'benchmarks/ddi/', 'results/', 'eval_outputs/',
       'third_party/DSN-DDI/', 'tests/', 'openspec/')

# 1. 폴더와 파일
for d, files in FILES.items():
    for f in files:
        check('%s/%s 있음' % (d, f), os.path.isfile(path(d, f)))
for v in ('v1', 'v2'):
    for c in 'ABC':
        n = len([f for f in os.listdir(path('results', v, c)) if f.endswith('.json')])
        check('results/%s/%s 채점 10개' % (v, c), n == 10, n)
for c in 'BC':
    n = len([d for d in os.listdir(path('results', 'v2', 'raw', c)) if d.startswith('q')])
    check('results/v2/raw/%s 원자료 10문항' % c, n == 10, n)
for d in OLD:
    check('옛 경로 %s 없음' % d, not os.path.exists(path(d)))

# 2. submodule
check('.gitmodules 경로 third_party/DSN-DDI', 'path = third_party/DSN-DDI' in open(path('.gitmodules')).read())
check('git 이 third_party/DSN-DDI 를 submodule 로 앎',
      git('ls-files', '-s', 'third_party/DSN-DDI').startswith('160000'))

# 3. README 구조 표
for readme in ('README.md', 'README_KO.md'):
    text = open(path(readme), encoding='utf-8').read()
    for d in TOP:
        check('%s 구조 표에 %s' % (readme, d), '| `%s` |' % d in text)

finish()
