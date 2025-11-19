/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['EB Garamond', 'Georgia', 'serif'],
      },
      colors: {
        warm: {
          50: 'hsl(40, 35%, 96%)',
          100: 'hsl(38, 30%, 88%)',
          200: 'hsl(36, 28%, 80%)',
          300: 'hsl(34, 26%, 70%)',
          400: 'hsl(32, 24%, 60%)',
          500: 'hsl(30, 22%, 50%)',
          600: 'hsl(145, 32%, 48%)',
          700: 'hsl(145, 35%, 40%)',
          800: 'hsl(145, 40%, 25%)',
          900: 'hsl(145, 45%, 15%)',
        },
      },
    },
  },
  plugins: [],
}

