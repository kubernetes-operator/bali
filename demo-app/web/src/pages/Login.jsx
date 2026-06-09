// 로그인 페이지 컴포넌트
// 사용자명/비밀번호를 입력받아 API에 로그인 요청을 보낸다

import { useState } from "react";
import axios from "axios";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");

  // 로그인 요청 핸들러
  const handleSubmit = async () => {
    try {
      setError("");
      const res = await axios.post("/api/auth/login", { username, password });
      onLogin(res.data.access_token);
    } catch {
      setError("아이디 또는 비밀번호가 올바르지 않습니다.");
    }
  };

  return (
    <div>
      <h2>로그인</h2>
      <input
        placeholder="아이디"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={{ display: "block", marginBottom: 8, width: "100%", padding: 8 }}
      />
      <input
        type="password"
        placeholder="비밀번호"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ display: "block", marginBottom: 8, width: "100%", padding: 8 }}
      />
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={handleSubmit} style={{ padding: "8px 24px" }}>로그인</button>
      <p style={{ marginTop: 12, fontSize: 12, color: "#888" }}>
        테스트 계정: admin / password123
      </p>
    </div>
  );
}

export default Login;
