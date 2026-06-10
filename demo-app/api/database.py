# 데이터베이스 연결 설정 모듈
# SQLAlchemy 엔진 생성, 세션 팩토리, 의존성 주입 함수를 제공한다

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# ----------------------------------------------------------------
# 환경변수에서 DB 접속 URL을 읽어온다
# 로컬 개발:  postgresql://demouser:demopassword@localhost:5432/demoapp
# K8s 환경:   postgresql://demouser:demopassword@postgres:5432/demoapp
#             (postgres = K8s Service 이름)
# ----------------------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://demouser:demopassword@localhost:5432/demoapp"
)

# SQLAlchemy 엔진 생성
# pool_pre_ping: 연결 전 헬스체크로 끊어진 커넥션 자동 복구
# pool_size: 동시 유지할 커넥션 수 (기본값 5)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False,  # True 로 변경 시 SQL 쿼리 로그 출력 (디버깅용)
)

# 세션 팩토리 생성
# autocommit=False: 명시적으로 commit() 호출 필요
# autoflush=False: 쿼리 실행 전 자동 flush 비활성화
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 의존성 주입용 DB 세션 제공 함수
    - 요청마다 새 세션을 열고 완료 후 반드시 닫는다
    - try/finally 구조로 예외 발생 시에도 세션이 닫힘을 보장

    사용 예시:
        @router.get("/notes")
        def list_notes(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
