"""기존 JWT/메모 소유권을 보존하는 부가 웹 권한 계약."""
import json
from fastapi import HTTPException
from sqlalchemy import select,update,literal
from sqlalchemy.exc import IntegrityError
from models.schemas import Base,User,UserAccess,AccessState
from core import page_policy
from core.auth_service import hash_password,verify_password

PROJECT='bali'

def migrate(engine):
    Base.metadata.create_all(engine,tables=[UserAccess.__table__,AccessState.__table__])
    if engine.dialect.name=='postgresql':from sqlalchemy.dialects.postgresql import insert
    elif engine.dialect.name=='sqlite':from sqlalchemy.dialects.sqlite import insert
    else:raise RuntimeError('Unsupported web access migration database')
    with engine.begin() as conn:
        conn.execute(insert(AccessState).values(id=1).on_conflict_do_nothing())
        # 기존 계정의 쓰기 기능과 로그인 토큰을 보존한다. 신규 계정은 명시적으로 viewer부터 생성한다.
        source=select(User.id,literal('admin'),literal(None),literal(0)).where(literal(True))
        conn.execute(insert(UserAccess).from_select(['user_id','role','pages','token_version'],source).on_conflict_do_nothing())

def access(db,user):
    row=db.get(UserAccess,user.id)
    if row is None:return {'role':'viewer','pages':[],'version':0}
    try:
        pages=None if row.pages is None else json.loads(row.pages)
        pages=page_policy.normalize(PROJECT,row.role,pages)
    except (ValueError,TypeError):return {'role':'viewer','pages':[],'version':row.token_version}
    return {'role':row.role,'pages':pages,'version':row.token_version}

def check(db,user,path,method):
    value=access(db,user)
    if path=='/api/auth/users' or path.startswith('/api/auth/users/'):page='users'
    elif path=='/api/notes' or path.startswith('/api/notes/'):page='notes'
    elif path in ('/api/auth/ui/session','/api/auth/ui/password'):page='settings'
    else:page='unknown'
    if not page_policy.allowed(PROJECT,value['role'],value['pages'],page):raise HTTPException(403,'이 페이지에 접근할 권한이 없습니다')
    if page=='notes' and method not in ('GET','HEAD','OPTIONS') and value['role']!='admin':raise HTTPException(403,'관리자 권한이 필요합니다')

def summary(db,user):
    value=access(db,user)
    return {'username':user.username,'role':value['role'],'pages':page_policy.effective(PROJECT,value['role'],value['pages']),'availablePages':page_policy.PAGES[PROJECT],'canManageUsers':value['role']=='admin','passwordMinLength':8}

def validate_password(password):
    if not isinstance(password,str) or len(password)<8 or len(password.encode('utf-8'))>72:raise HTTPException(400,'비밀번호는 8자 이상, UTF-8 72바이트 이하로 입력하세요')
def validate(username,role,pages):
    try:
        username=page_policy.normalize_username(username)
        if len(username)>50:raise ValueError('아이디는 50자 이하로 입력하세요')
        return username,page_policy.normalize(PROJECT,role,pages)
    except ValueError as error:raise HTTPException(400,str(error)) from error

def list_users(db):
    return [{'username':u.username,'role':access(db,u)['role'],'pages':access(db,u)['pages']} for u in db.query(User).order_by(User.username).all()]

def create(db,username,password,role,pages):
    username,pages=validate(username,role,pages);validate_password(password)
    try:
        user=User(username=username,hashed_password=hash_password(password),is_active=True)
        db.add(user);db.flush()
        db.add(UserAccess(user_id=user.id,role=role,pages=json.dumps(pages),token_version=0));db.commit()
    except IntegrityError:
        db.rollback();raise HTTPException(409,'이미 존재하는 사용자입니다') from None
    return {'ok':True,'username':username}

def edit(db,username,changes):
    db.execute(update(AccessState).where(AccessState.id==1).values(id=1))
    user=db.query(User).filter(User.username==username).first()
    if user is None:raise HTTPException(404,'사용자가 없습니다')
    value=access(db,user);role=changes.get('role',value['role']);pages=changes.get('pages',value['pages'])
    _,pages=validate(username,role,pages)
    if user.is_active and value['role']=='admin' and role!='admin' and db.query(UserAccess).join(User,User.id==UserAccess.user_id).filter(UserAccess.role=='admin',User.is_active.is_(True)).count()<=1:raise HTTPException(409,'마지막 관리자는 강등할 수 없습니다')
    row=db.get(UserAccess,user.id)
    if row is None:row=UserAccess(user_id=user.id,token_version=0);db.add(row)
    row.role=role;row.pages=json.dumps(pages)
    if 'password' in changes:
        validate_password(changes['password']);user.hashed_password=hash_password(changes['password']);row.token_version+=1
    db.commit();return {'ok':True}

def change_password(db,user,current,new,confirm):
    if new!=confirm:raise HTTPException(400,'새 비밀번호가 일치하지 않습니다')
    validate_password(new)
    db.execute(update(AccessState).where(AccessState.id==1).values(id=1))
    db.refresh(user)
    if not verify_password(current,user.hashed_password):raise HTTPException(403,'현재 비밀번호가 올바르지 않습니다')
    row=db.get(UserAccess,user.id)
    if row is None:row=UserAccess(user_id=user.id,role='viewer',pages='[]',token_version=0);db.add(row)
    user.hashed_password=hash_password(new);row.token_version+=1;db.commit()
    return {'ok':True,'reauthenticate':True}
