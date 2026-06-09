# demo-app CLAUDE.md

## 프로젝트 개요
로그인 + 텍스트 입출력 기능을 가진 풀스택 데모 앱
WSL2 + Kubernetes 환경에서 동작

## 레이어 구조
- WEB  : React (web/)         — 사용자 UI
- API  : FastAPI (api/)       — HTTP 엔드포인트, JWT 인증
- Core : api/core/            — 비즈니스 로직 (API와 분리)
- DB   : PostgreSQL (K8s)     — StatefulSet으로 배포

## 코드 규칙
- 모든 Python 코드에 한국어 주석 필수
- 기능별 pytest 단위 테스트 반드시 함께 작성 (api/tests/)
- API 응답은 항상 JSON 형식
- 환경변수는 .env 또는 K8s ConfigMap/Secret으로 관리

## 개발 환경
- OS: WSL2 Ubuntu
- K8s namespace: demo-app
- Python: 3.10+
- Node: 18+

## 주요 명령어
# API 로컬 실행
cd api && uvicorn main:app --reload --port 8000

# pytest 실행
cd api && pytest tests/ -v

# React 로컬 실행
cd web && npm start

# K8s 배포
kubectl apply -f k8s/
