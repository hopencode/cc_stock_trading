import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

// 요청 인터셉터로 매 요청마다 토큰 자동 첨부
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// setAuthToken 함수는 필요시 토큰을 수동으로 설정하거나 제거할 때 사용
export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
};

export default api;
