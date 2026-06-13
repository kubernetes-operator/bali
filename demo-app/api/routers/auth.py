# 인증 라우터
# 로그인 요청을 처리하고 JWT 토큰을 발급한다
# Core Layer의 authenticate_user, create_access_token을 호출한다

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from core.auth_service import authenticate_user, create_access_token

router = APIRouter()


# ----------------------------------------------------------------
# 요청/응답 스키마
# ----------------------------------------------------------------

class LoginRequest(BaseModel):
    """로그인 요청 바디 스키마"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """로그인 성공 응답 스키마"""
    access_token: str
    token_type: str = "bearer"
    username: str


# ----------------------------------------------------------------
# 엔드포인트
# ----------------------------------------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="로그인",
    description="username/password를 검증하고 JWT 액세스 토큰을 반환한다.",
)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    로그인 엔드포인트
    - 성공: 200 + access_token 반환
    - 실패: 401 Unauthorized 반환
    - 보안: 사용자 없음/비밀번호 오류를 동일 메시지로 처리 (정보 노출 방지)
    """
    # Core Layer에서 인증 수행
    user = authenticate_user(db, request.username, request.password)

    if user is None:
        # 사용자 없음과 비밀번호 오류를 동일 메시지로 반환
        # (어느 쪽이 틀렸는지 노출하지 않음)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT 토큰 생성 — sub 클레임에 username 저장
    token = create_access_token({"sub": user.username})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        username=user.username,
    )
