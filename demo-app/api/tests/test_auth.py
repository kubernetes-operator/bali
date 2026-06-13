# 인증 Core 서비스 단위 테스트 (pytest)
# auth_service.py의 모든 함수를 독립적으로 검증한다
# SQLite 인메모리 DB를 사용하므로 PostgreSQL 없이 실행 가능

import pytest
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.schemas import Base, User
from core.auth_service import (
    hash_password,
    verify_password,
    get_user_by_username,
    authenticate_user,
    create_access_token,
    decode_access_token,
)


# ----------------------------------------------------------------
# 공통 픽스처
# ----------------------------------------------------------------

@pytest.fixture(scope="function")
def db_session():
    """각 테스트마다 독립된 인메모리 SQLite 세션을 제공한다"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def 샘플_사용자(db_session):
    """비밀번호가 해시된 테스트용 사용자를 생성한다"""
    user = User(
        username="testuser",
        email="test@demo.local",
        hashed_password=hash_password("testpass123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ----------------------------------------------------------------
# 비밀번호 해시/검증 테스트
# ----------------------------------------------------------------

class TestPasswordHandling:
    """비밀번호 해시 및 검증 함수 테스트"""

    def test_비밀번호_해시_생성_성공(self):
        """hash_password는 문자열을 반환해야 한다"""
        hashed = hash_password("mypassword")
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_동일_비밀번호_다른_해시_생성(self):
        """같은 비밀번호도 매번 다른 해시가 생성되어야 한다 (salt 적용)"""
        hash1 = hash_password("samepassword")
        hash2 = hash_password("samepassword")
        assert hash1 != hash2

    def test_올바른_비밀번호_검증_성공(self):
        """올바른 비밀번호와 해시가 일치하면 True를 반환해야 한다"""
        hashed = hash_password("correct_pass")
        assert verify_password("correct_pass", hashed) is True

    def test_잘못된_비밀번호_검증_실패(self):
        """잘못된 비밀번호는 False를 반환해야 한다"""
        hashed = hash_password("correct_pass")
        assert verify_password("wrong_pass", hashed) is False


# ----------------------------------------------------------------
# 사용자 조회 테스트
# ----------------------------------------------------------------

class TestUserQuery:
    """사용자 조회 함수 테스트"""

    def test_존재하는_사용자_조회_성공(self, db_session, 샘플_사용자):
        """존재하는 username으로 조회하면 User 객체를 반환해야 한다"""
        user = get_user_by_username(db_session, "testuser")
        assert user is not None
        assert user.username == "testuser"

    def test_존재하지_않는_사용자_조회_None_반환(self, db_session):
        """존재하지 않는 username 조회 시 None을 반환해야 한다"""
        user = get_user_by_username(db_session, "nobody")
        assert user is None


# ----------------------------------------------------------------
# 사용자 인증 테스트
# ----------------------------------------------------------------

class TestAuthenticateUser:
    """인증 함수 통합 테스트"""

    def test_올바른_계정_인증_성공(self, db_session, 샘플_사용자):
        """올바른 username/password로 인증하면 User 객체를 반환해야 한다"""
        user = authenticate_user(db_session, "testuser", "testpass123")
        assert user is not None
        assert user.username == "testuser"

    def test_잘못된_비밀번호_인증_실패(self, db_session, 샘플_사용자):
        """잘못된 비밀번호로 인증하면 None을 반환해야 한다"""
        user = authenticate_user(db_session, "testuser", "wrongpass")
        assert user is None

    def test_존재하지_않는_사용자_인증_실패(self, db_session):
        """존재하지 않는 사용자로 인증하면 None을 반환해야 한다"""
        user = authenticate_user(db_session, "nobody", "anypass")
        assert user is None

    def test_비활성_계정_인증_실패(self, db_session):
        """is_active=False인 계정은 인증이 실패해야 한다"""
        inactive = User(
            username="inactive",
            hashed_password=hash_password("pass123"),
            is_active=False,
        )
        db_session.add(inactive)
        db_session.commit()

        user = authenticate_user(db_session, "inactive", "pass123")
        assert user is None


# ----------------------------------------------------------------
# JWT 토큰 테스트
# ----------------------------------------------------------------

class TestJWTToken:
    """JWT 토큰 생성 및 디코딩 테스트"""

    def test_토큰_생성_문자열_반환(self):
        """create_access_token은 JWT 형식의 문자열을 반환해야 한다"""
        token = create_access_token({"sub": "testuser"})
        assert isinstance(token, str)
        # JWT는 점(.)으로 구분된 3개 부분으로 구성된다
        assert len(token.split(".")) == 3

    def test_토큰_디코딩_페이로드_확인(self):
        """생성된 토큰을 디코딩하면 원본 페이로드를 반환해야 한다"""
        token = create_access_token({"sub": "testuser"})
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"

    def test_만료된_토큰_디코딩_None_반환(self):
        """만료 시간이 지난 토큰은 None을 반환해야 한다"""
        # 만료 시간을 -1분으로 설정하여 즉시 만료
        token = create_access_token(
            {"sub": "testuser"},
            expires_delta=timedelta(minutes=-1),
        )
        payload = decode_access_token(token)
        assert payload is None

    def test_잘못된_토큰_디코딩_None_반환(self):
        """유효하지 않은 토큰 문자열은 None을 반환해야 한다"""
        payload = decode_access_token("invalid.token.string")
        assert payload is None
