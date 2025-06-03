import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

function CompanyFinancialInfoPage() {
  const [form, setForm] = useState({
    year: "",
    sales: "",
    business_profits: "",
    pure_profits: ""
  });
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(""); setError("");
    try {
      const res = await api.post("/company/financial-info", {
        ...form,
        year: Number(form.year),
        sales: Number(form.sales),
        business_profits: Number(form.business_profits),
        pure_profits: Number(form.pure_profits)
      });
      setResult("재무정보 등록 완료!");
    } catch (err) {
      setError("등록 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white p-6 rounded-2xl shadow-lg space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold">📊 재무정보 등록</h2>
          <button
            onClick={() => navigate("/company/home")}
            className="p-2 rounded hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            name="year"
            value={form.year}
            onChange={handleChange}
            placeholder="연도"
            type="number"
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="sales"
            value={form.sales}
            onChange={handleChange}
            placeholder="매출"
            type="number"
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="business_profits"
            value={form.business_profits}
            onChange={handleChange}
            placeholder="영업이익"
            type="number"
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="pure_profits"
            value={form.pure_profits}
            onChange={handleChange}
            placeholder="순이익"
            type="number"
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition"
          >
            등록
          </button>
        </form>

        {result && <div className="text-green-600 text-sm text-center">{result}</div>}
        {error && <div className="text-red-500 text-sm text-center">{error}</div>}
      </div>
    </div>
  );
}

export default CompanyFinancialInfoPage;
