import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { HomeIcon } from "@heroicons/react/24/outline";

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
    <div className="min-h-screen bg-gray-100 p-6 flex justify-center">
      <div className="w-full max-w-4xl bg-white p-6 rounded-xl shadow-md space-y-6 relative">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">📋 내 주문 목록</h2>
          <button
            onClick={() => navigate("/customer/home")}
            className="p-2 rounded hover:bg-gray-100 transition"
            title="홈으로"
          >
            <HomeIcon className="h-6 w-6 text-gray-600 hover:text-blue-500" />
          </button>
        </div>

        {error && <div className="text-red-500 text-sm">{error}</div>}

        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300 text-sm text-center">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 border">주문번호</th>
                <th className="px-4 py-2 border">유형</th>
                <th className="px-4 py-2 border">기업명</th>
                <th className="px-4 py-2 border">가격</th>
                <th className="px-4 py-2 border">수량</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((o) => (
                <tr key={o.order_number} className="hover:bg-gray-50">
                  <td className="border px-4 py-2">{o.order_number}</td>
                  <td className="border px-4 py-2">
                    {o.type === "buy" ? "매수" : "매도"}
                  </td>
                  <td className="border px-4 py-2">{o.name}</td>
                  <td className="border px-4 py-2">{o.price}</td>
                  <td className="border px-4 py-2">{o.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-6 flex flex-col sm:flex-row gap-3 items-center">
          <input
            type="number"
            value={cancelOrderNumber}
            onChange={e => setCancelOrderNumber(e.target.value)}
            placeholder="취소할 주문번호 입력"
            className="border px-4 py-2 rounded-md w-full sm:w-auto"
          />
          <button
            onClick={handleCancel}
            className="bg-red-500 hover:bg-red-600 text-white font-semibold px-4 py-2 rounded-md"
          >
            주문 취소
          </button>
        </div>

        {cancelResult && (
          <div className="text-blue-600 mt-4 font-medium">{cancelResult}</div>
        )}
      </div>
    </div>
  );
}

export default OrderListPage;
