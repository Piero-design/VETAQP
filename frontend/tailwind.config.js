/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        brand: '#2563EB',  // azul principal
        mint: '#10B981',   // verde menta
        ink: '#1F2937'     // texto oscuro
      },
      borderRadius: {
        '2xl': '1rem'
      }
    }
  },
  plugins: []
}
