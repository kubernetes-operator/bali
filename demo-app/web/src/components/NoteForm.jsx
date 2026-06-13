// 노트 입력 폼 컴포넌트
// CSS Module 대신 인라인 스타일을 사용한다

import { useState } from "react";

const S = {
  wrap: {
    background: "#FFFFFF", border: "1px solid #E4E2DC",
    borderRadius: "10px", overflow: "hidden",
  },
  textarea: {
    display: "block", width: "100%", border: "none",
    padding: "14px 16px", resize: "none",
    fontSize: "14px", lineHeight: "1.65",
    fontFamily: "'Inter', -apple-system, sans-serif",
    outline: "none", boxSizing: "border-box",
    background: "transparent",
  },
  footer: {
    display: "flex", alignItems: "center",
    justifyContent: "space-between",
    padding: "8px 12px 10px",
    borderTop: "1px solid #E4E2DC", background: "#FAFAF8",
  },
  counter: { fontSize: "12px", color: "#6B6966" },
  counterWarn: { fontSize: "12px", color: "#DC2626" },
  button: {
    padding: "6px 14px", background: "#2563EB",
    color: "#fff", border: "none", borderRadius: "6px",
    fontSize: "13px", fontWeight: "500", cursor: "pointer",
    fontFamily: "inherit",
  },
};

function NoteForm({ onSave, saving }) {
  const [content, setContent] = useState("");
  const remaining = 500 - content.length;

  const handleSave = () => {
    if (!content.trim() || saving) return;
    onSave(content.trim());
    setContent("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) handleSave();
  };

  return (
    <div style={S.wrap}>
      <textarea
        rows={3} placeholder="메모를 입력하세요..."
        value={content}
        onChange={(e) => { if (e.target.value.length <= 500) setContent(e.target.value); }}
        onKeyDown={handleKeyDown}
        style={S.textarea}
      />
      <div style={S.footer}>
        <span style={remaining < 50 ? S.counterWarn : S.counter}>
          {remaining}자 남음
        </span>
        <button style={{ ...S.button, opacity: (!content.trim() || saving) ? 0.5 : 1 }}
          onClick={handleSave} disabled={!content.trim() || saving}>
          {saving ? "저장 중..." : "저장  Ctrl+Enter"}
        </button>
      </div>
    </div>
  );
}

export default NoteForm;
