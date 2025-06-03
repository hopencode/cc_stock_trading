import React, { useEffect, useState, useRef } from "react";
import { useLocation } from "react-router-dom";
import api from "../api/api";

function OrderbookAndOrderPage() {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const initialCompanyName = params.get("name") || "";
  const inputRef = useRef(null);

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
      handleOrderbook(initialCompanyName);
    }
    // eslint-disable-next-line
  }, [companies, initialCompanyName]);

  const handleOrderbook = async (name = companyName) => {
    setOrderbook(null); setError(""); setOrderResult("");
    if (!companies.some(c => c.name === name)) {
      setError("입력한 기업명이 목록에 없습니다.");
      return;
    }
    try {
      const res = await api.get(`/customer/companies/${name}/orders`);
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
      // 주문 입력값만 초기화 (companyName 유지)
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
      
      // 주문 성공 후 호가창 갱신
      await handleOrderbook(companyName);
      // 주문 입력값만 초기화 (companyName 유지)
      setOrderPrice("");
      setOrderCount("")
    } catch (err) {
      setOrderResult("매도 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h2>호가창 조회 및 주식 주문</h2>
      <button onClick={() => window.history.back()} style={{ float: "right" }}>이전 페이지</button>
      <input
        ref={inputRef}
        type="text"
        value={companyName}
        onChange={e => setCompanyName(e.target.value)}
        placeholder="기업명 입력"
      />
      <button onClick={() => handleOrderbook(inputRef.current.value)}>호가창 조회</button>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {/* 호가창 출력 */}
      {orderbook && (
        <div style={{ margin: "20px 0" }}>
          <h3>호가창 - {companyName}</h3>
          <div style={{ display: "flex", gap: "40px" }}>
            <div>
              <strong>매수</strong>
              <table border="1">
                <thead>
                  <tr><th>가격</th><th>수량</th></tr>
                </thead>
                <tbody>
                  {orderbook.buy_orders.map((o, i) => (
                    <tr key={i}><td>{o.price}</td><td>{o.count}</td></tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div>
              <strong>매도</strong>
              <table border="1">
                <thead>
                  <tr><th>가격</th><th>수량</th></tr>
                </thead>
                <tbody>
                  {orderbook.sell_orders.map((o, i) => (
                    <tr key={i}><td>{o.price}</td><td>{o.count}</td></tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 주문 입력 */}
      <div style={{ margin: "20px 0" }}>
        <input
          type="number"
          value={orderPrice}
          onChange={e => setOrderPrice(e.target.value)}
          placeholder="주문 가격"
          style={{ marginRight: "10px" }}
        />
        <input
          type="number"
          value={orderCount}
          onChange={e => setOrderCount(e.target.value)}
          placeholder="주문 수량"
          style={{ marginRight: "10px" }}
        />
        <button onClick={handleBuy}>매수</button>
        <button onClick={handleSell} style={{ marginLeft: "5px" }}>매도</button>
      </div>
      {orderResult && <div style={{ color: "blue" }}>{orderResult}</div>}
    </div>
  );
}

export default OrderbookAndOrderPage;
