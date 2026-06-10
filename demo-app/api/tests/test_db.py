# DB 모델 단위 테스트
# SQLAlchemy 모델의 컬럼 정의, 관계, 기본값을 검증한다
# 인메모리 SQLite를 사용하므로 PostgreSQL 없이도 실행 가능

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 테스트 대상 모듈
from models.schemas import Base, User, Note


# ----------------------------------------------------------------
# 테스트용 인메모리 DB 픽스처
# 각 테스트 함수마다 독립된 DB 세션을 제공한다
# ----------------------------------------------------------------
@pytest.fixture(scope="function")
def db_session():
    """
    인메모리 SQLite DB 세션을 생성한다
    - 테스트 완료 후 테이블 전체를 삭제하여 격리를 보장한다
    - PostgreSQL 없이도 모델 구조 검증 가능
    """
    # 인메모리 SQLite 엔진 생성 (테스트 전용)
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    # 모든 테이블 생성
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # 테스트 함수에 세션 전달

    # 테스트 후 정리
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def 샘플_사용자(db_session):
    """테스트용 사용자 객체를 생성하고 DB에 저장한다"""
    user = User(
        username="testuser",
        email="test@demo.local",
        hashed_password="$2b$12$fakehash",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ----------------------------------------------------------------
# User 모델 테스트
# ----------------------------------------------------------------
class TestUserModel:
    """User 모델 컬럼 및 기본값 테스트"""

    def test_사용자_생성_성공(self, db_session):
        """사용자를 DB에 저장하면 id가 자동 할당되어야 한다"""
        user = User(
            username="alice",
            hashed_password="hashed_pw",
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # id가 자동 할당되었는지 확인
        assert user.id is not None
        assert user.id > 0

    def test_사용자_기본값_is_active_true(self, db_session):
        """is_active 기본값은 True여야 한다"""
        user = User(username="bob", hashed_password="pw")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.is_active is True

    def test_사용자_created_at_자동_설정(self, db_session):
        """created_at은 저장 시 자동으로 현재 시각이 설정되어야 한다"""
        user = User(username="carol", hashed_password="pw")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)

    def test_사용자명_중복_저장_실패(self, db_session):
        """동일한 username은 unique 제약으로 저장이 실패해야 한다"""
        from sqlalchemy.exc import IntegrityError

        user1 = User(username="duplicate", hashed_password="pw1")
        user2 = User(username="duplicate", hashed_password="pw2")
        db_session.add(user1)
        db_session.commit()

        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()


# ----------------------------------------------------------------
# Note 모델 테스트
# ----------------------------------------------------------------
class TestNoteModel:
    """Note 모델 컬럼 및 외래 키 관계 테스트"""

    def test_노트_생성_성공(self, db_session, 샘플_사용자):
        """노트를 사용자와 연결하여 저장하면 id가 자동 할당되어야 한다"""
        note = Note(
            content="첫 번째 테스트 노트입니다.",
            user_id=샘플_사용자.id,
        )
        db_session.add(note)
        db_session.commit()
        db_session.refresh(note)

        assert note.id is not None
        assert note.content == "첫 번째 테스트 노트입니다."

    def test_노트_created_at_자동_설정(self, db_session, 샘플_사용자):
        """created_at은 저장 시 자동으로 설정되어야 한다"""
        note = Note(content="타임스탬프 테스트", user_id=샘플_사용자.id)
        db_session.add(note)
        db_session.commit()
        db_session.refresh(note)

        assert note.created_at is not None

    def test_사용자_관계_조회(self, db_session, 샘플_사용자):
        """note.owner를 통해 연결된 사용자를 조회할 수 있어야 한다"""
        note = Note(content="관계 테스트", user_id=샘플_사용자.id)
        db_session.add(note)
        db_session.commit()
        db_session.refresh(note)

        assert note.owner.username == "testuser"

    def test_사용자_삭제_시_노트_cascade_삭제(self, db_session, 샘플_사용자):
        """사용자 삭제 시 연관 노트도 함께 삭제되어야 한다 (CASCADE)"""
        note = Note(content="삭제 테스트 노트", user_id=샘플_사용자.id)
        db_session.add(note)
        db_session.commit()

        note_id = note.id

        # 사용자 삭제
        db_session.delete(샘플_사용자)
        db_session.commit()

        # 노트도 삭제되었는지 확인
        deleted_note = db_session.query(Note).filter(Note.id == note_id).first()
        assert deleted_note is None

    def test_사용자_노트_1대N_관계(self, db_session, 샘플_사용자):
        """한 사용자에 여러 노트를 연결할 수 있어야 한다"""
        for i in range(3):
            note = Note(content=f"노트 {i+1}", user_id=샘플_사용자.id)
            db_session.add(note)
        db_session.commit()
        db_session.refresh(샘플_사용자)

        assert len(샘플_사용자.notes) == 3
