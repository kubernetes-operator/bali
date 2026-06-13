# 노트(텍스트) 입출력 라우터
# 노트 생성/조회 API 엔드포인트를 정의한다

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.note_service import create_note, get_all_notes

router = APIRouter()


class NoteRequest(BaseModel):
    """노트 생성 요청 바디"""
    content: str


class NoteResponse(BaseModel):
    """노트 응답 스키마"""
    id: int
    content: str


@router.post("/", response_model=NoteResponse)
def add_note(request: NoteRequest):
    """
    노트 생성 엔드포인트
    - 텍스트를 받아 DB에 저장하고 저장된 노트를 반환한다
    """
    return create_note(request.content)


@router.get("/", response_model=list[NoteResponse])
def list_notes():
    """
    노트 목록 조회 엔드포인트
    - 저장된 모든 노트를 반환한다
    """
    return get_all_notes()
