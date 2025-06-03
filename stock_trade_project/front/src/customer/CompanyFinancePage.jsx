import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import api from "../api/api";

function CompanyFinancePage() {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const initialCompanyName = params.get("name") || "";

  const [companyName, setCompanyName] = useState(initialCompanyName);
  const [finance, setFinance] = useState(null);
  const [error, setError] = useState("");
  const [companies, setCompanies] = useState([]);

  // 기업 목록 캐싱
  useEffect(() => {
    api.get("/customer/companies").then(res => setCompanies(res.data));
  }, []);

  // 페이지 진입 시 쿼리스트링으로 받은 기업명으로 바로 조회
  useEffect(() => {
    if (initialCompanyName && companies.some(c => c.name === initialCompanyName)) {
      handleFinance(initialCompanyName);
    }
    // eslint-disable-next-line
  }, [companies, initialCompanyName]);

  // 재무정보 조회 함수 분리
  const handleFinance = async (name = companyName) => {
    setFinance(null); setError("");
    if (!companies.some(c => c.name === name)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    try {
      const res = await api.get(`/customer/companies/${name}/info`);
      setFinance(res.data);
    } catch (err) {
      setError("재무정보 조회 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <button onClick={() => window.history.back()} style={{ float: "right" }}>이전 페이지</button>
      <h2>기업 재무정보 조회</h2>
      <input
        type="text"
        value={companyName}
        onChange={e => setCompanyName(e.target.value)}
        placeholder="기업명 입력"
      />
      <button onClick={() => handleFinance()}>재무정보 조회</button>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {finance && (
        <table border="1" style={{ marginTop: "15px" }}>
          <thead>
            <tr><th>연도</th><th>매출</th><th>영업이익</th><th>순이익</th></tr>
          </thead>
          <tbody>
            {finance.map((f, i) => (
              <tr key={i}>
                <td>{f.year}</td>
                <td>{f.sales}</td>
                <td>{f.business_profits}</td>
                <td>{f.pure_profits}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default CompanyFinancePage;
