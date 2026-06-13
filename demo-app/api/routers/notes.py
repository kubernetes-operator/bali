# 노트 라우터
# 텍스트 입력/조회 엔드포인트를 제공한다
# 모든 엔드포인트는 JWT 인증이 필요하다 (Depends(get_current_user))

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models.schemas import User
from dependencies import get_current_user
from core.note_service import create_note, get_notes_by_user, get_note_by_id

router = APIRouter()


# ----------------------------------------------------------------
# 요청/응답 스키마
# ----------------------------------------------------------------

class NoteCreateRequest(BaseModel):
    """노트 생성 요청 바디"""
    content: str


class NoteResponse(BaseModel):
    """노트 응답 스키마"""
    id: int
    content: str
    user_id: int
    created_at: datetime

    class Config:
        # SQLAlchemy ORM 객체를 Pydantic 모델로 자동 변환
        from_attributes = True


# ----------------------------------------------------------------
# 엔드포인트
# ----------------------------------------------------------------

@router.get(
    "/",
    response_model=List[NoteResponse],
    summary="노트 목록 조회",
    description="로그인한 사용자의 모든 노트를 최신순으로 반환한다.",
)
def list_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    노트 목록 조회 엔드포인트
    - JWT 토큰으로 인증된 사용자의 노트만 반환한다
    - 다른 사용자의 노트는 절대 노출되지 않는다
    """
    return get_notes_by_user(db, current_user.id)


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="노트 생성",
    description="새 노트를 저장하고 저장된 노트를 반환한다.",
)
def add_note(
    request: NoteCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    노트 생성 엔드포인트
    - 빈 내용은 저장하지 않고 400 Bad Request 반환
    - 성공 시 201 Created + 저장된 노트 반환
    """
    try:
        note = create_note(db, request.content, current_user.id)
    except ValueError as e:
        # Core Layer에서 발생한 빈 내용 오류를 HTTP 400으로 변환
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return note


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="노트 단건 조회",
    description="특정 노트를 ID로 조회한다.",
)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    노트 단건 조회 엔드포인트
    - 본인 노트가 아니면 404 반환 (존재 여부 노출 방지)
    """
    note = get_note_by_id(db, note_id, current_user.id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="노트를 찾을 수 없습니다.",
        )
    return note
