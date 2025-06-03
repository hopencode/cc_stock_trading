import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

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
    <form onSubmit={handleSubmit}>
      <h2>재무정보 등록</h2>
      <button onClick={() => navigate("/company/home")} style={{ float: "right" }}>홈 페이지</button>
      <input name="year" value={form.year} onChange={handleChange} placeholder="연도" type="number" /><br />
      <input name="sales" value={form.sales} onChange={handleChange} placeholder="매출" type="number" /><br />
      <input name="business_profits" value={form.business_profits} onChange={handleChange} placeholder="영업이익" type="number" /><br />
      <input name="pure_profits" value={form.pure_profits} onChange={handleChange} placeholder="순이익" type="number" /><br />
      <button type="submit">등록</button>
      {result && <div style={{ color: "green" }}>{result}</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
    </form>
  );
}

export default CompanyFinancialInfoPage;
