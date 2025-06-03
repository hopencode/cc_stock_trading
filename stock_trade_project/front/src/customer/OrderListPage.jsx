import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function OrderListPage() {
  const [orders, setOrders] = useState([]);
  const [cancelOrderNumber, setCancelOrderNumber] = useState("");
  const [cancelResult, setCancelResult] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // 주문 목록 불러오기
  const fetchOrders = () => {
    api.get("/customer/orders")
      .then(res => setOrders(res.data))
      .catch(err => setError("주문 목록 조회 실패: " + (err.response?.data?.detail || err.message)));
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  // 주문 취소
  const handleCancel = async () => {
    setCancelResult(""); setError("");
    if (!cancelOrderNumber) {
      setError("주문번호를 입력하세요.");
      return;
    }
    if (!orders.some(o => String(o.order_number) === cancelOrderNumber)) {
      setError("해당 주문번호가 목록에 없습니다.");
      return;
    }
    try {
      await api.delete("/customer/orders", { data: { order_number: Number(cancelOrderNumber) } });
      setCancelResult(`주문번호 ${cancelOrderNumber}번이 취소되었습니다.`);
      setCancelOrderNumber("");
      fetchOrders(); // 목록 갱신
    } catch (err) {
      setError("주문 취소 실패: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h2>내 주문 목록</h2>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <button onClick={() => navigate("/customer/home")} style={{ float: "right" }}>홈 페이지</button>
      <table border="1">
        <thead>
          <tr>
            <th>주문번호</th>
            <th>유형</th>
            <th>기업명</th>
            <th>가격</th>
            <th>수량</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(o => (
            <tr key={o.order_number}>
              <td>{o.order_number}</td>
              <td>{o.type === "buy" ? "매수" : "매도"}</td>
              <td>{o.name}</td>
              <td>{o.price}</td>
              <td>{o.count}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: "20px" }}>
        <input
          type="number"
          value={cancelOrderNumber}
          onChange={e => setCancelOrderNumber(e.target.value)}
          placeholder="취소할 주문번호 입력"
          style={{ marginRight: "10px" }}
        />
        <button onClick={handleCancel}>주문 취소</button>
      </div>
      {cancelResult && <div style={{ color: "blue", marginTop: "10px" }}>{cancelResult}</div>}
    </div>
  );
}

export default OrderListPage;
