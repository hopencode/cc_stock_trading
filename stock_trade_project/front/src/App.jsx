import React, { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./auth/LoginPage";
import RegisterPage from "./auth/RegisterPage";

// 고객
import CustomerHome from "./customer/CustomerHome";
import DepositWithdrawPage from "./customer/DepositWithdrawPage";
import CompanyListPage from "./customer/CompanyListPage";
import CompanyFinancePage from "./customer/CompanyFinancePage";
import OrderbookAndOrderPage from "./customer/OrderbookAndOrderPage";
import OrderListPage from "./customer/OrderListPage";
import BalancePage from "./customer/BalancePage";
import PortfolioWeightPage from "./customer/PortfolioWeightPage";

// 관리자
import AdminHome from "./admin/AdminHome";
import RegisterCompanyPage from "./admin/RegisterCompanyPage";
import UpdateSectorPage from "./admin/UpdateSectorPage";
import DeleteCompanyPage from "./admin/DeleteCompanyPage";

// 기업
import CompanyHome from "./company/CompanyHome";
import CompanyDepositWithdrawPage from "./company/DepositWithdrawPage";
import CompanyListPage2 from "./company/CompanyListPage";
import CompanyFinancePage2 from "./company/CompanyFinancePage";
import CompanyOrderbookAndOrderPage from "./company/OrderbookAndOrderPage";
import CompanyOrderListPage from "./company/OrderListPage";
import CompanyBalancePage from "./company/BalancePage";
import CompanyFinancialInfoPage from "./company/CompanyFinancialInfoPage";

function App() {
  // 로그인 상태 관리(간단 예시)
  const [userRole, setUserRole] = useState(null);

  // 로그인 성공 시 콜백
  const handleLogin = (userInfo, userType) => {
    setUserRole(userType);
  };

  return (
    <Routes>
      {/* 인증 */}
      <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* 고객 */}
      <Route path="/customer/home" element={userRole === "customer" ? <CustomerHome /> : <Navigate to="/login" />} />
      <Route path="/customer/deposit-withdraw" element={<DepositWithdrawPage />} />
      <Route path="/customer/companies" element={<CompanyListPage />} />
      <Route path="/customer/finance" element={<CompanyFinancePage />} />
      <Route path="/customer/order" element={<OrderbookAndOrderPage />} />
      <Route path="/customer/orders" element={<OrderListPage />} />
      <Route path="/customer/balance" element={<BalancePage />} />
      <Route path="/customer/portfolio" element={<PortfolioWeightPage />} />

      {/* 관리자 */}
      <Route path="/admin/home" element={userRole === "admin" ? <AdminHome /> : <Navigate to="/login" />} />
      <Route path="/admin/register-company" element={<RegisterCompanyPage />} />
      <Route path="/admin/update-sector" element={<UpdateSectorPage />} />
      <Route path="/admin/delete-company" element={<DeleteCompanyPage />} />

      {/* 기업 */}
      <Route path="/company/home" element={userRole === "company" ? <CompanyHome /> : <Navigate to="/login" />} />
      <Route path="/company/deposit-withdraw" element={<CompanyDepositWithdrawPage />} />
      <Route path="/company/companies" element={<CompanyListPage2 />} />
      <Route path="/company/finance" element={<CompanyFinancePage2 />} />
      <Route path="/company/order" element={<CompanyOrderbookAndOrderPage />} />
      <Route path="/company/orders" element={<CompanyOrderListPage />} />
      <Route path="/company/balance" element={<CompanyBalancePage />} />
      <Route path="/company/financial-info" element={<CompanyFinancialInfoPage />} />

      {/* 기본 경로: 로그인으로 리다이렉트 */}
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

export default App;
