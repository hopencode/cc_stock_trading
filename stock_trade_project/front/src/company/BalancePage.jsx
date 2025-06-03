import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function BalancePage() {
  const [balance, setBalance] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/company/balance").then(res => setBalance(res.data));
  }, []);

  if (!balance) return <div>로딩 중...</div>;

  return (
    <div>
      <h2>잔고 조회</h2>
      <button onClick={() => navigate("/company/home")} style={{ float: "right" }}>홈 페이지</button>
      <div>현금: {balance.cash} 원</div>
      <div>양도소득: {balance.capital_gain} 원</div>
      <h3>보유 주식</h3>
      <table border="1">
        <thead>
          <tr>
            <th>종목명</th><th>수량</th><th>평균단가</th><th>현재가</th><th>평가금액</th>
          </tr>
        </thead>
        <tbody>
          {balance.stocks.map(s => (
            <tr key={s.stock_name}>
              <td>{s.stock_name}</td>
              <td>{s.stock_count}</td>
              <td>{s.avg_buy_price}</td>
              <td>{s.current_price}</td>
              <td>{s.valuation_amount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BalancePage;
