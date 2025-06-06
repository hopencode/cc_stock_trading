import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../api/api";
import { ArrowLeftIcon } from "@heroicons/react/24/outline";

// 첫글자만 대문자, 나머지는 소문자 변환 함수
function capitalize(str) {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function OrderbookAndOrderPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const params = new URLSearchParams(location.search);
  const initialCompanyName = params.get("name") || "";

  const [companyName, setCompanyName] = useState(initialCompanyName);
  const [orderbook, setOrderbook] = useState(null);
  const [orderPrice, setOrderPrice] = useState("");
  const [orderCount, setOrderCount] = useState("");
  const [orderResult, setOrderResult] = useState("");
  const [error, setError] = useState("");
  const [companies, setCompanies] = useState([]);
  const [displayCompanyName, setDisplayCompanyName] = useState(""); // 현재 호가창이 출력중인 기업명

  useEffect(() => {
    api.get("/company/companies").then(res => setCompanies(res.data));
  }, []);

  // 페이지 진입 시 쿼리스트링으로 받은 기업명으로 바로 조회
  useEffect(() => {
    if (initialCompanyName && companies.some(c => c.name === capitalize(initialCompanyName))) {
      setCompanyName(capitalize(initialCompanyName));
      handleOrderbook(capitalize(initialCompanyName));
    }
    // eslint-disable-next-line
  }, [companies, initialCompanyName]);

  const handleOrderbook = async (name = companyName) => {
    setOrderbook(null); setError(""); setOrderResult("");
    const targetName = capitalize(name);
    if (!companies.some(c => c.name === targetName)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    try {
      const res = await api.get(`/company/companies/${targetName}/orders`);
      setOrderbook(res.data);
      setDisplayCompanyName(targetName); // 조회 성공 시 현재 호가창 기업명 고정
    } catch (err) {
      setError("호가창 조회 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleBuy = async () => {
    setOrderResult(""); setError("");
    const targetName = capitalize(companyName);
    if (!companies.some(c => c.name === targetName)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    if (!orderPrice || !orderCount) {
      setError("주문 가격과 수량을 입력하세요.");
      return;
    }
    try {
      const res = await api.post("/company/trading/buy", {
        company_name: targetName,
        price: Number(orderPrice),
        count: Number(orderCount)
      });
      setOrderResult("매수: " + res.data.message +
        ` (체결: ${res.data.concluded_count}, 미체결: ${res.data.remaining_count})`);
      await handleOrderbook(targetName);
      setOrderPrice("");
      setOrderCount("");
    } catch (err) {
      setOrderResult("매수 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleSell = async () => {
    setOrderResult(""); setError("");
    const targetName = capitalize(companyName);
    if (!companies.some(c => c.name === targetName)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    if (!orderPrice || !orderCount) {
      setError("주문 가격과 수량을 입력하세요.");
      return;
    }
    try {
      const res = await api.post("/company/trading/sell", {
        company_name: targetName,
        price: Number(orderPrice),
        count: Number(orderCount)
      });
      setOrderResult("매도: " + res.data.message +
        ` (체결: ${res.data.concluded_count}, 미체결: ${res.data.remaining_count})`);
      await handleOrderbook(targetName);
      setOrderPrice("");
      setOrderCount("");
    } catch (err) {
      setOrderResult("매도 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex justify-center">
      <div className="w-full max-w-3xl bg-white p-6 rounded-xl shadow-md space-y-6">
        <h2 className="text-2xl font-bold">📈 호가창 조회 및 주식 주문</h2>
        <button
          onClick={() => window.history.back()}
          className="p-2 rounded hover:bg-gray-100 transition"
          title="이전 페이지"
        >
          <ArrowLeftIcon className="h-5 w-5 text-gray-600 hover:text-blue-500" />
        </button>

        <div className="flex flex-col sm:flex-row items-center gap-4">
          <input
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="기업명 입력"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={() => handleOrderbook()}
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md"
          >
            호가창 조회
          </button>
        </div>

        {error && <div className="text-red-500 text-sm">{error}</div>}

        {orderbook && (
          <div className="mt-4 space-y-4">
            <h3 className="text-lg font-semibold">
              {displayCompanyName} 호가창
            </h3>
            <div className="flex gap-6">
              <div className="flex-1">
                <h4 className="font-semibold text-red-600">🔴 매수</h4>
                <table className="w-full text-sm border border-gray-300">
                  <thead className="bg-red-100">
                    <tr>
                      <th className="border px-2 py-1">가격</th>
                      <th className="border px-2 py-1">수량</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orderbook.buy_orders.map((o, i) => (
                      <tr key={i} className="text-center">
                        <td className="border px-2 py-1">{o.price}</td>
                        <td className="border px-2 py-1">{o.count}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-blue-600">🔵 매도</h4>
                <table className="w-full text-sm border border-gray-300">
                  <thead className="bg-blue-100">
                    <tr>
                      <th className="border px-2 py-1">가격</th>
                      <th className="border px-2 py-1">수량</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orderbook.sell_orders.map((o, i) => (
                      <tr key={i} className="text-center">
                        <td className="border px-2 py-1">{o.price}</td>
                        <td className="border px-2 py-1">{o.count}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* 주문 입력 */}
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="number"
            value={orderPrice}
            onChange={(e) => setOrderPrice(e.target.value)}
            placeholder="주문 가격"
            className="flex-1 px-4 py-2 border rounded-md"
          />
          <input
            type="number"
            value={orderCount}
            onChange={(e) => setOrderCount(e.target.value)}
            placeholder="주문 수량"
            className="flex-1 px-4 py-2 border rounded-md"
          />
          <button
            onClick={handleBuy}
            className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition"
          >
            매수
          </button>
          <button
            onClick={handleSell}
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition"
          >
            매도
          </button>
        </div>

        {orderResult && <div className="text-blue-700 font-medium">{orderResult}</div>}
      </div>
    </div>
  );
}

export default OrderbookAndOrderPage;
