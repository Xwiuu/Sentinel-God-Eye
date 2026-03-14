/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'obsidian': '#020202',
        'matrix-green': '#00ff41',
        'emergency-red': '#ff0000',
      }
    },
  },
  plugins: [],
}