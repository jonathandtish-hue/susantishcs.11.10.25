/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./website/**/*.html",
    "./generate_website_v5.py"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

