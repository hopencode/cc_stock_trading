import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import api from "../api/api";
import { ArrowLeftIcon } from "@heroicons/react/24/outline";

// 첫글자만 대문자, 나머지는 소문자 변환 함수
function capitalize(str) {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function CompanyFinancePage() {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const initialCompanyName = params.get("name") || "";

  const [companyName, setCompanyName] = useState(initialCompanyName);
  const [finance, setFinance] = useState(null);
  const [error, setError] = useState("");
  const [companies, setCompanies] = useState([]);
  const [displayCompanyName, setDisplayCompanyName] = useState(""); // 현재 조회된 기업명

  // 기업 목록 캐싱
  useEffect(() => {
    api.get("/company/companies").then(res => setCompanies(res.data));
  }, []);

  // 페이지 진입 시 쿼리스트링으로 받은 기업명으로 바로 조회
  useEffect(() => {
    if (
      initialCompanyName &&
      companies.some(c => c.name === capitalize(initialCompanyName))
    ) {
      setCompanyName(capitalize(initialCompanyName));
      handleFinance(capitalize(initialCompanyName));
    }
    // eslint-disable-next-line
  }, [companies, initialCompanyName]);

  // 재무정보 조회 함수
  const handleFinance = async (name = companyName) => {
    setFinance(null);
    setError("");
    const targetName = capitalize(name);
    if (!companies.some(c => c.name === targetName)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    try {
      const res = await api.get(`/company/companies/${targetName}/info`);
      setFinance(res.data);
      setDisplayCompanyName(targetName); // 조회 성공 시 현재 기업명 고정
    } catch (err) {
      setError(
        "재무정보 조회 실패: " + (err.response?.data?.detail || err.message)
      );
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center p-4">
      <div className="w-full max-w-3xl bg-white p-6 rounded-2xl shadow-lg space-y-6">
        {/* 헤더 */}
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold">🏢 기업 재무정보 조회</h2>
          <button
            onClick={() => window.history.back()}
            className="p-2 rounded hover:bg-gray-100 transition"
            title="이전 페이지"
          >
            <ArrowLeftIcon className="h-5 w-5 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        {/* 입력 및 버튼 */}
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            value={companyName}
            onChange={e => setCompanyName(e.target.value)}
            placeholder="기업명 입력"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={() => handleFinance()}
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition"
          >
            재무정보 조회
          </button>
        </div>

        {/* 오류 메시지 */}
        {error && <div className="text-red-500 text-sm">{error}</div>}

        {/* 조회된 기업명 고정 출력 */}
        {finance && displayCompanyName && (
          <div className="text-lg font-semibold mt-2 mb-2">
            {displayCompanyName} 재무정보
          </div>
        )}

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
