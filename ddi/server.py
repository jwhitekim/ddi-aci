"""DSN-DDI 예측 서버(환경 ②) 연결: 서버 자동 기동, 첫 요청 때 대기, JSON 요청."""
import json
import os
import urllib.error
import urllib.request

SERVER_URL = os.environ.get('DDI_SERVER_URL', 'http://127.0.0.1:8765')

# C 컨테이너에서는 import 할 때 예측 서버(환경 ②)가 없으면 백그라운드로 띄운다 (기다리지 않음: import 가
# 주피터 커널 시작을 막으면 OpenHands 런타임이 시작되지 않는다). 첫 요청 때 서버가 준비될 때까지 기다린다.
# (OpenHands 0.62.0 헤드리스 모드는 setup 스크립트를 실행하지 않고, 컨테이너 CMD 도 바꾸기 때문)
_SERVER_APP = '/opt/ddi-server/app.py'
_SERVER_PYTHON = '/opt/conda/envs/dsn/bin/python'
_SERVER_WAIT_SECONDS = 180
_server_started = False


def _server_up():
    try:
        urllib.request.urlopen(SERVER_URL + '/health', timeout=2)
        return True
    except (urllib.error.URLError, OSError):
        return False


def _start_server():
    global _server_started
    if _server_up() or not (os.path.exists(_SERVER_APP) and os.path.exists(_SERVER_PYTHON)):
        return
    import subprocess
    subprocess.Popen([_SERVER_PYTHON, _SERVER_APP], cwd='/opt/DSN-DDI', stdout=open('/tmp/ddi-server.log', 'w'),
                     stderr=subprocess.STDOUT, start_new_session=True)
    _server_started = True


def _wait_for_server():
    import time
    for _ in range(_SERVER_WAIT_SECONDS):
        if _server_up():
            return True
        time.sleep(1)
    return False


def _post(path, body):
    if _server_started and not _server_up():
        _wait_for_server()
    req = urllib.request.Request(SERVER_URL + path, json.dumps(body).encode('utf-8'),
                                 {'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise ValueError(json.loads(e.read()).get('error', str(e)))
    except urllib.error.URLError as e:
        raise RuntimeError('DSN-DDI 예측 서버(%s)에 연결할 수 없습니다: %s' % (SERVER_URL, e.reason))


if os.environ.get('DDI_AUTOSTART', '1') != '0':
    _start_server()
