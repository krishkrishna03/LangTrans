import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    strictPort: false
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'axios']
        }
      }
    },
    // Ensure proper chunking for production
    chunkSizeWarningLimit: 1000
  },
  // Base URL - important for Netlify deployments
  base: '/',
  // Optimize dependencies
  optimizeDeps: {
    include: ['react', 'react-dom', 'axios']
  }
})
