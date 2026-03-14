import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/auth": "http://localhost:8000",
      "/urls": "http://localhost:8000",
      "/analytics": "http://localhost:8000",
      "/r": "http://localhost:8000",
    },
  },
});
