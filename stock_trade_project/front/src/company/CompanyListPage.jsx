import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function CompanyListPage() {
  const [companies, setCompanies] = useState([]);
  const [inputName, setInputName] = useState("");
  const [alert, setAlert] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/company/companies").then(res => setCompanies(res.data));
  }, []);

  // 기업명 유효성 검사
  const isValidCompany = (name) => companies.some(c => c.name === name);

  // 버튼 클릭시 페이지 이동
  const handleGoFinance = () => {
    if (!isValidCompany(inputName)) {
      setAlert("입력한 기업명이 목록에 없습니다.");
      return;
    }
    setAlert("");
    navigate(`/company/finance?name=${encodeURIComponent(inputName)}`);
  };

  const handleGoOrderbook = () => {
    if (!isValidCompany(inputName)) {
      setAlert("입력한 기업명이 목록에 없습니다.");
      return;
    }
    setAlert("");
    navigate(`/company/order?name=${encodeURIComponent(inputName)}`);
  };

  return (
    <div>
      <h2>상장 기업 목록</h2>
      <table border="1">
        <thead>
          <tr>
            <th>기업명</th><th>섹터</th><th>현재가</th><th>총발행주식</th><th>시가총액</th>
          </tr>
        </thead>
        <tbody>
          {companies.map(c => (
            <tr key={c.name}>
              <td>{c.name}</td>
              <td>{c.sector}</td>
              <td>{c.price}</td>
              <td>{c.stock_num}</td>
              <td>{c.total_price}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: "20px" }}>
        <input
          type="text"
          value={inputName}
          onChange={e => setInputName(e.target.value)}
          placeholder="기업명 입력"
          style={{ marginRight: "10px" }}
        />
        <button onClick={handleGoFinance}>재무정보 조회</button>
        <button onClick={handleGoOrderbook} style={{ marginLeft: "5px" }}>호가창/주문</button>
      </div>
      {alert && <div style={{ color: "red", marginTop: "10px" }}>{alert}</div>}
    </div>
  );
}

export default CompanyListPage;
