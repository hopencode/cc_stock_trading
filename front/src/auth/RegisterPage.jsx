import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function RegisterPage() {
  const [form, setForm] = useState({ id: "", password: "", name: "", phone: "", type: "customer" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      let url = "/auth/register/customer";
      if (form.type === "company") url = "/auth/register/company";
      await api.post(url, form);
      setMessage("회원가입 성공! 로그인 해주세요.");
      setError("");
    } catch (err) {
      setError("회원가입 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleRegister}
        className="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg space-y-5"
      >
        <h2 className="text-2xl font-bold text-center">회원가입</h2>

        <input
          name="id"
          value={form.id}
          onChange={handleChange}
          placeholder="아이디"
          className="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-400"
        />

        <input
          name="password"
          type="password"
          value={form.password}
          onChange={handleChange}
          placeholder="비밀번호"
          className="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-400"
        />

        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="이름 / 기업명"
          className="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-400"
        />

        <input
          name="phone"
          value={form.phone}
          onChange={handleChange}
          placeholder="전화번호"
          className="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-400"
        />

        <select
          name="type"
          value={form.type}
          onChange={handleChange}
          className="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-400"
        >
          <option value="customer">일반고객</option>
          <option value="company">기업고객</option>
        </select>

        <button
          type="submit"
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded-md transition"
        >
          회원가입
        </button>

        {message && (
          <div className="text-green-600 text-center text-sm">{message}</div>
        )}
        {error && (
          <div className="text-red-500 text-center text-sm">{error}</div>
        )}
        <button onClick={() => navigate("/login")} style={{ marginLeft: "5px" }}>로그인</button>
      </form>
    </div>
  );
}

export default RegisterPage;
