# SQLAlchemy ORM 모델 정의
# users 테이블과 notes 테이블의 컬럼 구조 및 관계를 정의한다

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text,
    DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship, declarative_base

# 모든 ORM 모델의 기반 클래스
# 각 모델 클래스는 Base를 상속받아 테이블과 매핑된다
Base = declarative_base()


class User(Base):
    """
    사용자 테이블 모델
    - 로그인 계정 정보를 저장한다
    - 한 명의 사용자는 여러 개의 노트를 가질 수 있다 (1:N)
    """
    __tablename__ = "users"

    # 기본 키: 자동 증가 정수
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 사용자명: 고유값, 로그인 시 사용
    username = Column(String(50), unique=True, nullable=False, index=True)

    # 이메일: 고유값, 선택 입력
    email = Column(String(100), unique=True, nullable=True)

    # 해시된 비밀번호: 평문 저장 금지, bcrypt로 해시 후 저장
    hashed_password = Column(String(255), nullable=False)

    # 계정 활성 여부: 비활성화 시 로그인 불가
    is_active = Column(Boolean, default=True, nullable=False)

    # 계정 생성 시각: 자동 기록
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 관계 설정: User → Notes (1:N)
    # cascade: 사용자 삭제 시 연관 노트도 함께 삭제
    notes = relationship(
        "Note",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


class Note(Base):
    """
    노트 테이블 모델
    - 사용자가 입력한 텍스트를 저장한다
    - 반드시 특정 사용자(owner)에 속해야 한다
    """
    __tablename__ = "notes"

    # 기본 키: 자동 증가 정수
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 노트 본문: 길이 제한 없는 텍스트
    content = Column(Text, nullable=False)

    # 외래 키: users.id 참조, 사용자 삭제 시 CASCADE 삭제
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # 노트 생성 시각: 자동 기록
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 노트 수정 시각: 수정 시 자동 갱신
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # 관계 설정: Note → User (N:1)
    owner = relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<Note id={self.id} user_id={self.user_id} content={self.content[:20]}>"
