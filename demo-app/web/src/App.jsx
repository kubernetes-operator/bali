// 루트 App 컴포넌트
// 로그인 상태를 관리하고 Login 또는 Notes 페이지를 렌더링한다
// localStorage를 사용하여 페이지 새로고침 후에도 로그인 상태를 유지한다

import { useState, useEffect } from "react";
import Login from "./pages/Login";
import Notes from "./pages/Notes";

function App() {
  // localStorage에서 초기 토큰/사용자명을 읽어온다 (새로고침 후 유지)
  const [token, setToken]       = useState(() => localStorage.getItem("access_token"));
  const [username, setUsername] = useState(() => localStorage.getItem("username") || "");

  // 로그인 처리: 토큰과 사용자명을 state와 localStorage에 저장한다
  const handleLogin = (accessToken, user) => {
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("username", user);
    setToken(accessToken);
    setUsername(user);
  };

  // 로그아웃 처리: 토큰과 사용자명을 state와 localStorage에서 삭제한다
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
    setToken(null);
    setUsername("");
  };

  return (
    <div>
      {token ? (
        // 로그인 상태: 노트 페이지 렌더링
        <Notes username={username} onLogout={handleLogout} />
      ) : (
        // 비로그인 상태: 로그인 페이지 렌더링
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
