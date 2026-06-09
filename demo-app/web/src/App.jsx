// 앱 루트 컴포넌트
// 로그인 상태에 따라 Login 또는 Notes 페이지를 렌더링한다

import { useState } from "react";
import Login from "./pages/Login";
import Notes from "./pages/Notes";

function App() {
  // 로그인 토큰 상태 (null이면 비로그인)
  const [token, setToken] = useState(null);

  return (
    <div style={{ maxWidth: "640px", margin: "40px auto", padding: "0 20px" }}>
      {token ? (
        // 로그인 상태: 노트 페이지
        <Notes token={token} onLogout={() => setToken(null)} />
      ) : (
        // 비로그인 상태: 로그인 페이지
        <Login onLogin={(t) => setToken(t)} />
      )}
    </div>
  );
}

export default App;
