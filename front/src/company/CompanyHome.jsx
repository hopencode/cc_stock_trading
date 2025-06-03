import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function CompanyHome() {
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState(null);

  const handleLogout = () => {
    localStorage.removeItem("token"); // 토큰 삭제
    localStorage.removeItem("userRole");
    setUserRole(null);
    navigate("/login"); // 로그인 페이지로 이동
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10">
      <div className="max-w-xl mx-auto p-6 bg-white rounded-xl shadow-md">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">🏢 기업 고객 기능</h2>
        </div>

        <div className="flex flex-col gap-3">
          <button
            onClick={() => navigate("/company/deposit-withdraw")}
            className="bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
          >
            입출금
          </button>
          <button
            onClick={() => navigate("/company/companies")}
            className="bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
          >
            기업 목록 조회
          </button>
          <button
            onClick={() => navigate("/company/orders")}
            className="bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
          >
            주문 조회/취소
          </button>
          <button
            onClick={() => navigate("/company/balance")}
            className="bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
          >
            잔고 조회
          </button>
          <button
            onClick={() => navigate("/company/financial-info")}
            className="bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
          >
            재무정보 등록
          </button>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white py-2 rounded hover:bg-red-600 transition"
          >
            로그아웃
          </button>
        </div>
      </div>
    </div>
  );
}

export default CompanyHome;
