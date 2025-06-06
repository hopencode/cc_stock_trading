import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function CustomerHome() {
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState(null);

  const handleLogout = () => {
    localStorage.removeItem("token"); // 토큰 삭제
    localStorage.removeItem("userRole");
    setUserRole(null);
    navigate("/login"); // 로그인 페이지로 이동
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg space-y-6">
        <h2 className="text-xl font-bold text-center">고객 기능</h2>

        <div className="flex flex-col gap-4">
          <button
            onClick={() => navigate("/customer/deposit-withdraw")}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md transition"
          >
            입출금
          </button>
          <button
            onClick={() => navigate("/customer/companies")}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md transition"
          >
            기업 목록 조회
          </button>
          <button
            onClick={() => navigate("/customer/orders")}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md transition"
          >
            주문 조회/취소
          </button>
          <button
            onClick={() => navigate("/customer/balance")}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md transition"
          >
            잔고 조회
          </button>
          <button
            onClick={() => navigate("/customer/portfolio")}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md transition"
          >
            포트폴리오 비중
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

export default CustomerHome;
