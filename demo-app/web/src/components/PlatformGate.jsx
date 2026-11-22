// 페이지 권한을 확인한 뒤 업무 컴포넌트를 마운트한다. 실제 접근 제한은 서버가 수행한다.
import { useEffect, useState } from "react";
import apiClient from "../api/client";
import Notes from "../pages/Notes";

export default function PlatformGate({ username, onLogout }) {
  const [access, setAccess] = useState(null);
  const [error, setError] = useState("");
  const [retry, setRetry] = useState(0);
  useEffect(() => {
    let active = true;
    setError("");
    apiClient.get("/api/auth/ui/session").then(({ data }) => {
      if (!Array.isArray(data.pages) || !["admin", "viewer"].includes(data.role)) throw new Error("invalid session");
      if (active) setAccess(data);
    }).catch(() => { if (active) setError("계정 권한을 확인하지 못했습니다. 다시 시도해 주세요."); });
    const refresh = () => {
      const sdk = window.WSSettings;
      if (active && sdk && Array.isArray(sdk.pages) && ["admin", "viewer"].includes(sdk.role)) setAccess({ pages: sdk.pages, role: sdk.role });
    };
    document.addEventListener("ws:settings:ready", refresh);
    return () => { active = false; document.removeEventListener("ws:settings:ready", refresh); };
  }, [retry]);
  if (access && access.pages.includes("notes")) return <Notes username={username} onLogout={onLogout} canWrite={access.role === "admin"} />;
  return <div style={{ padding: 24 }}>
    <header><h1>개인 설정</h1><button type="button" onClick={onLogout}>로그아웃</button></header>
    {!access && !error && <p role="status">계정 권한을 확인하고 있습니다.</p>}
    {error && <><p role="alert">{error}</p><button type="button" onClick={() => setRetry(value => value + 1)}>다시 시도</button></>}
    {access && <><p>이 계정에 허용된 업무 페이지가 없습니다. 개인 설정에서 비밀번호를 변경할 수 있습니다.</p><button type="button" className="ws-security-open" onClick={() => window.WSSettings.open("personal")}>개인 설정 열기</button></>}
  </div>;
}
