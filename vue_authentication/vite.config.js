import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})

// import vue from '@vitejs/plugin-vue'
// import { defineConfig } from 'vite'

// export default defineConfig({
//   plugins: [vue()],
//   base: '/joydeep/pyaudio/',
//   build: {
//     minify: true,
//     target: 'es2015',
//     outDir: 'dist',
//     assetsDir: 'assets',
//     sourcemap: false,
//   },
// })