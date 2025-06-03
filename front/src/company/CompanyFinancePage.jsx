import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

function CompanyFinancePage() {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const initialCompanyName = params.get("name") || "";

  const [companyName, setCompanyName] = useState(initialCompanyName);
  const [finance, setFinance] = useState(null);
  const [error, setError] = useState("");
  const [companies, setCompanies] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/company/companies").then(res => setCompanies(res.data));
  }, []);

  useEffect(() => {
    if (initialCompanyName && companies.some(c => c.name === initialCompanyName)) {
      handleFinance(initialCompanyName);
    }
    // eslint-disable-next-line
  }, [companies, initialCompanyName]);

  const handleFinance = async (name = companyName) => {
    setFinance(null); setError("");
    if (!companies.some(c => c.name === name)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    try {
      const res = await api.get(`/company/companies/${name}/info`);
      setFinance(res.data);
    } catch (err) {
      setError("재무정보 조회 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center p-4">
      <div className="w-full max-w-3xl bg-white p-6 rounded-2xl shadow-lg space-y-6">
        {/* 헤더 */}
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold">🏢 기업 재무정보 조회</h2>
          <button
            onClick={() => navigate("/company/home")}
            className="p-2 rounded hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        {/* 입력 및 버튼 */}
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="기업명 입력"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={handleFinance}
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition"
          >
            재무정보 조회
          </button>
        </div>

        {/* 오류 메시지 */}
        {error && <div className="text-red-500 text-sm">{error}</div>}

        {/* 테이블 */}
        {finance && (
          <div className="overflow-x-auto">
            <table className="min-w-full border border-gray-300 text-sm text-center mt-4">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-2 border">연도</th>
                  <th className="px-4 py-2 border">매출</th>
                  <th className="px-4 py-2 border">영업이익</th>
                  <th className="px-4 py-2 border">순이익</th>
                </tr>
              </thead>
              <tbody>
                {finance.map((f, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    <td className="px-4 py-2 border">{f.year}</td>
                    <td className="px-4 py-2 border">{f.sales}</td>
                    <td className="px-4 py-2 border">{f.business_profits}</td>
                    <td className="px-4 py-2 border">{f.pure_profits}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default CompanyFinancePage;
