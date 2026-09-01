/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: '#0E2A47',
          mid: '#163A5F',
          line: '#2F5C86',
          50: '#EEF3F9',
          100: '#D6E1EE',
        },
        gold: {
          DEFAULT: '#D9A441',
          dark: '#B8842E',
          light: '#F1DBA3',
        },
        paper: '#FBF9F4',
        ink: '#12202B',
        success: '#3D8361',
        danger: '#C1443C',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
};
