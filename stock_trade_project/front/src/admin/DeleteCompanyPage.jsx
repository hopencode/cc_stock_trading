import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function DeleteCompanyPage() {
  const [companyName, setCompanyName] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [companies, setCompanies] = useState([]);
  const navigate = useNavigate();

  // 기업 목록 불러오기
  const fetchCompanies = () => {
    api.get("/admin/companies").then(res => setCompanies(res.data));
  };

  useEffect(() => {
    fetchCompanies();
  }, []);

  const handleDelete = async () => {
    setResult(""); setError("");
    try {
      await api.delete(`/admin/companies/${encodeURIComponent(companyName)}`);
      setResult("기업 삭제 완료!");
      fetchCompanies(); // 삭제 후 목록 갱신
    } catch (err) {
      setError("삭제 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h2>기업 상장 폐지</h2>
      <button onClick={() => navigate("/admin/home")} style={{ float: "right" }}>홈 페이지</button>
      <table border="1">
        <thead>
          <tr>
            <th>기업명</th><th>섹터</th><th>현재가</th><th>총발행주식</th><th>시가총액</th>
          </tr>
        </thead>
        <tbody>
          {companies.map(c => (
            <tr key={c.name}>
              <td>{c.name}</td>
              <td>{c.sector}</td>
              <td>{c.price}</td>
              <td>{c.stock_num}</td>
              <td>{c.total_price}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <br />
      <input value={companyName} onChange={e => setCompanyName(e.target.value)} placeholder="기업명" />
      <button onClick={handleDelete}>삭제</button>
      {result && <div style={{ color: "green" }}>{result}</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
    </div>
  );
}

export default DeleteCompanyPage;
