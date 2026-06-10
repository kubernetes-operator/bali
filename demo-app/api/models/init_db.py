# DB 초기화 스크립트
# 테이블 생성 및 데모용 초기 데이터(admin 계정)를 삽입한다
# 실행 방법: cd api && python -m models.init_db

import sys
import os

# 상위 디렉토리를 경로에 추가 (api/ 루트에서 import 가능하도록)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, SessionLocal
from models.schemas import Base, User
from passlib.context import CryptContext

# 비밀번호 해시 컨텍스트 (bcrypt 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_tables() -> None:
    """
    Base에 등록된 모든 모델 클래스를 기반으로 테이블을 생성한다
    - 이미 존재하는 테이블은 건너뛴다 (checkfirst=True)
    """
    print("[1/3] 테이블 생성 중...")
    Base.metadata.create_all(bind=engine, checkfirst=True)
    print("      users, notes 테이블 생성 완료")


def seed_admin_user() -> None:
    """
    데모용 admin 계정을 삽입한다
    - 이미 존재하면 건너뛴다
    - 비밀번호: password123 (bcrypt 해시로 저장)
    """
    print("[2/3] 초기 데이터 삽입 중...")
    db = SessionLocal()
    try:
        # admin 계정이 이미 있으면 건너뜀
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print("      admin 계정이 이미 존재함 — 건너뜀")
            return

        # admin 계정 생성
        admin = User(
            username="admin",
            email="admin@demo.local",
            hashed_password=pwd_context.hash("password123"),
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print("      admin 계정 생성 완료 (비밀번호: password123)")
    finally:
        db.close()


def verify_tables() -> None:
    """
    생성된 테이블 목록을 출력하여 정상 생성 여부를 확인한다
    """
    print("[3/3] 테이블 확인 중...")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    for t in tables:
        cols = [c["name"] for c in inspector.get_columns(t)]
        print(f"      {t}: {', '.join(cols)}")


if __name__ == "__main__":
    print("=" * 40)
    print("  demo-app DB 초기화 시작")
    print("=" * 40)
    create_tables()
    seed_admin_user()
    verify_tables()
    print("=" * 40)
    print("  초기화 완료")
    print("=" * 40)
