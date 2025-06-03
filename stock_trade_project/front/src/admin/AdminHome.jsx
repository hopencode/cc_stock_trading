import React from "react";
import { useNavigate } from "react-router-dom";

function AdminHome() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token"); // 토큰 삭제
    navigate("/login"); // 로그인 페이지로 이동
  };

  return (
    <div>
      <h2>관리자 기능</h2>
      <button onClick={handleLogout} style={{ float: "right" }}>로그아웃</button>
      <div style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "200px" }}>
        <button onClick={() => navigate("/admin/register-company")}>기업 상장</button>
        <button onClick={() => navigate("/admin/update-sector")}>기업 섹터 수정</button>
        <button onClick={() => navigate("/admin/delete-company")}>기업 상장 폐지</button>
      </div>
    </div>
  );
}

export default AdminHome;
