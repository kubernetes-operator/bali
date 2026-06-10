# pytest 경로 설정 파일
# 이 파일이 있는 디렉토리(api/)를 sys.path에 자동 추가한다
# 덕분에 tests/ 안에서 core, models, routers 등을 경로 없이 import 할 수 있다

import sys
import os

# api/ 디렉토리를 Python 모듈 탐색 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))
