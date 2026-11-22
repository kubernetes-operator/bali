# 인증 라우터
# 로그인 요청을 처리하고 JWT 토큰을 발급한다
# Core Layer의 authenticate_user, create_access_token을 호출한다

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from core.auth_service import authenticate_user, create_access_token
from core import web_access
from dependencies import get_current_user
from models.schemas import User, UserAccess

router = APIRouter()


# ----------------------------------------------------------------
# 요청/응답 스키마
# ----------------------------------------------------------------

class LoginRequest(BaseModel):
    """로그인 요청 바디 스키마"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """로그인 성공 응답 스키마"""
    access_token: str
    token_type: str = "bearer"
    username: str


# ----------------------------------------------------------------
# 엔드포인트
# ----------------------------------------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="로그인",
    description="username/password를 검증하고 JWT 액세스 토큰을 반환한다.",
)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    로그인 엔드포인트
    - 성공: 200 + access_token 반환
    - 실패: 401 Unauthorized 반환
    - 보안: 사용자 없음/비밀번호 오류를 동일 메시지로 처리 (정보 노출 방지)
    """
    # Core Layer에서 인증 수행
    # 비밀번호 확인 전에 버전을 읽어 변경 중인 이전 비밀번호가 새 버전을 얻지 못하게 한다.
    version = db.query(UserAccess.token_version).join(User,User.id==UserAccess.user_id).filter(User.username==request.username).scalar() or 0
    user = authenticate_user(db, request.username, request.password)

    if user is None:
        # 사용자 없음과 비밀번호 오류를 동일 메시지로 반환
        # (어느 쪽이 틀렸는지 노출하지 않음)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if web_access.access(db,user)["version"] != version:
        raise HTTPException(401,"아이디 또는 비밀번호가 올바르지 않습니다.")

    # JWT 토큰 생성 — sub 클레임에 username 저장
    token = create_access_token({"sub": user.username,"ver": version})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        username=user.username,
    )


class CreateUserBody(BaseModel):
    username:str
    password:str
    role:str='viewer'
    pages:list[str]=[]
class UpdateUserBody(BaseModel):
    role:str|None=None
    pages:list[str]|None=None
    password:str|None=None
class ConfirmedPasswordBody(BaseModel):
    current_password:str
    new_password:str
    confirm_password:str

@router.get('/ui/session')
def ui_session(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return web_access.summary(db,user)

@router.post('/ui/password')
def ui_password(body:ConfirmedPasswordBody,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return web_access.change_password(db,user,body.current_password,body.new_password,body.confirm_password)

@router.get('/users')
def ui_users(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return web_access.list_users(db)

@router.post('/users')
def ui_create_user(body:CreateUserBody,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return web_access.create(db,body.username,body.password,body.role,body.pages)

@router.patch('/users/{username}')
def ui_update_user(username:str,body:UpdateUserBody,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    changes=body.model_dump(exclude_unset=True)
    if any(value is None for value in changes.values()):raise HTTPException(400,'변경 값은 null일 수 없습니다')
    return web_access.edit(db,username,changes)
