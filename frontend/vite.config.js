import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    proxy: {
      // Proxy API calls to the FastAPI backend during development
      "/search": "http://127.0.0.1:8000",
      "/health": "http://127.0.0.1:8000",
      "/rag": "http://127.0.0.1:8000",
    },
  },
});
