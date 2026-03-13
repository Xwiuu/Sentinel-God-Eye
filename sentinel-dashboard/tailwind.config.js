/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: '#0f172a',
        panel: '#1e293b',
        primary: '#00ffcc',
        danger: '#ff0033'
      }
    },
  },
  plugins: [],
}