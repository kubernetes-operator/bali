# FastAPI 앱 진입점
# 라우터를 등록하고 앱 설정을 초기화한다

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, notes

# FastAPI 인스턴스 생성
app = FastAPI(
    title="demo-app API",
    description="로그인 + 텍스트 입출력 데모",
    version="0.1.0",
)

# CORS 설정 — React 개발 서버(3000)에서의 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["인증"])
app.include_router(notes.router, prefix="/api/notes", tags=["노트"])


@app.get("/health")
def health_check():
    """헬스체크 엔드포인트 — K8s Liveness Probe용"""
    return {"status": "ok"}
