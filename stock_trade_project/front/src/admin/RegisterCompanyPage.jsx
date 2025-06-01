import React, { useState } from "react";
import api from "../api/api";

function RegisterCompanyPage() {
  const [form, setForm] = useState({
    name: "",
    sector: "",
    price: "",
    stock_num: ""
  });
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(""); setError("");
    try {
      await api.post("/admin/companies", {
        ...form,
        price: Number(form.price),
        stock_num: Number(form.stock_num)
      });
      setResult("기업 등록 완료!");
    } catch (err) {
      setError("등록 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>기업 상장 등록</h2>
      <input name="name" value={form.name} onChange={handleChange} placeholder="기업명" /><br />
      <input name="sector" value={form.sector} onChange={handleChange} placeholder="섹터" /><br />
      <input name="price" value={form.price} onChange={handleChange} placeholder="주당 가격" type="number" /><br />
      <input name="stock_num" value={form.stock_num} onChange={handleChange} placeholder="총 발행주식수" type="number" /><br />
      <button type="submit">등록</button>
      {result && <div style={{ color: "green" }}>{result}</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
    </form>
  );
}

export default RegisterCompanyPage;
