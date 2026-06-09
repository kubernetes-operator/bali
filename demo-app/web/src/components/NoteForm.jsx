// 노트 입력 폼 컴포넌트
// 텍스트를 입력하고 저장 버튼을 누르면 부모 컴포넌트의 onSave를 호출한다

import { useState } from "react";

function NoteForm({ onSave }) {
  const [content, setContent] = useState("");

  // 저장 핸들러 — 빈 내용은 저장하지 않는다
  const handleSave = () => {
    if (!content.trim()) return;
    onSave(content);
    setContent("");
  };

  return (
    <div>
      <textarea
        rows={3}
        placeholder="노트를 입력하세요..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
        style={{ width: "100%", padding: 8, boxSizing: "border-box" }}
      />
      <button onClick={handleSave} style={{ marginTop: 6, padding: "6px 20px" }}>
        저장
      </button>
    </div>
  );
}

export default NoteForm;
