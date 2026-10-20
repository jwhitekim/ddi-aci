"""루트 구조 확인. 실행: python3 tests/layout/layout_structure.py

목표 구조 (OpenHands software-agent-sdk, OpenHands/benchmarks 를 따름)
    ddi-agent/            에이전트 실행기 (openhands-sdk 대응)
    ddi-tools/ddi/        도구 인터페이스 (openhands-tools 대응)
    ddi-tools/server/     도구 뒷단 예측 서버
    ddi-workspace/        실행 환경 Docker 이미지 (openhands-workspace 대응)
    benchmarks/ddi/       평가 정의: run_infer.py, eval_infer.py, prompts/, data/, scripts/
    results/              공개 결과 (v1/, v2/, v2/raw/, baseline_a/)
    eval_outputs/         새 실행 원자료 (git 제외)
    third_party/DSN-DDI/  원 DSN-DDI 저장소 (submodule)
    tests/                tools/, workspace/, layout/

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
    'ddi-workspace': ('Dockerfile', 'Dockerfile.specialist', 'REPRODUCTION.md'),
    'benchmarks/ddi': ('run_infer.py', 'eval_infer.py', 'eval_spec.md', 'prompts/task_suffix.txt',
                       'data/questions/questions.jsonl',
                       'data/relation_map/dsn_relation_map.csv', 'scripts/run_eval.sh'),
    'ddi-agent': ('run_agent.py', 'openhands_main.py', 'config.toml.j2', 'requirements.lock.txt',
                  'c_workspace/.openhands/microagents/ddi.md'),
    'results': ('RESULTS.md', 'v1/RESULTS.md', 'v1/summary.json', 'v2/summary.json', 'v2/ANSWER_COMPARISON.md',
                'baseline_a/a_claims.jsonl', 'v2/raw/logs/score_output.txt'),
    'tests': ('tools/check_ddi.py', 'tools/check_edges.py', 'tools/check_original.py',
              'workspace/check_runtime.py'),
}
OLD = ('agent', 'ddi', 'server', 'docker', 'eval', 'runs', 'tool', 'tools', 'agent_pkg', 'agent-pkg',
       'agent-server', 'Drug-Interaction-Research', 'benchmarks/ddi/agent')
TOP = ('ddi-agent/', 'ddi-tools/ddi/', 'ddi-tools/server/', 'ddi-workspace/', 'benchmarks/ddi/', 'results/', 'eval_outputs/',
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
    check('옛 폴더 %s/ 없음' % d, not os.path.exists(path(d)))

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
