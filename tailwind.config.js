export default {content: [
  './index.html',
  './src/**/*.{js,ts,jsx,tsx}'
],
  theme: {
    extend: {
      colors: {
        void: '#04070d',
        abyss: '#060c16',
        panel: '#08182b',
        edge: '#123a5c',
        ion: {
          DEFAULT: '#22d3ee',
          soft: '#7dd8f0',
          deep: '#0e7490',
        },
        signal: '#3b82f6',
        online: '#22c55e',
        alert: '#ef4444',
        muted: '#5c7d9c',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Orbitron', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        glow: '0 0 24px -6px rgba(34,211,238,0.45)',
      },
    },
  },
}
