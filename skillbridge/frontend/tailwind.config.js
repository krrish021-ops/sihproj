export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: '#12202B',
        paper: '#FBF9F4',
        blueprint: {
          DEFAULT: '#0E2A47',
          mid: '#163A5F',
          line: '#2F5C86',
          50: '#EAF1F7',
          100: '#D7E4F0',
        },
        gold: {
          DEFAULT: '#D9A441',
          dark: '#B8842E',
          light: '#F1DBA3',
        },
        success: '#3D8361',
        danger: '#C1443C',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        body: ['"Inter"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
      backgroundImage: {
        'blueprint-grid': "linear-gradient(rgba(47,92,134,0.35) 1px, transparent 1px), linear-gradient(90deg, rgba(47,92,134,0.35) 1px, transparent 1px)",
      },
      backgroundSize: {
        'grid-24': '24px 24px',
      },
    },
  },
  plugins: [],
}
