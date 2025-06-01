import React, { useState } from "react";
import api from "../api/api";

function UpdateSectorPage() {
  const [companyName, setCompanyName] = useState("");
  const [sector, setSector] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(""); setError("");
    try {
      await api.put("/admin/companies/sector", {
        company_name: companyName,
        sector: sector
      });
      setResult("섹터 수정 완료!");
    } catch (err) {
      setError("수정 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>기업 섹터 수정</h2>
      <input value={companyName} onChange={e => setCompanyName(e.target.value)} placeholder="기업명" /><br />
      <input value={sector} onChange={e => setSector(e.target.value)} placeholder="새 섹터" /><br />
      <button type="submit">수정</button>
      {result && <div style={{ color: "green" }}>{result}</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
    </form>
  );
}

export default UpdateSectorPage;
