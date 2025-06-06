import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

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
    <div className="min-h-screen bg-gray-100 py-10 px-4">
      <div className="max-w-xl mx-auto bg-white p-6 rounded-lg shadow-md space-y-6">
        {/* 헤더 */}
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold">📊 섹터별 자산 비중</h2>
          <button
            onClick={() => navigate("/customer/home")}
            className="p-2 rounded hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        {/* 에러 메시지 */}
        {error && <div className="text-red-500 text-sm">{error}</div>}

        {/* 테이블 */}
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300 text-center text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 border">섹터</th>
                <th className="px-4 py-2 border">비중 (%)</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.map((item, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-4 py-2 border">{item.sector}</td>
                  <td className="px-4 py-2 border">{item.weight}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default PortfolioWeightPage;
