import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function DepositWithdrawPage() {
  const [amount, setAmount] = useState("");
  const [result, setResult] = useState("");
  const navigate = useNavigate();

  const handleDeposit = async () => {
    if (!amount || isNaN(amount) || Number(amount) <= 0) {
      setResult("올바른 금액을 입력하세요.");
      return;
    }
    try {
      const res = await api.post("/customer/deposit", { amount: Number(amount) });
      setResult(res.data.message + " (잔액: " + res.data.balance + ")");
    } catch (err) {
      setResult("입금 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleWithdraw = async () => {
    if (!amount || isNaN(amount) || Number(amount) <= 0) {
      setResult("올바른 금액을 입력하세요.");
      return;
    }
    try {
      const res = await api.post("/customer/withdraw", { amount: Number(amount) });
      setResult(res.data.message + " (잔액: " + res.data.balance + ")");
    } catch (err) {
      setResult("출금 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h2>입금 / 출금</h2>
      <button onClick={() => navigate("/customer/home")} style={{ float: "right" }}>홈 페이지</button>
      <input
        type="number"
        value={amount}
        onChange={e => setAmount(e.target.value)}
        placeholder="금액"
        min="1"
      />
      <div style={{ marginTop: "10px", display: "flex", gap: "10px" }}>
        <button onClick={handleDeposit}>입금</button>
        <button onClick={handleWithdraw}>출금</button>
      </div>
      <div style={{ marginTop: "15px" }}>{result}</div>
    </div>
  );
}

export default DepositWithdrawPage;
