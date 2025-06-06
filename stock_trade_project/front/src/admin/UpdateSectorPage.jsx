import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

function UpdateSectorPage() {
  const [companyName, setCompanyName] = useState("");
  const [sector, setSector] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [companies, setCompanies] = useState([]);
  const navigate = useNavigate();

  const fetchCompanies = () => {
    api.get("/admin/companies").then((res) => setCompanies(res.data));
  };

  useEffect(() => {
    fetchCompanies();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult("");
    setError("");
    try {
      await api.put("/admin/companies/sector", {
        company_name: companyName,
        sector: sector,
      });
      setResult("✅ 섹터 수정 완료!");
      setCompanyName("");
      setSector("");
      fetchCompanies();
    } catch (err) {
      setError("❌ 수정 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-5xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-6">
        {/* 상단 헤더 */}
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-800">🏢 기업 섹터 수정</h2>
          <button
            onClick={() => navigate("/admin/home")}
            className="p-2 rounded-full hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        {/* 기업 테이블 */}
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

        {/* 수정 폼 */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="기업명"
            className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            value={sector}
            onChange={(e) => setSector(e.target.value)}
            placeholder="새 섹터"
            className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
          >
            섹터 수정
          </button>
        </form>

        {/* 메시지 출력 */}
        {result && <div className="text-green-600">{result}</div>}
        {error && <div className="text-red-500">{error}</div>}
      </div>
    </div>
  );
}

export default UpdateSectorPage;
