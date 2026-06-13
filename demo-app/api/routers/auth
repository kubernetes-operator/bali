# 인증 관련 라우터
# 로그인 요청을 받아 JWT 토큰을 발급한다

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from core.auth_service import create_access_token, verify_password

router = APIRouter()


class LoginRequest(BaseModel):
    """로그인 요청 바디 스키마"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """토큰 응답 스키마"""
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """
    로그인 엔드포인트
    - username/password를 검증하고 JWT 토큰을 반환한다
    - 실패 시 401 Unauthorized 반환
    """
    # 비밀번호 검증 (추후 DB 연동으로 교체)
    if not verify_password(request.username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
        )
    # JWT 토큰 생성
    token = create_access_token({"sub": request.username})
    return TokenResponse(access_token=token)
