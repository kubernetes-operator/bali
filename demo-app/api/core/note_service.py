# 노트 비즈니스 로직 모듈
# 노트 생성/조회 기능을 제공한다
# SQLAlchemy Session을 통해 PostgreSQL에 직접 읽고 쓴다

from typing import List, Optional
from sqlalchemy.orm import Session

from models.schemas import Note


# ----------------------------------------------------------------
# 노트 생성
# ----------------------------------------------------------------

def create_note(db: Session, content: str, user_id: int) -> Note:
    """
    새 노트를 DB에 저장하고 저장된 Note 객체를 반환한다
    - content: 저장할 텍스트 내용 (빈 문자열 불허)
    - user_id: 노트를 작성한 사용자의 ID
    - 저장 후 db.refresh()로 DB 생성 값(id, created_at)을 동기화한다
    """
    # 빈 내용 저장 방지
    if not content or not content.strip():
        raise ValueError("노트 내용은 비어 있을 수 없습니다.")

    note = Note(
        content=content.strip(),  # 앞뒤 공백 제거 후 저장
        user_id=user_id,
    )
    db.add(note)
    db.commit()
    db.refresh(note)  # DB에서 생성된 id, created_at 값을 객체에 반영
    return note


# ----------------------------------------------------------------
# 노트 조회
# ----------------------------------------------------------------

def get_notes_by_user(db: Session, user_id: int) -> List[Note]:
    """
    특정 사용자의 모든 노트를 최신순으로 반환한다
    - user_id: 조회할 사용자 ID
    - created_at 내림차순 정렬 (최신 노트가 먼저)
    """
    return (
        db.query(Note)
        .filter(Note.user_id == user_id)
        .order_by(Note.created_at.desc())
        .all()
    )


def get_note_by_id(db: Session, note_id: int, user_id: int) -> Optional[Note]:
    """
    특정 노트를 ID로 조회한다
    - note_id와 user_id를 함께 검증하여 다른 사용자의 노트 조회를 방지한다
    - 존재하지 않거나 소유자가 다르면 None 반환
    """
    return (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id)
        .first()
    )
