# 노트 비즈니스 로직
# 노트 생성/조회 함수를 포함한다 (데모용 인메모리, 추후 DB 연동)

from typing import List

# 데모용 인메모리 저장소 (추후 SQLAlchemy + PostgreSQL로 교체)
_note_store: List[dict] = []
_next_id: int = 1


def create_note(content: str) -> dict:
    """
    새 노트를 저장하고 반환한다
    - content: 저장할 텍스트 내용
    """
    global _next_id
    note = {"id": _next_id, "content": content}
    _note_store.append(note)
    _next_id += 1
    return note


def get_all_notes() -> List[dict]:
    """
    저장된 모든 노트를 반환한다
    """
    return list(_note_store)
