import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

function BalancePage() {
  const [balance, setBalance] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/company/balance").then(res => setBalance(res.data));
  }, []);

  if (!balance) return <div>로딩 중...</div>;

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">
      <div className="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">🏦 기업 잔고 조회</h2>
          <button
            onClick={() => navigate("/customer/home")}
            className="p-2 rounded hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        <div className="grid grid-cols-2 gap-4 text-lg font-medium">
          <div>💰 보유 현금: <span className="text-blue-600">{balance.cash.toLocaleString()} 원</span></div>
          <div>📈 누적 양도소득: <span className="text-green-600">{balance.capital_gain.toLocaleString()} 원</span></div>
        </div>

        <h3 className="text-xl font-semibold mt-6">📦 보유 주식</h3>
        <div className="overflow-x-auto">
          <table className="w-full table-auto border border-gray-300 rounded">
            <thead className="bg-gray-100">
              <tr className="text-left">
                <th className="p-2 border">종목명</th>
                <th className="p-2 border">수량</th>
                <th className="p-2 border">평균단가</th>
                <th className="p-2 border">현재가</th>
                <th className="p-2 border">평가금액</th>
              </tr>
            </thead>
            <tbody>
              {balance.stocks.map((s) => (
                <tr key={s.stock_name} className="hover:bg-gray-50">
                  <td className="p-2 border">{s.stock_name}</td>
                  <td className="p-2 border">{s.stock_count}</td>
                  <td className="p-2 border">{s.avg_buy_price.toLocaleString()}</td>
                  <td className="p-2 border">{s.current_price.toLocaleString()}</td>
                  <td className="p-2 border">{s.valuation_amount.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default BalancePage;
