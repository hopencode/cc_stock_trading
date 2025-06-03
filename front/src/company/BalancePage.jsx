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
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="w-full max-w-3xl bg-white p-6 rounded-2xl shadow-lg space-y-6">
        {/* 상단 헤더 */}
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold">🏦 기업 잔고 조회</h2>
          <button
            onClick={() => navigate("/company/home")}
            className="p-2 rounded hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        {/* 현금 및 양도소득 */}
        <div className="space-y-1 text-gray-700">
          <div>💰 <strong>현금:</strong> {balance.cash.toLocaleString()} 원</div>
          <div>📈 <strong>양도소득:</strong> {balance.capital_gain.toLocaleString()} 원</div>
        </div>

        {/* 보유 주식 테이블 */}
        <div>
          <h3 className="text-lg font-semibold mt-4 mb-2">📊 보유 주식</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full border border-gray-300 text-sm text-center">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-2 border">종목명</th>
                  <th className="px-4 py-2 border">수량</th>
                  <th className="px-4 py-2 border">평균단가</th>
                  <th className="px-4 py-2 border">현재가</th>
                  <th className="px-4 py-2 border">평가금액</th>
                </tr>
              </thead>
              <tbody>
                {balance.stocks.map((s) => (
                  <tr key={s.stock_name} className="hover:bg-gray-50">
                    <td className="px-4 py-2 border">{s.stock_name}</td>
                    <td className="px-4 py-2 border">{s.stock_count}</td>
                    <td className="px-4 py-2 border">{s.avg_buy_price}</td>
                    <td className="px-4 py-2 border">{s.current_price}</td>
                    <td className="px-4 py-2 border font-semibold">{s.valuation_amount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default BalancePage;
