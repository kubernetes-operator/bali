// 노트 페이지 컴포넌트
// CSS Module 대신 인라인 스타일을 사용한다

import { useState, useEffect, useCallback } from "react";
import { notesAPI } from "../api/client";
import NoteForm from "../components/NoteForm";

function formatDate(isoString) {
  const d = new Date(isoString);
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}.${pad(d.getMonth()+1)}.${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

const S = {
  container: {
    minHeight: "100vh", background: "#F7F6F3",
    paddingBottom: "48px",
    fontFamily: "'Inter', -apple-system, sans-serif",
  },
  inner: { maxWidth: "640px", margin: "0 auto", padding: "0 20px" },
  header: {
    display: "flex", alignItems: "center",
    justifyContent: "space-between",
    padding: "24px 0 20px",
    borderBottom: "1px solid #E4E2DC", marginBottom: "24px",
  },
  headerLeft: { display: "flex", alignItems: "center", gap: "12px" },
  logo: {
    width: "38px", height: "38px", background: "#2563EB",
    color: "#fff", fontSize: "17px", fontWeight: "600",
    borderRadius: "6px", display: "flex",
    alignItems: "center", justifyContent: "center", flexShrink: 0,
  },
  title: { fontSize: "17px", fontWeight: "600", lineHeight: "1.2", margin: 0 },
  greeting: { fontSize: "12px", color: "#6B6966", marginTop: "1px" },
  logoutBtn: {
    padding: "6px 14px", background: "transparent",
    color: "#6B6966", border: "1px solid #E4E2DC",
    fontSize: "13px", borderRadius: "6px", cursor: "pointer",
    fontFamily: "inherit",
  },
  formSection: { marginBottom: "28px" },
  error: {
    fontSize: "13px", color: "#DC2626",
    background: "#FEF2F2", border: "1px solid #FECACA",
    borderRadius: "6px", padding: "8px 12px", marginBottom: "16px",
  },
  listMeta: { fontSize: "12px", color: "#6B6966", marginBottom: "12px" },
  empty: { textAlign: "center", padding: "48px 0", color: "#6B6966" },
  emptyTitle: { fontSize: "15px", fontWeight: "500", marginBottom: "6px", color: "#1A1917" },
  emptySub: { fontSize: "13px" },
  noteCard: {
    background: "#FFFFFF", border: "1px solid #E4E2DC",
    borderRadius: "10px", padding: "14px 16px", marginBottom: "8px",
  },
  noteContent: {
    fontSize: "14px", lineHeight: "1.65",
    color: "#1A1917", whiteSpace: "pre-wrap",
    wordBreak: "break-word", margin: 0,
  },
  noteMeta: {
    fontSize: "11px", color: "#6B6966",
    marginTop: "8px", fontFamily: "monospace",
  },
};

function Notes({ username, onLogout }) {
  const [notes, setNotes]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving]   = useState(false);
  const [error, setError]     = useState("");

  const fetchNotes = useCallback(async () => {
    try {
      setError("");
      const res = await notesAPI.getAll();
      setNotes(res.data);
    } catch {
      setError("노트를 불러오는 데 실패했습니다.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchNotes(); }, [fetchNotes]);

  const handleSave = async (content) => {
    setSaving(true);
    setError("");
    try {
      const res = await notesAPI.create(content);
      setNotes((prev) => [res.data, ...prev]);
    } catch {
      setError("노트 저장에 실패했습니다.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={S.container}>
      <div style={S.inner}>
        <header style={S.header}>
          <div style={S.headerLeft}>
            <div style={S.logo}>N</div>
            <div>
              <h1 style={S.title}>메모</h1>
              <p style={S.greeting}>{username}님의 메모장</p>
            </div>
          </div>
          <button style={S.logoutBtn} onClick={onLogout}>로그아웃</button>
        </header>

        <section style={S.formSection}>
          <NoteForm onSave={handleSave} saving={saving} />
        </section>

        {error && <p style={S.error}>{error}</p>}

        <section>
          <p style={S.listMeta}>
            {loading ? "불러오는 중..." : `메모 ${notes.length}개`}
          </p>

          {!loading && notes.length === 0 && (
            <div style={S.empty}>
              <p style={S.emptyTitle}>메모가 없습니다</p>
              <p style={S.emptySub}>위 입력창에 첫 메모를 작성해보세요.</p>
            </div>
          )}

          {!loading && notes.map((note) => (
            <div key={note.id} style={S.noteCard}>
              <p style={S.noteContent}>{note.content}</p>
              <p style={S.noteMeta}>{formatDate(note.created_at)}</p>
            </div>
          ))}
        </section>
      </div>
    </div>
  );
}

export default Notes;
