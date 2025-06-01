import React, { useState } from "react";
import api from "../api/api";

function DeleteCompanyPage() {
  const [companyName, setCompanyName] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const handleDelete = async () => {
    setResult(""); setError("");
    try {
      await api.delete(`/admin/companies/${encodeURIComponent(companyName)}`);
      setResult("기업 삭제 완료!");
    } catch (err) {
      setError("삭제 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h2>기업 상장 폐지</h2>
      <input value={companyName} onChange={e => setCompanyName(e.target.value)} placeholder="기업명" />
      <button onClick={handleDelete}>삭제</button>
      {result && <div style={{ color: "green" }}>{result}</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
    </div>
  );
}

export default DeleteCompanyPage;
