// API 클라이언트 모듈
// Axios 인스턴스를 생성하고 JWT 토큰 자동 첨부 인터셉터를 설정한다
// 모든 API 호출은 이 클라이언트를 통해 이루어진다

import axios from "axios";

// Axios 인스턴스 생성
// baseURL: K8s 환경에서는 API Service 주소로 변경 필요
const apiClient = axios.create({
//  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
  baseURL: "",
  headers: { "Content-Type": "application/json" },
  timeout: 10000, // 10초 타임아웃
});

// 요청 인터셉터: 모든 요청에 JWT 토큰을 자동으로 첨부한다
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 응답 인터셉터: 401 응답 시 토큰을 삭제하고 로그인 페이지로 이동한다
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 토큰 만료 또는 유효하지 않은 토큰 → 자동 로그아웃
      localStorage.removeItem("access_token");
      localStorage.removeItem("username");
      window.location.href = "/";
    }
    return Promise.reject(error);
  }
);

// ----------------------------------------------------------------
// API 함수 정의
// ----------------------------------------------------------------

export const authAPI = {
  /** 로그인: username/password로 JWT 토큰을 발급받는다 */
  login: (username, password) =>
    apiClient.post("/api/auth/login", { username, password }),
};

export const notesAPI = {
  /** 노트 목록 조회: 로그인한 사용자의 모든 노트를 반환한다 */
  getAll: () => apiClient.get("/api/notes/"),

  /** 노트 생성: 새 노트를 저장하고 저장된 노트를 반환한다 */
  create: (content) => apiClient.post("/api/notes/", { content }),
};

export default apiClient;
