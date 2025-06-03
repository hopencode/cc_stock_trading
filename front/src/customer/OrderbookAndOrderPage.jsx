import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

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

  useEffect(() => {
    api.get("/customer/companies").then(res => setCompanies(res.data));
  }, []);

  // 페이지 진입 시 쿼리스트링으로 받은 기업명으로 바로 조회
  useEffect(() => {
    if (initialCompanyName && companies.some(c => c.name === initialCompanyName)) {
      setCompanyName(initialCompanyName);
      handleOrderbook(initialCompanyName);
    }
    // eslint-disable-next-line
  }, [companies, initialCompanyName]);

  const handleOrderbook = async (name = companyName) => {
    setOrderbook(null); setError(""); setOrderResult("");
    const targetName = name || companyName;
    if (!companies.some(c => c.name === targetName)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    try {
      const res = await api.get(`/customer/companies/${targetName}/orders`);
      setOrderbook(res.data);
    } catch (err) {
      setError("호가창 조회 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleBuy = async () => {
    setOrderResult(""); setError("");
    if (!companies.some(c => c.name === companyName)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    if (!orderPrice || !orderCount) {
      setError("주문 가격과 수량을 입력하세요.");
      return;
    }
    try {
      const res = await api.post("/customer/trading/buy", {
        company_name: companyName,
        price: Number(orderPrice),
        count: Number(orderCount)
      });
      setOrderResult("매수: " + res.data.message +
        ` (체결: ${res.data.concluded_count}, 미체결: ${res.data.remaining_count})`);

      // 주문 성공 후 호가창 갱신
      await handleOrderbook(companyName);
      setOrderPrice("");
      setOrderCount("");
    } catch (err) {
      setOrderResult("매수 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleSell = async () => {
    setOrderResult(""); setError("");
    if (!companies.some(c => c.name === companyName)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    if (!orderPrice || !orderCount) {
      setError("주문 가격과 수량을 입력하세요.");
      return;
    }
    try {
      const res = await api.post("/customer/trading/sell", {
        company_name: companyName,
        price: Number(orderPrice),
        count: Number(orderCount)
      });
      setOrderResult("매도: " + res.data.message +
        ` (체결: ${res.data.concluded_count}, 미체결: ${res.data.remaining_count})`);
      await handleOrderbook(companyName);
      setOrderPrice("");
      setOrderCount("");
    } catch (err) {
      setOrderResult("매도 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6 bg-gray-100 rounded-xl shadow-md">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold">📈 호가창 조회 및 주문</h2>
        <button onClick={() => navigate("/customer/home")} className="hover:text-blue-500">
          <HomeIcon className="h-6 w-6 text-gray-600" />
        </button>
      </div>

      <div className="flex items-center space-x-2 mb-4">
        <input
          type="text"
          value={companyName}
          onChange={e => setCompanyName(e.target.value)}
          placeholder="기업명 입력"
          className="border px-4 py-2 rounded-md flex-grow"
        />
        <button onClick={() => handleOrderbook()} className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md">호가창 조회</button>
      </div>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      {orderbook && (
        <div className="mb-6">
          <h3 className="text-xl font-semibold mb-2">{companyName} 호가창</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="font-semibold mb-1">🟢 매수</h4>
              <table className="w-full border">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="border px-2">가격</th>
                    <th className="border px-2">수량</th>
                  </tr>
                </thead>
                <tbody>
                  {orderbook.buy_orders.map((o, i) => (
                    <tr key={i}>
                      <td className="border px-2 text-center">{o.price}</td>
                      <td className="border px-2 text-center">{o.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div>
              <h4 className="font-semibold mb-1">🔴 매도</h4>
              <table className="w-full border">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="border px-2">가격</th>
                    <th className="border px-2">수량</th>
                  </tr>
                </thead>
                <tbody>
                  {orderbook.sell_orders.map((o, i) => (
                    <tr key={i}>
                      <td className="border px-2 text-center">{o.price}</td>
                      <td className="border px-2 text-center">{o.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-3">
        <div className="flex gap-2">
          <input
            type="number"
            value={orderPrice}
            onChange={e => setOrderPrice(e.target.value)}
            placeholder="주문 가격"
            className="border px-4 py-2 rounded-md w-1/2"
          />
          <input
            type="number"
            value={orderCount}
            onChange={e => setOrderCount(e.target.value)}
            placeholder="주문 수량"
            className="border px-4 py-2 rounded-md w-1/2"
          />
        </div>
        <div className="flex gap-4">
          <button onClick={handleBuy} className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md w-full">매수</button>
          <button onClick={handleSell} className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md w-full">매도</button>
        </div>
        {orderResult && <div className="text-blue-600 font-medium">{orderResult}</div>}
      </div>
    </div>
  );
}

export default OrderbookAndOrderPage;
