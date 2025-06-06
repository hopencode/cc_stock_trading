import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

function DeleteCompanyPage() {
  const [companyName, setCompanyName] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [companies, setCompanies] = useState([]);
  const navigate = useNavigate();

  // 기업 목록 불러오기
  const fetchCompanies = () => {
    api.get("/admin/companies").then(res => setCompanies(res.data));
  };

  useEffect(() => {
    fetchCompanies();
  }, []);

  const handleDelete = async () => {
    setResult("");
    setError("");
    try {
      await api.delete(`/admin/companies/${encodeURIComponent(companyName)}`);
      setResult("✅ 기업 삭제 완료!");
      setCompanyName("");
      fetchCompanies(); // 삭제 후 목록 갱신
    } catch (err) {
      setError("❌ 삭제 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-5xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-6">

        {/* 상단 헤더 */}
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-800">📉 기업 상장 폐지</h2>
          <button
            onClick={() => navigate("/admin/home")}
            className="p-2 rounded-full hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        {/* 기업 목록 테이블 */}
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300 text-sm text-center">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 border">기업명</th>
                <th className="px-4 py-2 border">섹터</th>
                <th className="px-4 py-2 border">현재가</th>
                <th className="px-4 py-2 border">총발행주식</th>
                <th className="px-4 py-2 border">시가총액</th>
              </tr>
            </thead>
            <tbody>
              {companies.map((c) => (
                <tr key={c.name} className="hover:bg-gray-50">
                  <td className="border px-4 py-2">{c.name}</td>
                  <td className="border px-4 py-2">{c.sector}</td>
                  <td className="border px-4 py-2">{c.price}</td>
                  <td className="border px-4 py-2">{c.stock_num}</td>
                  <td className="border px-4 py-2">{c.total_price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* 삭제 입력 & 버튼 */}
        <div className="flex flex-col sm:flex-row items-center gap-4">
          <input
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="삭제할 기업명 입력"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400"
          />
          <button
            onClick={handleDelete}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition"
          >
            삭제
          </button>
        </div>

        {/* 결과 메시지 */}
        {result && <div className="text-green-600">{result}</div>}
        {error && <div className="text-red-500">{error}</div>}
      </div>
    </div>
  );
}

export default DeleteCompanyPage;
