import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function PortfolioWeightPage() {
  const [portfolio, setPortfolio] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/customer/portfolio/weight")
      .then(res => setPortfolio(res.data.portfolio))
      .catch(err => setError("포트폴리오 조회 실패: " + (err.response?.data?.detail || err.message)));
  }, []);

  return (
    <div>
      <h2>섹터별 자산 비중</h2>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <button onClick={() => navigate("/customer/home")} style={{ float: "right" }}>홈 페이지</button>
      <table border="1">
        <thead>
          <tr>
            <th>섹터</th>
            <th>비중(%)</th>
          </tr>
        </thead>
        <tbody>
          {portfolio.map((item, idx) => (
            <tr key={idx}>
              <td>{item.sector}</td>
              <td>{item.weight}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PortfolioWeightPage;
