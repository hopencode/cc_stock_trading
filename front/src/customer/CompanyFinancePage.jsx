import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import api from "../api/api";
import { ArrowLeftIcon } from "@heroicons/react/24/outline";

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
    <div className="min-h-screen bg-white flex justify-center items-start p-4">
      <div className="w-full max-w-3xl bg-gray-50 p-6 rounded-2xl shadow-md space-y-6 mt-10">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold">📂 기업 재무정보 조회</h2>
          <button
            onClick={() => window.history.back()}
            className="p-2 hover:bg-gray-100 rounded transition"
            title="이전 페이지"
          >
            <ArrowLeftIcon className="h-5 w-5 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        <div className="flex gap-3">
          <input
            type="text"
            value={companyName}
            onChange={e => setCompanyName(e.target.value)}
            placeholder="기업명 입력"
            className="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={() => handleFinance()}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition"
          >
            조회
          </button>
        </div>

        {error && <div className="text-red-500 font-medium">{error}</div>}

        {finance && (
          <div className="overflow-x-auto mt-4">
            <table className="w-full table-auto border border-gray-300 rounded">
              <thead className="bg-gray-100 text-left">
                <tr>
                  <th className="p-2 border">연도</th>
                  <th className="p-2 border">매출</th>
                  <th className="p-2 border">영업이익</th>
                  <th className="p-2 border">순이익</th>
                </tr>
              </thead>
              <tbody>
                {finance.map((f, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    <td className="p-2 border">{f.year}</td>
                    <td className="p-2 border">{Number(f.sales).toLocaleString()} 원</td>
                    <td className="p-2 border">{Number(f.business_profits).toLocaleString()} 원</td>
                    <td className="p-2 border">{Number(f.pure_profits).toLocaleString()} 원</td>
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
