# API Layer 단위 테스트 (pytest)
# FastAPI TestClient를 사용하여 실제 HTTP 요청/응답을 검증한다
# 인메모리 SQLite DB로 교체하여 PostgreSQL 없이 실행 가능

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db
from models.schemas import Base, User
from core.auth_service import hash_password

# ----------------------------------------------------------------
# 테스트용 DB 및 앱 설정
# ----------------------------------------------------------------

# 테스트 전용 인메모리 SQLite 엔진
TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=TEST_ENGINE
)


def override_get_db():
    """
    테스트 시 실제 PostgreSQL 대신 인메모리 SQLite를 사용하도록
    get_db 의존성을 교체한다
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI 의존성 교체 및 TestClient 생성
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ----------------------------------------------------------------
# 공통 픽스처
# ----------------------------------------------------------------

@pytest.fixture(autouse=True)
def 테이블_초기화():
    """각 테스트 전에 테이블을 새로 생성하고 후에 삭제한다"""
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture
def 테스트_사용자():
    """테스트용 admin 계정을 DB에 삽입하고 계정 정보를 반환한다"""
    db = TestSessionLocal()
    user = User(
        username="admin",
        hashed_password=hash_password("password123"),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.close()
    return {"username": "admin", "password": "password123"}


@pytest.fixture
def 인증_헤더(테스트_사용자):
    """로그인하여 JWT 토큰을 받고 Authorization 헤더를 반환한다"""
    response = client.post("/api/auth/login", json=테스트_사용자)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ----------------------------------------------------------------
# 헬스체크 테스트
# ----------------------------------------------------------------

class TestHealthCheck:
    """헬스체크 엔드포인트 테스트"""

    def test_헬스체크_200_반환(self):
        """GET /health는 200과 ok 상태를 반환해야 한다"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


# ----------------------------------------------------------------
# 로그인 API 테스트
# ----------------------------------------------------------------

class TestLoginAPI:
    """POST /api/auth/login 테스트"""

    def test_올바른_계정_로그인_성공(self, 테스트_사용자):
        """올바른 계정으로 로그인하면 200과 토큰을 반환해야 한다"""
        response = client.post("/api/auth/login", json=테스트_사용자)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["username"] == "admin"

    def test_잘못된_비밀번호_로그인_실패(self, 테스트_사용자):
        """잘못된 비밀번호로 로그인하면 401을 반환해야 한다"""
        response = client.post("/api/auth/login", json={
            "username": "admin",
            "password": "wrongpassword",
        })
        assert response.status_code == 401

    def test_존재하지_않는_사용자_로그인_실패(self):
        """존재하지 않는 사용자로 로그인하면 401을 반환해야 한다"""
        response = client.post("/api/auth/login", json={
            "username": "nobody",
            "password": "anypass",
        })
        assert response.status_code == 401

    def test_로그인_실패_메시지_동일(self, 테스트_사용자):
        """사용자 없음과 비밀번호 오류의 에러 메시지가 동일해야 한다 (정보 노출 방지)"""
        res_no_user = client.post("/api/auth/login", json={
            "username": "nobody", "password": "pass"
        })
        res_wrong_pw = client.post("/api/auth/login", json={
            "username": "admin", "password": "wrong"
        })
        assert res_no_user.json()["detail"] == res_wrong_pw.json()["detail"]


# ----------------------------------------------------------------
# 노트 API 테스트
# ----------------------------------------------------------------

class TestNotesAPI:
    """POST/GET /api/notes/ 테스트"""

    def test_인증_없이_노트_조회_401(self):
        """Authorization 헤더 없이 노트 조회 시 401을 반환해야 한다"""
        response = client.get("/api/notes/")
        assert response.status_code == 403  # HTTPBearer 미제공 시 403

    def test_노트_생성_성공(self, 인증_헤더):
        """인증된 사용자가 노트를 생성하면 201을 반환해야 한다"""
        response = client.post(
            "/api/notes/",
            json={"content": "테스트 노트입니다."},
            headers=인증_헤더,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "테스트 노트입니다."
        assert "id" in data
        assert "created_at" in data

    def test_빈_내용_노트_생성_400(self, 인증_헤더):
        """빈 내용으로 노트 생성 시 400을 반환해야 한다"""
        response = client.post(
            "/api/notes/",
            json={"content": ""},
            headers=인증_헤더,
        )
        assert response.status_code == 400

    def test_노트_목록_조회_성공(self, 인증_헤더):
        """노트 생성 후 목록 조회 시 생성한 노트가 포함되어야 한다"""
        # 노트 2개 생성
        client.post("/api/notes/", json={"content": "노트 A"}, headers=인증_헤더)
        client.post("/api/notes/", json={"content": "노트 B"}, headers=인증_헤더)

        response = client.get("/api/notes/", headers=인증_헤더)
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 2

    def test_노트_단건_조회_성공(self, 인증_헤더):
        """생성한 노트를 ID로 단건 조회할 수 있어야 한다"""
        create_res = client.post(
            "/api/notes/",
            json={"content": "단건 조회 테스트"},
            headers=인증_헤더,
        )
        note_id = create_res.json()["id"]

        response = client.get(f"/api/notes/{note_id}", headers=인증_헤더)
        assert response.status_code == 200
        assert response.json()["content"] == "단건 조회 테스트"

    def test_존재하지_않는_노트_조회_404(self, 인증_헤더):
        """존재하지 않는 노트 ID 조회 시 404를 반환해야 한다"""
        response = client.get("/api/notes/99999", headers=인증_헤더)
        assert response.status_code == 404
