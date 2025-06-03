import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function UpdateSectorPage() {
  const [companyName, setCompanyName] = useState("");
  const [sector, setSector] = useState("");
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(""); setError("");
    try {
      await api.put("/admin/companies/sector", {
        company_name: companyName,
        sector: sector
      });
      setResult("섹터 수정 완료!");
      fetchCompanies(); // 수정 후 목록 갱신
    } catch (err) {
      setError("수정 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>기업 섹터 수정</h2>
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
      <input value={companyName} onChange={e => setCompanyName(e.target.value)} placeholder="기업명" /><br />
      <input value={sector} onChange={e => setSector(e.target.value)} placeholder="새 섹터" /><br />
      <button type="submit">수정</button>
      {result && <div style={{ color: "green" }}>{result}</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
    </form>
  );
}

export default UpdateSectorPage;
