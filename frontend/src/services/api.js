import axios from "axios";

const RAW_URL = import.meta.env.VITE_API_URL?.trim();

// Fail loudly in prod if the env var was never set or still contains a placeholder.
const isPlaceholder =
  !RAW_URL ||
  RAW_URL.includes("__SET_IN") ||
  RAW_URL.includes("your-domain") ||
  RAW_URL.includes("example.com");

if (import.meta.env.PROD && isPlaceholder) {
  // Surfaces in browser console immediately on bundle load
  // — much easier to diagnose than a CORS error against a fake host.
  // eslint-disable-next-line no-console
  console.error(
    "[config] VITE_API_URL is missing or a placeholder. " +
      "Set it in your hosting provider's environment variables and redeploy. " +
      "Current value:",
    RAW_URL
  );
}

const BASE_URL = import.meta.env.DEV ? "" : RAW_URL || "";

const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  headers: { "Content-Type": "application/json" },
});

// eslint-disable-next-line no-console
console.info("[api] baseURL =", BASE_URL || "(vite proxy)");

// Request/response interceptors for debugging
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(
      "[API Error]",
      error.response?.status,
      error.message,
      "→",
      error.config?.baseURL + error.config?.url
    );
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
