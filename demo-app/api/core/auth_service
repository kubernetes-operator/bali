# 인증 비즈니스 로직
# JWT 토큰 생성/검증 및 비밀번호 확인 함수를 포함한다

from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# JWT 설정값 (실제 운영 시 환경변수로 분리 필요)
SECRET_KEY = "demo-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 비밀번호 해시 컨텍스트 (bcrypt 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 데모용 임시 사용자 (추후 DB 연동으로 교체)
DEMO_USERS = {
    "admin": pwd_context.hash("password123"),
}


def verify_password(username: str, plain_password: str) -> bool:
    """
    사용자명과 비밀번호를 검증한다
    - 존재하지 않는 사용자: False 반환
    - 비밀번호 불일치: False 반환
    """
    hashed = DEMO_USERS.get(username)
    if not hashed:
        return False
    return pwd_context.verify(plain_password, hashed)


def create_access_token(data: dict) -> str:
    """
    JWT 액세스 토큰을 생성한다
    - 만료 시간: ACCESS_TOKEN_EXPIRE_MINUTES 분 후
    """
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
