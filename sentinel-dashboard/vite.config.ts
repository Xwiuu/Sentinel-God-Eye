import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      // ADICIONE ESSA LINHA ABAIXO:
      'vue': 'vue/dist/vue.esm-bundler.js' 
    }
  }
})