# demo-app

로그인 + 텍스트 입출력 기능을 갖춘 풀스택 데모 애플리케이션입니다.
React, FastAPI, PostgreSQL을 4계층 구조로 구성하고 Kubernetes 클러스터에 배포합니다.

---

## 기술 스택

| 레이어 | 기술 | 역할 |
|--------|------|------|
| WEB | React 18, Axios, Nginx | 사용자 UI 서빙 |
| API | FastAPI, python-jose | HTTP 엔드포인트, JWT 인증 |
| Core | Python, bcrypt, SQLAlchemy | 비즈니스 로직 |
| DB | PostgreSQL 15 | 데이터 영구 저장 |
| 인프라 | Kubernetes, Docker | 컨테이너 오케스트레이션 |

---

## 아키텍처

```
[브라우저]
    ↓ http://<노드IP>:30000
[WEB] React + Nginx (NodePort 30000)
    ↓ /api/* Nginx 프록시
[API] FastAPI (ClusterIP 8000)
    ↓ SQLAlchemy ORM
[Core] Python 비즈니스 로직
    ↓ psycopg2
[DB] PostgreSQL (StatefulSet + PVC)
```

---

## 디렉토리 구조

```
demo-app/
├── CLAUDE.md               # Claude Code CLI 프로젝트 설정
├── AGENTS.md               # 레이어별 Claude 에이전트 가이드
├── api/
│   ├── main.py             # FastAPI 앱 진입점
│   ├── database.py         # DB 연결 설정
│   ├── dependencies.py     # JWT 인증 의존성
│   ├── core/
│   │   ├── auth_service.py # JWT + bcrypt 인증 로직
│   │   └── note_service.py # 노트 CRUD 로직
│   ├── models/
│   │   ├── schemas.py      # SQLAlchemy ORM 모델
│   │   └── init_db.py      # 테이블 초기화 스크립트
│   ├── routers/
│   │   ├── auth.py         # POST /api/auth/login
│   │   └── notes.py        # GET/POST /api/notes/
│   ├── tests/              # pytest 단위 테스트 (43개)
│   ├── conftest.py         # pytest 경로 설정
│   ├── pytest.ini          # pytest 전역 설정
│   ├── requirements.txt
│   └── Dockerfile
├── web/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx         # 루트 컴포넌트
│   │   ├── api/client.js   # Axios 클라이언트
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   └── Notes.jsx
│   │   └── components/
│   │       └── NoteForm.jsx
│   ├── package.json
│   └── Dockerfile
└── k8s/
    ├── namespace.yaml
    ├── postgres/           # StatefulSet, PVC, Service, Secret
    ├── api/                # Deployment, Service, ConfigMap
    └── web/                # Deployment, Service, ConfigMap
```

---

## 시작하기

### 사전 요구사항

- WSL2 Ubuntu
- Docker
- kubectl (K8s 클러스터 연결됨)
- Node.js 18+
- Python 3.10+

### 1. 프로젝트 구조 생성

```bash
chmod +x setup_demo_app.sh
./setup_demo_app.sh
```

### 2. PostgreSQL K8s 배포

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/postgres/secret.yaml
kubectl apply -f k8s/postgres/pvc.yaml
kubectl apply -f k8s/postgres/statefulset.yaml
kubectl apply -f k8s/postgres/service.yaml

# Pod Running 확인
kubectl get pods -n demo-app -w
```

### 3. DB 테이블 및 초기 계정 생성

```bash
# PostgreSQL Pod 접속
kubectl exec -it postgres-0 -n demo-app -- psql -U demouser -d demoapp

# SQL 실행
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE, hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE, created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY, content TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(), updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

# admin 역할 및 계정 생성
CREATE ROLE admin WITH LOGIN PASSWORD 'password123' SUPERUSER;
INSERT INTO users (username, email, hashed_password, is_active)
VALUES ('admin', 'admin@demo.local', '$(bcrypt hash of password123)', true);
\q
```

### 4. pytest 실행

```bash
cd demo-app/api
pip install -r requirements.txt
pytest tests/ -v
```

### 5. Docker 이미지 빌드 및 배포

```bash
# API
docker build -t registry.local.cloud:5000/demo-app-api:latest ./api
docker push registry.local.cloud:5000/demo-app-api:latest

# WEB
cd web && rm -rf build/ node_modules/.cache/
npm run build
docker build --no-cache -t registry.local.cloud:5000/demo-app-web:latest .
docker push registry.local.cloud:5000/demo-app-web:latest

# K8s 배포
kubectl apply -f k8s/api/
kubectl apply -f k8s/web/
```

### 6. 접속 확인

```
http://<워커노드IP>:30000
테스트 계정: admin / password123
```

---

## API 엔드포인트

| 메서드 | 경로 | 인증 | 설명 |
|--------|------|------|------|
| GET | /health | 불필요 | 헬스체크 |
| POST | /api/auth/login | 불필요 | 로그인 → JWT 반환 |
| GET | /api/notes/ | JWT 필요 | 노트 목록 조회 |
| POST | /api/notes/ | JWT 필요 | 노트 생성 |
| GET | /api/notes/{id} | JWT 필요 | 노트 단건 조회 |

Swagger UI: `http://localhost:8000/docs`

---

## 테스트

```bash
cd demo-app/api

# 전체 테스트 실행
pytest tests/ -v

# 파일별 실행
pytest tests/test_db.py -v      # DB 모델 테스트 (9개)
pytest tests/test_auth.py -v    # 인증 로직 테스트 (14개)
pytest tests/test_notes.py -v   # 노트 CRUD 테스트 (9개)
pytest tests/test_api.py -v     # API 엔드포인트 테스트 (11개)
```

총 43개 테스트, SQLite 인메모리 사용으로 PostgreSQL 없이 실행 가능합니다.

---

## 코드 규칙

- 모든 Python 코드에 한국어 주석 포함
- 기능 추가 시 pytest 단위 테스트 함께 작성
- CSS Module 사용 금지 — 인라인 스타일 사용 (CRA + K8s 환경 충돌)
- Axios baseURL 빈 문자열 유지 — K8s Nginx 프록시 경유

---

## 알려진 제약사항

| 항목 | 내용 |
|------|------|
| 인증 | 단일 admin 계정 (회원가입 미구현) |
| 노트 | 생성/조회만 가능 (수정/삭제 미구현) |
| 보안 | JWT Secret Key 하드코딩 (운영 환경에서 Secret으로 분리 필요) |
| DB | Alembic 마이그레이션 미적용 |

---

## 다음 개발 예정

- [ ] 노트 수정 / 삭제
- [ ] 회원가입
- [ ] Alembic DB 마이그레이션
- [ ] 노트 검색 및 페이지네이션
- [ ] GitHub Actions CI/CD 연동

---

## 참조 문서

- [AGENTS.md](./AGENTS.md) — 레이어별 Claude 에이전트 가이드
- [CLAUDE.md](./CLAUDE.md) — Claude Code CLI 프로젝트 설정
- [REPORT.md](./REPORT.md) — 구축 완료 리포트
