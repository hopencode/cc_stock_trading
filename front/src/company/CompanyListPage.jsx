import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

function CompanyListPage() {
  const [companies, setCompanies] = useState([]);
  const [inputName, setInputName] = useState("");
  const [alert, setAlert] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/company/companies").then(res => setCompanies(res.data));
  }, []);

  // 기업명 유효성 검사
  const isValidCompany = (name) => companies.some(c => c.name === name);

  // 버튼 클릭시 페이지 이동
  const handleGoFinance = () => {
    if (!isValidCompany(inputName)) {
      setAlert("입력한 기업명이 목록에 없습니다.");
      return;
    }
    setAlert("");
    navigate(`/company/finance?name=${encodeURIComponent(inputName)}`);
  };

  const handleGoOrderbook = () => {
    if (!isValidCompany(inputName)) {
      setAlert("입력한 기업명이 목록에 없습니다.");
      return;
    }
    setAlert("");
    navigate(`/company/order?name=${encodeURIComponent(inputName)}`);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-5xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">🏢 상장 기업 목록</h2>
          <button
            onClick={() => navigate("/company/home")}
            className="p-2 rounded hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

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
                  <td className="px-4 py-2 border">{c.name}</td>
                  <td className="px-4 py-2 border">{c.sector}</td>
                  <td className="px-4 py-2 border">{c.price}</td>
                  <td className="px-4 py-2 border">{c.stock_num}</td>
                  <td className="px-4 py-2 border">{c.total_price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-4">
          <input
            type="text"
            value={inputName}
            onChange={(e) => setInputName(e.target.value)}
            placeholder="기업명 입력"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={handleGoFinance}
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition"
          >
            재무정보 조회
          </button>
          <button
            onClick={handleGoOrderbook}
            className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition"
          >
            호가창/주문
          </button>
        </div>

        {alert && <div className="text-red-500 text-sm">{alert}</div>}
      </div>
    </div>
  );
}

export default CompanyListPage;
