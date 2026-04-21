/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        cyber: ['"Press Start 2P"', 'cursive'],
        sans: ['Poppins', 'sans-serif'],
        mono: ['"Roboto Mono"', 'monospace'],
      },
      colors: {
        'ctf-dark': '#0B0E14',
        'ctf-surface': '#161B22',
        'ctf-primary': '#00F5FF',
        'ctf-accent': '#7000FF',
      }
    }, // Fin de extend
  }, // Fin de theme
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      {
        'piscine-dark': {
          "primary": "#00BABC",
          "secondary": "#7000FF",
          "accent": "#FF0055",
          "neutral": "#1E293B",
          "base-100": "#05070A",
          "base-200": "#0D1117",
          "base-300": "#161B22",
          "base-content": "#E6EDF3",
          "info": "#0CA5E9",
          "success": "#238636",
          "warning": "#F59E0B",
          "error": "#EF4444",
        },
      },
      {
        'piscine-light': {
          "primary": "#00BABC",
          "secondary": "#4338CA",
          "accent": "#E11D48",
          "neutral": "#E5E7EB",
          "base-100": "#F3F4F6",
          "base-200": "#FFFFFF",
          "base-300": "#E5E7EB",
          "base-content": "#1F2937",
          "info": "#0284C7",
          "success": "#16A34A",
          "warning": "#D97706",
          "error": "#DC2626",
        },
      }
    ],
  },
}