import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

function RegisterCompanyPage() {
  const [form, setForm] = useState({ name: "", sector: "", price: "", stock_num: "" });
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [companies, setCompanies] = useState([]);
  const navigate = useNavigate();

  const fetchCompanies = () => {
    api.get("/admin/companies").then(res => setCompanies(res.data));
  };

  useEffect(() => {
    fetchCompanies();
  }, []);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult("");
    setError("");
    try {
      await api.post("/admin/companies", {
        ...form,
        price: Number(form.price),
        stock_num: Number(form.stock_num),
      });
      setResult("✅ 기업 등록 완료!");
      setForm({ name: "", sector: "", price: "", stock_num: "" });
      fetchCompanies();
    } catch (err) {
      setError("❌ 등록 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-5xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-6">

        {/* 헤더 */}
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-800">📈 기업 상장 등록</h2>
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

        {/* 등록 폼 */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="기업명"
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="sector"
            value={form.sector}
            onChange={handleChange}
            placeholder="섹터"
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="price"
            value={form.price}
            onChange={handleChange}
            placeholder="주당 가격"
            type="number"
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="stock_num"
            value={form.stock_num}
            onChange={handleChange}
            placeholder="총 발행주식수"
            type="number"
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
          >
            기업 등록
          </button>
        </form>

        {/* 메시지 출력 */}
        {result && <div className="text-green-600 mt-2">{result}</div>}
        {error && <div className="text-red-500 mt-2">{error}</div>}
      </div>
    </div>
  );
}

export default RegisterCompanyPage;
