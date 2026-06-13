# 노트 Core 서비스 단위 테스트 (pytest)
# note_service.py의 모든 함수를 독립적으로 검증한다
# SQLite 인메모리 DB를 사용하므로 PostgreSQL 없이 실행 가능

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.schemas import Base, User, Note
from core.auth_service import hash_password
from core.note_service import (
    create_note,
    get_notes_by_user,
    get_note_by_id,
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
    """테스트용 사용자를 생성하고 반환한다"""
    user = User(
        username="noteuser",
        hashed_password=hash_password("pass123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ----------------------------------------------------------------
# 노트 생성 테스트
# ----------------------------------------------------------------

class TestCreateNote:
    """노트 생성 함수 테스트"""

    def test_노트_생성_성공(self, db_session, 샘플_사용자):
        """정상적인 내용으로 노트를 생성하면 Note 객체를 반환해야 한다"""
        note = create_note(db_session, "첫 번째 노트입니다.", 샘플_사용자.id)

        assert note.id is not None
        assert note.content == "첫 번째 노트입니다."
        assert note.user_id == 샘플_사용자.id

    def test_노트_생성_후_created_at_자동_설정(self, db_session, 샘플_사용자):
        """노트 생성 시 created_at이 자동으로 설정되어야 한다"""
        note = create_note(db_session, "타임스탬프 테스트", 샘플_사용자.id)
        assert note.created_at is not None

    def test_앞뒤_공백_제거_후_저장(self, db_session, 샘플_사용자):
        """앞뒤 공백은 제거되어 저장되어야 한다"""
        note = create_note(db_session, "  공백 포함 노트  ", 샘플_사용자.id)
        assert note.content == "공백 포함 노트"

    def test_빈_내용_노트_생성_예외_발생(self, db_session, 샘플_사용자):
        """빈 문자열로 노트 생성 시 ValueError가 발생해야 한다"""
        with pytest.raises(ValueError, match="비어 있을 수 없습니다"):
            create_note(db_session, "", 샘플_사용자.id)

    def test_공백만_있는_내용_노트_생성_예외_발생(self, db_session, 샘플_사용자):
        """공백만 있는 내용으로 노트 생성 시 ValueError가 발생해야 한다"""
        with pytest.raises(ValueError):
            create_note(db_session, "   ", 샘플_사용자.id)


# ----------------------------------------------------------------
# 노트 조회 테스트
# ----------------------------------------------------------------

class TestGetNotes:
    """노트 조회 함수 테스트"""

    def test_사용자_노트_전체_조회(self, db_session, 샘플_사용자):
        """사용자의 모든 노트를 반환해야 한다"""
        create_note(db_session, "노트 A", 샘플_사용자.id)
        create_note(db_session, "노트 B", 샘플_사용자.id)
        create_note(db_session, "노트 C", 샘플_사용자.id)

        notes = get_notes_by_user(db_session, 샘플_사용자.id)
        assert len(notes) == 3

    def test_노트_없는_사용자_빈_리스트_반환(self, db_session, 샘플_사용자):
        """노트가 없는 사용자 조회 시 빈 리스트를 반환해야 한다"""
        notes = get_notes_by_user(db_session, 샘플_사용자.id)
        assert notes == []

    def test_다른_사용자_노트_미포함(self, db_session, 샘플_사용자):
        """다른 사용자의 노트는 조회 결과에 포함되지 않아야 한다"""
        # 두 번째 사용자 생성
        other = User(
            username="otheruser",
            hashed_password=hash_password("pass"),
            is_active=True,
        )
        db_session.add(other)
        db_session.commit()
        db_session.refresh(other)

        create_note(db_session, "내 노트", 샘플_사용자.id)
        create_note(db_session, "다른 사람 노트", other.id)

        # 샘플_사용자의 노트만 조회
        notes = get_notes_by_user(db_session, 샘플_사용자.id)
        assert len(notes) == 1
        assert notes[0].content == "내 노트"

    def test_노트_ID로_단건_조회_성공(self, db_session, 샘플_사용자):
        """note_id와 user_id가 일치하면 Note 객체를 반환해야 한다"""
        created = create_note(db_session, "단건 조회 테스트", 샘플_사용자.id)
        note = get_note_by_id(db_session, created.id, 샘플_사용자.id)

        assert note is not None
        assert note.id == created.id

    def test_다른_사용자_노트_단건_조회_None_반환(self, db_session, 샘플_사용자):
        """다른 사용자의 노트를 ID로 조회하면 None을 반환해야 한다"""
        other = User(
            username="otheruser2",
            hashed_password=hash_password("pass"),
            is_active=True,
        )
        db_session.add(other)
        db_session.commit()
        db_session.refresh(other)

        other_note = create_note(db_session, "다른 사람 노트", other.id)

        # 샘플_사용자가 다른 사람 노트 조회 시도
        note = get_note_by_id(db_session, other_note.id, 샘플_사용자.id)
        assert note is None
