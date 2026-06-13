# React 앱 이미지 빌드 (멀티스테이지)
# 1단계: Node로 빌드, 2단계: Nginx로 서빙

# 1단계: 빌드
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

# 2단계: Nginx 서빙
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
