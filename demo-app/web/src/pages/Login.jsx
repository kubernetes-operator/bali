// 로그인 페이지 컴포넌트
// CSS Module 대신 인라인 스타일을 사용한다 (CRA 환경 호환성)

import { useState } from "react";
import { authAPI } from "../api/client";

const S = {
  container: {
    minHeight: "100vh", display: "flex",
    alignItems: "center", justifyContent: "center",
    padding: "24px", background: "#F7F6F3",
    fontFamily: "'Inter', -apple-system, sans-serif",
  },
  card: {
    width: "100%", maxWidth: "380px",
    background: "#FFFFFF", border: "1px solid #E4E2DC",
    borderRadius: "14px", padding: "36px 32px 28px",
    boxShadow: "0 1px 3px rgba(0,0,0,0.07)",
  },
  header: { textAlign: "center", marginBottom: "28px" },
  logo: {
    width: "44px", height: "44px",
    background: "#2563EB", color: "#fff",
    fontSize: "20px", fontWeight: "600", borderRadius: "10px",
    display: "flex", alignItems: "center", justifyContent: "center",
    margin: "0 auto 14px",
  },
  title: { fontSize: "20px", fontWeight: "600", marginBottom: "6px", margin: "0 0 6px" },
  subtitle: { fontSize: "13px", color: "#6B6966", margin: 0 },
  form: { display: "flex", flexDirection: "column", gap: "14px" },
  field: { display: "flex", flexDirection: "column", gap: "6px" },
  label: { fontSize: "13px", fontWeight: "500" },
  input: {
    fontSize: "14px", padding: "10px 12px",
    border: "1px solid #E4E2DC", borderRadius: "6px",
    outline: "none", fontFamily: "inherit", width: "100%",
    boxSizing: "border-box",
  },
  error: {
    fontSize: "13px", color: "#DC2626",
    background: "#FEF2F2", border: "1px solid #FECACA",
    borderRadius: "6px", padding: "8px 12px", margin: 0,
  },
  button: {
    width: "100%", padding: "10px",
    background: "#2563EB", color: "#fff", border: "none",
    borderRadius: "6px", fontSize: "14px", fontWeight: "500",
    cursor: "pointer", marginTop: "4px", fontFamily: "inherit",
  },
  hint: { marginTop: "20px", textAlign: "center", fontSize: "12px", color: "#6B6966" },
  hintCode: {
    fontFamily: "monospace", fontSize: "11px",
    background: "#F7F6F3", border: "1px solid #E4E2DC",
    borderRadius: "4px", padding: "1px 5px",
  },
};

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      setError("아이디와 비밀번호를 모두 입력해주세요.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await authAPI.login(username, password);
      onLogin(res.data.access_token, res.data.username);
    } catch (err) {
      setError(err.response?.data?.detail || "로그인에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => { if (e.key === "Enter") handleLogin(); };

  return (
    <div style={S.container}>
      <div style={S.card}>
        <div style={S.header}>
          <div style={S.logo}>N</div>
          <h1 style={S.title}>메모 앱</h1>
          <p style={S.subtitle}>로그인하여 메모를 관리하세요</p>
        </div>
        <div style={S.form}>
          <div style={S.field}>
            <label style={S.label} htmlFor="username">아이디</label>
            <input id="username" type="text" placeholder="아이디를 입력하세요"
              value={username} onChange={(e) => setUsername(e.target.value)}
              onKeyDown={handleKeyDown} style={S.input} autoFocus />
          </div>
          <div style={S.field}>
            <label style={S.label} htmlFor="password">비밀번호</label>
            <input id="password" type="password" placeholder="비밀번호를 입력하세요"
              value={password} onChange={(e) => setPassword(e.target.value)}
              onKeyDown={handleKeyDown} style={S.input} />
          </div>
          {error && <p style={S.error}>{error}</p>}
          <button style={{ ...S.button, opacity: loading ? 0.6 : 1 }}
            onClick={handleLogin} disabled={loading}>
            {loading ? "로그인 중..." : "로그인"}
          </button>
        </div>
        <p style={S.hint}>
          테스트 계정: <span style={S.hintCode}>admin</span> / <span style={S.hintCode}>password123</span>
        </p>
      </div>
    </div>
  );
}

export default Login;
