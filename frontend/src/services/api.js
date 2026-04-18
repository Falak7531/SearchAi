import axios from "axios";

const BASE_URL = import.meta.env.DEV
  ? ""
  : import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  headers: { "Content-Type": "application/json" },
});

// Request/response interceptors for debugging
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("[API Error]", error.response?.status, error.message);
    return Promise.reject(error);
  }
);

export const searchProducts = async (query, options = {}) => {
  const payload = {
    query,
    top_k: options.top_k || 10,
    ...(options.category && { category: options.category }),
  };
  const response = await apiClient.post("/search/", payload);
  return response.data;
};

export const checkHealth = async () => {
  const response = await apiClient.get("/health/");
  return response.data;
};

export default apiClient;
