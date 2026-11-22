"""추가 웹 역할/페이지와 기존 JWT·메모 소유권의 실제 HTTP 회귀."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import json
import pytest
import os
import uuid
from sqlalchemy import text
from fastapi import FastAPI,HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import get_db
from models.schemas import Base,User,Note,UserAccess
from core.auth_service import hash_password,create_access_token,verify_password
from core import web_access
from routers import auth,notes

PASSWORD='native-fixture-password'

@pytest.fixture
def isolated_engine(tmp_path):
    dsn=os.environ.get('WS_TEST_POSTGRES_DSN');admin=None;schema=None
    if dsn:
        if dsn!='postgresql://ws_test:ws_test_fixture@ws-platform-postgres:5432/ws_test':raise RuntimeError('Only the dedicated disposable PostgreSQL is permitted')
        admin=create_engine(dsn);schema='ws_test_'+uuid.uuid4().hex
        with admin.begin() as conn:conn.execute(text('CREATE SCHEMA '+schema))
        engine=create_engine(dsn,connect_args={'options':'-csearch_path='+schema})
    else:engine=create_engine('sqlite:///'+str(tmp_path/'accounts.db'),connect_args={'check_same_thread':False})
    try:yield engine
    finally:
        engine.dispose()
        if admin:
            with admin.begin() as conn:conn.execute(text('DROP SCHEMA '+schema+' CASCADE'))
            admin.dispose()

@pytest.fixture
def platform(isolated_engine):
    engine=isolated_engine
    Base.metadata.create_all(engine);factory=sessionmaker(bind=engine)
    with factory() as db:
        user=User(username='native-admin',hashed_password=hash_password(PASSWORD),is_active=True);db.add(user);db.flush()
        db.add(Note(content='existing fixture note',user_id=user.id));db.commit()
    web_access.migrate(engine)
    app=FastAPI();app.include_router(auth.router,prefix='/api/auth');app.include_router(notes.router,prefix='/api/notes')
    def override():
        with factory() as db:yield db
    app.dependency_overrides[get_db]=override
    with TestClient(app) as client:yield engine,factory,client
    engine.dispose()

def headers(client,username='native-admin',password=PASSWORD):
    response=client.post('/api/auth/login',json={'username':username,'password':password})
    assert response.status_code==200,response.text
    assert set(response.json())=={'access_token','token_type','username'}
    return {'Authorization':'Bearer '+response.json()['access_token']}

def test_additive_migration_preserves_hash_notes_and_old_jwt(platform):
    engine,factory,client=platform
    with factory() as db:
        before=[(u.id,u.username,u.hashed_password,u.email,u.is_active) for u in db.query(User)]
        note_before=[(n.id,n.user_id,n.content) for n in db.query(Note)]
    web_access.migrate(engine);web_access.migrate(engine)
    with factory() as db:
        assert before==[(u.id,u.username,u.hashed_password,u.email,u.is_active) for u in db.query(User)]
        assert note_before==[(n.id,n.user_id,n.content) for n in db.query(Note)]
    old_token=create_access_token({'sub':'native-admin'})
    assert client.get('/api/notes/',headers={'Authorization':'Bearer '+old_token}).status_code==200
    assert client.get('/api/auth/ui/session',headers={'Authorization':'Bearer '+old_token}).json()['canManageUsers']

def test_viewer_grants_and_new_account_are_server_enforced(platform):
    _,_,client=platform;admin=headers(client)
    response=client.post('/api/auth/users',headers=admin,json={'username':'reader','password':'reader-fixture-password','pages':['notes']})
    assert response.status_code==200,response.text
    reader=headers(client,'reader','reader-fixture-password')
    assert client.get('/api/notes/',headers=reader).json()==[]
    assert client.post('/api/notes/',headers=reader,json={'content':'not allowed'}).status_code==403
    assert client.get('/api/auth/users',headers=reader).status_code==403
    assert client.post('/api/auth/users',headers=reader,json={'username':'forged','password':PASSWORD,'role':'admin'}).status_code==403
    assert client.get('/api/auth/ui/session',headers=reader).json()['pages']==['notes','settings']
    assert client.patch('/api/auth/users/reader',headers=admin,json={'pages':[]}).status_code==200
    assert client.get('/api/notes/',headers=reader).status_code==403
    assert client.get('/api/auth/ui/session',headers=reader).json()['pages']==['settings']

def test_new_admin_still_cannot_read_another_users_note(platform):
    _,_,client=platform;admin=headers(client)
    client.post('/api/auth/users',headers=admin,json={'username':'other-admin','password':PASSWORD,'role':'admin','pages':[]})
    other=headers(client,'other-admin')
    original=client.get('/api/notes/',headers=admin).json()[0]
    assert client.get('/api/notes/'+str(original['id']),headers=other).status_code==404
    own=client.post('/api/notes/',headers=other,json={'content':'my fixture note'})
    assert own.status_code==201,own.text
    assert [n['content'] for n in client.get('/api/notes/',headers=other).json()]==['my fixture note']
    assert client.get('/api/notes/'+str(own.json()['id']),headers=admin).status_code==404

def test_password_confirmation_and_current_password_revoke_old_tokens(platform):
    engine,factory,client=platform;original=headers(client)
    old={'Authorization':'Bearer '+create_access_token({'sub':'native-admin'})}
    body={'current_password':PASSWORD,'new_password':'new-fixture-password','confirm_password':'different-password'}
    assert client.post('/api/auth/ui/password',headers=original,json=body).status_code==400
    body['confirm_password']=body['new_password'];body['current_password']='incorrect'
    assert client.post('/api/auth/ui/password',headers=original,json=body).status_code==403
    assert client.get('/api/notes/',headers=original).status_code==200
    body['current_password']=PASSWORD
    assert client.post('/api/auth/ui/password',headers=original,json=body).status_code==200
    assert client.get('/api/notes/',headers=original).status_code==401
    assert client.get('/api/notes/',headers=old).status_code==401
    assert client.post('/api/auth/login',json={'username':'native-admin','password':PASSWORD}).status_code==401
    updated=headers(client,password=body['new_password'])
    assert client.get('/api/notes/',headers=updated).status_code==200
    web_access.migrate(engine)
    assert client.get('/api/notes/',headers=original).status_code==401

def test_admin_reset_revokes_existing_session_and_last_admin_guard(platform):
    _,_,client=platform;admin=headers(client)
    assert client.patch('/api/auth/users/native-admin',headers=admin,json={'role':'viewer','pages':[]}).status_code==409
    client.post('/api/auth/users',headers=admin,json={'username':'reader','password':PASSWORD,'pages':['notes']})
    old=headers(client,'reader')
    assert client.patch('/api/auth/users/reader',headers=admin,json={'password':'reset-fixture-password'}).status_code==200
    assert client.get('/api/notes/',headers=old).status_code==401
    assert client.get('/api/notes/',headers=headers(client,'reader','reset-fixture-password')).status_code==200

@pytest.mark.parametrize('payload',[{'username':'bad/name','pages':[]},{'username':'x'*51,'pages':[]},{'username':'bad','pages':['unknown']},{'username':'bad','pages':['users']},{'username':'bad','pages':[],'password':'짧은'*20}])
def test_invalid_account_and_grants_do_not_persist(platform,payload):
    _,factory,client=platform;admin=headers(client)
    response=client.post('/api/auth/users',headers=admin,json={'password':PASSWORD,**payload})
    assert response.status_code==400,response.text
    with factory() as db:assert db.query(User).count()==1

def test_missing_metadata_fails_closed(platform):
    _,factory,client=platform
    with factory() as db:
        user=User(username='unmanaged',hashed_password=hash_password(PASSWORD),is_active=True);db.add(user);db.commit()
    h=headers(client,'unmanaged')
    assert client.get('/api/notes/',headers=h).status_code==403
    assert client.get('/api/auth/users',headers=h).status_code==403
    assert client.get('/api/auth/ui/session',headers=h).json()['pages']==['settings']

def test_concurrent_demotion_preserves_last_admin(isolated_engine):
    engine=isolated_engine
    Base.metadata.create_all(engine);factory=sessionmaker(bind=engine)
    with factory() as db:
        for username in ('first','second'):db.add(User(username=username,hashed_password='fixture-hash',is_active=True))
        db.commit()
    web_access.migrate(engine);barrier=Barrier(2)
    def demote(username):
        barrier.wait(timeout=5)
        with factory() as db:
            try:return web_access.edit(db,username,{'role':'viewer','pages':[]})
            except HTTPException as error:return error.status_code
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(demote,['first','second']))
    assert results.count(409)==1
    with factory() as db:assert db.query(UserAccess).filter(UserAccess.role=='admin').count()==1
    engine.dispose()


def test_password_change_during_login_cannot_issue_valid_old_password_token(platform,monkeypatch):
    _,_,client=platform
    original=auth.authenticate_user
    def change_during_login(db,username,password):
        user=original(db,username,password)
        if user:web_access.change_password(db,user,PASSWORD,'raced-new-password','raced-new-password')
        return user
    monkeypatch.setattr(auth,'authenticate_user',change_during_login)
    response=client.post('/api/auth/login',json={'username':'native-admin','password':PASSWORD})
    if response.status_code==200:
        h={'Authorization':'Bearer '+response.json()['access_token']}
        assert client.get('/api/auth/ui/session',headers=h).status_code==401
    else:assert response.status_code==401

def test_inactive_admin_can_be_demoted_without_removing_active_admin(platform):
    engine,factory,client=platform
    with factory() as db:
        db.add(User(username='inactive-admin',hashed_password='fixture-hash',is_active=False));db.commit()
    web_access.migrate(engine)
    response=client.patch('/api/auth/users/inactive-admin',headers=headers(client),json={'role':'viewer','pages':[]})
    assert response.status_code==200,response.text
