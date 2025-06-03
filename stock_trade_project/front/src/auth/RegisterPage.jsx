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
    <form onSubmit={handleRegister}>
      <h2>회원가입</h2>
      <input name="id" value={form.id} onChange={handleChange} placeholder="ID" /> <br/>
      <input name="password" type="password" value={form.password} onChange={handleChange} placeholder="비밀번호" /> <br/>
      <input name="name" value={form.name} onChange={handleChange} placeholder="이름/기업명" /> <br/>
      <input name="phone" value={form.phone} onChange={handleChange} placeholder="전화번호 010-0000-0000" /> <br/>
      <select name="type" value={form.type} onChange={handleChange}> 
        <option value="customer">일반고객</option>
        <option value="company">기업고객</option>
      </select> <br/> <br/>
      <button type="submit" style={{ marginLeft: "5px" }}>회원가입</button>
      {message && <div style={{color:"green"}}>{message}</div>}
      {error && <div style={{color:"red"}}>{error}</div>}
        <button onClick={() => navigate("/login")} style={{ marginLeft: "5px" }}>로그인</button>
    </form>
  );
}

export default RegisterPage;
