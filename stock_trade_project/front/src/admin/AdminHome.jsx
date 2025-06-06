import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function AdminHome() {
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState(null);

  const handleLogout = () => {
    localStorage.removeItem("token"); // 토큰 삭제
    localStorage.removeItem("userRole");
    setUserRole(null);
    navigate("/login"); // 로그인 페이지로 이동
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">🛠️ 관리자 기능</h2>

        <div className="flex flex-col gap-4">
          <button
            onClick={() => navigate("/admin/register-company")}
            className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition"
          >
            기업 상장
          </button>
          <button
            onClick={() => navigate("/admin/update-sector")}
            className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition"
          >
            기업 섹터 수정
          </button>
          <button
            onClick={() => navigate("/admin/delete-company")}
            className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition"
          >
            기업 상장 폐지
          </button>
          <button
            onClick={handleLogout}
            className="w-full bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-md transition"
          >
            로그아웃
          </button>
        </div>
      </div>
    </div>
  );
}

export default AdminHome;
