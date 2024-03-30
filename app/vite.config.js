import { defineConfig } from 'vite'

export default defineConfig({
    // Base configuration
    base: '/pro-stock-ai/',
    build: {
      rollupOptions: {
        input: {
          main: 'index.html',
          page1: 'pitch-only-stats-tsne.html',
          page2: 'experiment-1.html'
        }
      }
    }
  });