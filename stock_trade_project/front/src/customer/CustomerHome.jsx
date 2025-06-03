import React from "react";
import { useNavigate } from "react-router-dom";

function CustomerHome() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token"); // 토큰 삭제
    navigate("/login"); // 로그인 페이지로 이동
  };

  return (
    <div>
      <h2>고객 기능</h2>
      <button onClick={handleLogout} style={{ float: "right" }}>로그아웃</button>
      <div style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "200px" }}>
        <button onClick={() => navigate("/customer/deposit-withdraw")}>입출금</button>
        <button onClick={() => navigate("/customer/companies")}>기업 목록 조회</button>
        <button onClick={() => navigate("/customer/orders")}>주문 조회/취소</button>
        <button onClick={() => navigate("/customer/balance")}>잔고 조회</button>
        <button onClick={() => navigate("/customer/portfolio")}>포트폴리오 비중</button>
      </div>
    </div>
  );
}

export default CustomerHome;
