# FastAPI 공통 의존성 모듈
# JWT 토큰을 검증하고 현재 로그인 사용자를 반환하는 함수를 제공한다
# 인증이 필요한 모든 엔드포인트에서 Depends(get_current_user)로 사용한다

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import User
from core.auth_service import decode_access_token, get_user_by_username

# Authorization: Bearer {token} 헤더에서 토큰을 추출하는 스키마
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    JWT 토큰을 검증하고 현재 로그인 사용자를 반환한다
    - Authorization: Bearer {token} 헤더가 없으면 자동으로 401 반환
    - 토큰이 만료되거나 유효하지 않으면 401 반환
    - 토큰의 사용자가 DB에 없으면 401 반환
    - 계정이 비활성 상태이면 403 반환

    사용 예시:
        @router.get("/notes")
        def list_notes(user: User = Depends(get_current_user)):
            ...
    """
    # 인증 실패 시 공통으로 사용할 예외
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # JWT 토큰 디코딩
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise credentials_exception

    # 토큰에서 사용자명 추출
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # DB에서 사용자 조회
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception

    # 계정 활성 여부 확인
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다.",
        )

    return user
