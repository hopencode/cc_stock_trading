import React, { useState } from "react";
import api, { setAuthToken } from "../api/api";
import { useNavigate } from "react-router-dom";

function LoginPage({ onLogin }) {
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");
  const [userType, setUserType] = useState("customer");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/auth/login", {
        id,
        password,
        user_type: userType,
      });
      setAuthToken(res.data.access_token);
      onLogin(res.data.user_info, userType);

      // 로그인 성공 후 계정 유형별 홈으로 이동
      localStorage.setItem("token", res.data.access_token);
      if (userType === "customer") {
        navigate("/customer/home");
      } else if (userType === "company") {
        navigate("/company/home");
      } else if (userType === "admin") {
        navigate("/admin/home");
      }
    } catch (err) {
      setError("로그인 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>로그인</h2>
      <input value={id} onChange={e => setId(e.target.value)} placeholder="ID" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="비밀번호" />
      <select value={userType} onChange={e => setUserType(e.target.value)}>
        <option value="customer">일반고객</option>
        <option value="company">기업고객</option>
        <option value="admin">관리자</option>
      </select>
      <button type="submit">로그인</button>
      {error && <div style={{color:"red"}}>{error}</div>}
    </form>
  );
}

export default LoginPage;
