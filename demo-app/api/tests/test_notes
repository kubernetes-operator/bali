# 노트 서비스 단위 테스트 (pytest)
# create_note, get_all_notes 함수를 검증한다

import pytest
from core.note_service import create_note, get_all_notes, _note_store


@pytest.fixture(autouse=True)
def 노트_저장소_초기화():
    """각 테스트 전에 인메모리 저장소를 초기화한다"""
    _note_store.clear()
    import core.note_service as ns
    ns._next_id = 1
    yield


class TestCreateNote:
    """노트 생성 함수 테스트"""

    def test_노트_생성_성공(self):
        """노트가 정상적으로 생성되어야 한다"""
        result = create_note("테스트 노트입니다")
        assert result["content"] == "테스트 노트입니다"
        assert result["id"] == 1

    def test_여러_노트_생성_시_id_증가(self):
        """노트를 여러 개 생성하면 id가 순서대로 증가해야 한다"""
        note1 = create_note("첫 번째 노트")
        note2 = create_note("두 번째 노트")
        assert note1["id"] == 1
        assert note2["id"] == 2


class TestGetAllNotes:
    """노트 조회 함수 테스트"""

    def test_빈_저장소_조회_빈_리스트_반환(self):
        """저장된 노트가 없으면 빈 리스트를 반환해야 한다"""
        assert get_all_notes() == []

    def test_저장된_노트_전체_조회(self):
        """저장된 모든 노트를 반환해야 한다"""
        create_note("노트 A")
        create_note("노트 B")
        notes = get_all_notes()
        assert len(notes) == 2
        assert notes[0]["content"] == "노트 A"
        assert notes[1]["content"] == "노트 B"
