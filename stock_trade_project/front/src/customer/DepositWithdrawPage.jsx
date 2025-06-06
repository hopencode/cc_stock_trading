import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

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
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold">💰 입금 / 출금</h2>
          <button
            onClick={() => navigate("/customer/home")}
            className="p-2 rounded hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="금액"
          min="1"
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <div className="flex gap-4">
          <button
            onClick={handleDeposit}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md transition"
          >
            입금
          </button>
          <button
            onClick={handleWithdraw}
            className="w-full bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-md transition"
          >
            출금
          </button>
        </div>

        {result && <div className="text-center text-gray-700">{result}</div>}
      </div>
    </div>
  );
}

export default DepositWithdrawPage;
