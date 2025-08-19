import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        /* sends request to backend when fetched */
        target: "http://localhost:5001",
        /* changes origin to server*/
        changeOrigin: true,
        /* sends to whatever comes after api*/
        rewrite: (path) => path.replace(/^\/api/, "")
      }
    }
  }
})
