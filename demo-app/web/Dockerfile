# React 앱 멀티스테이지 빌드
# 1단계: Node로 npm run build 실행
# 2단계: Nginx로 빌드 결과물 서빙

# ── 1단계: 빌드 ──────────────────────────────────────────────
FROM node:18-alpine AS builder

WORKDIR /app

# package.json 먼저 복사하여 레이어 캐시 활용
# 소스 변경 없이 의존성이 동일하면 npm install을 재실행하지 않는다
COPY package.json ./
RUN npm install

# 소스 전체 복사 후 프로덕션 빌드 실행
COPY . .

# CI=false: 경고를 에러로 취급하지 않음 (빌드 실패 방지)
ENV CI=false
RUN npm run build

# 빌드 결과 확인 (디버깅용)
RUN ls -la /app/build/ && ls -la /app/build/static/

# ── 2단계: Nginx 서빙 ─────────────────────────────────────────
FROM nginx:1.25-alpine

# 빌드 결과물을 Nginx 서빙 디렉토리로 복사
COPY --from=builder /app/build /usr/share/nginx/html

# 포트 노출
EXPOSE 80

# Nginx 포그라운드 실행
CMD ["nginx", "-g", "daemon off;"]
