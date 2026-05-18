/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'risk-low': '#16A34A',
        'risk-medium': '#D97706',
        'risk-high': '#EA580C',
        'risk-critical': '#DC2626',
      }
    },
  },
  plugins: [],
}
