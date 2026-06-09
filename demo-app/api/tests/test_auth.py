# 인증 서비스 단위 테스트 (pytest)
# verify_password, create_access_token 함수를 검증한다

import pytest
from core.auth_service import verify_password, create_access_token


class TestVerifyPassword:
    """비밀번호 검증 함수 테스트"""

    def test_올바른_사용자명과_비밀번호_검증_성공(self):
        """정상적인 로그인 정보는 True를 반환해야 한다"""
        assert verify_password("admin", "password123") is True

    def test_잘못된_비밀번호_검증_실패(self):
        """잘못된 비밀번호는 False를 반환해야 한다"""
        assert verify_password("admin", "wrongpassword") is False

    def test_존재하지_않는_사용자_검증_실패(self):
        """존재하지 않는 사용자명은 False를 반환해야 한다"""
        assert verify_password("unknown_user", "password123") is False


class TestCreateAccessToken:
    """JWT 토큰 생성 함수 테스트"""

    def test_토큰_생성_성공(self):
        """토큰이 문자열로 생성되어야 한다"""
        token = create_access_token({"sub": "admin"})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_토큰_형식_JWT_점_세개(self):
        """JWT 토큰은 점(.)으로 구분된 3부분이어야 한다"""
        token = create_access_token({"sub": "admin"})
        parts = token.split(".")
        assert len(parts) == 3
