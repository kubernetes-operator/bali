// 노트 페이지 컴포넌트
// 텍스트 입력/조회 기능을 제공한다

import { useState, useEffect } from "react";
import axios from "axios";
import NoteForm from "../components/NoteForm";

function Notes({ token, onLogout }) {
  const [notes, setNotes] = useState([]);

  // 컴포넌트 마운트 시 노트 목록 조회
  useEffect(() => {
    fetchNotes();
  }, []);

  // 노트 목록 API 호출
  const fetchNotes = async () => {
    const res = await axios.get("/api/notes/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    setNotes(res.data);
  };

  // 노트 저장 후 목록 갱신
  const handleSave = async (content) => {
    await axios.post("/api/notes/", { content }, {
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchNotes();
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h2>노트</h2>
        <button onClick={onLogout}>로그아웃</button>
      </div>
      <NoteForm onSave={handleSave} />
      <ul style={{ marginTop: 16, paddingLeft: 0, listStyle: "none" }}>
        {notes.map((n) => (
          <li key={n.id} style={{ borderBottom: "1px solid #eee", padding: "8px 0" }}>
            {n.content}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Notes;
