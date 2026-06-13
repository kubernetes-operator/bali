# 인증 비즈니스 로직 모듈
# JWT 토큰 생성/검증, 비밀번호 해시/검증, 사용자 조회 함수를 제공한다
# API Layer(routers/auth.py)에서 이 모듈을 호출하여 사용한다

import os
import bcrypt

from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.schemas import User

# ----------------------------------------------------------------
# 설정값
# 실운영 환경에서는 반드시 환경변수로 분리할 것
# ----------------------------------------------------------------
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "demo-secret-key-change-in-production")
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# bcrypt 해시 컨텍스트
# deprecated="auto": 구버전 해시 형식을 자동으로 최신 형식으로 업그레이드
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------------------------------------------------------
# 비밀번호 처리 함수
# ----------------------------------------------------------------

def hash_password(plain_password: str) -> str:
    """
    평문 비밀번호를 bcrypt 해시로 변환한다
    - DB에 저장할 때 사용
    - 같은 비밀번호도 매번 다른 해시값이 생성된다 (salt 자동 적용)
    
    return pwd_context.hash(plain_password)
    """
    return bcrypt.hashpw(
        plain_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문 비밀번호와 저장된 해시값을 비교 검증한다
    - 로그인 시 입력 비밀번호 확인에 사용
    - 일치하면 True, 불일치하면 False 반환
    
    return pwd_context.verify(plain_password, hashed_password)
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

# ----------------------------------------------------------------
# 사용자 조회 함수
# ----------------------------------------------------------------

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    사용자명으로 DB에서 사용자를 조회한다
    - 존재하지 않으면 None 반환
    - 로그인 처리 시 호출된다
    """
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    사용자명과 비밀번호로 인증을 수행한다
    - 사용자가 없거나 비밀번호 불일치 시 None 반환
    - 계정이 비활성(is_active=False) 상태이면 None 반환
    - 인증 성공 시 User 객체 반환
    """
    # 사용자 조회
    user = get_user_by_username(db, username)
    if not user:
        return None

    # 비밀번호 검증
    if not verify_password(password, user.hashed_password):
        return None

    # 계정 활성 여부 확인
    if not user.is_active:
        return None

    return user


# ----------------------------------------------------------------
# JWT 토큰 함수
# ----------------------------------------------------------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT 액세스 토큰을 생성한다
    - data: 토큰에 담을 페이로드 (예: {"sub": "admin"})
    - expires_delta: 만료 시간 (기본값: ACCESS_TOKEN_EXPIRE_MINUTES)
    - 반환값: 인코딩된 JWT 문자열
    """
    payload = data.copy()

    # 만료 시각 계산
    expire = datetime.utcnow() + (
        expires_delta if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload.update({"exp": expire})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    JWT 토큰을 디코딩하여 페이로드를 반환한다
    - 만료된 토큰: None 반환
    - 서명 불일치: None 반환
    - 정상 토큰: {"sub": username, "exp": ...} 형태의 dict 반환
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # 만료, 서명 오류, 형식 오류 등 모든 JWT 오류를 None으로 처리
        return None
