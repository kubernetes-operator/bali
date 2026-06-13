# FastAPI 앱 진입점
# 라우터 등록, CORS 설정, 헬스체크 엔드포인트를 정의한다

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, notes

# FastAPI 인스턴스 생성
app = FastAPI(
    title="demo-app API",
    description="로그인 + 텍스트 입출력 데모 API",
    version="0.1.0",
    # /docs 에서 Swagger UI 확인 가능
    # /redoc 에서 ReDoc UI 확인 가능
)

# CORS 설정
# React 개발 서버(3000)와 K8s NodePort(30000)에서의 요청을 허용한다
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React 로컬 개발 서버
        "http://localhost:30000",  # K8s NodePort
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
# prefix: URL 접두사, tags: Swagger UI 그룹명
app.include_router(auth.router,  prefix="/api/auth",  tags=["인증"])
app.include_router(notes.router, prefix="/api/notes", tags=["노트"])


@app.get("/health", tags=["시스템"])
def health_check():
    """
    헬스체크 엔드포인트
    - K8s Liveness/Readiness Probe에서 사용한다
    - DB 연결 없이 앱 기동 여부만 확인한다
    """
    return {"status": "ok", "version": "0.1.0"}
