const { transform } = require("typescript");

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ["./pages/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./app/**/*.{ts,tsx}", "./src/**/*.{ts,tsx}"],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        primary: {
          DEFAULT: "#000835",
          dark: "#3A8BFF",
          light: "#F9A826",
        },
        secondary: {
          DEFAULT: "#3A8BFF",
          dark: "#B2D5FF",
          light: "#F9A826",
        },
        tertiary: {
          DEFAULT: "#C5D5F9",
          dark: "#C5D5F9",
          light: "#F9A826",
        },
        neutral: {
          DEFAULT: "#FFFFFF",
          dark: "#F9A826",
          light: "#F9A826",
        },

        placeholder: {
          DEFAULT: "#64748b",
          dark: "#170206",
          light: "#170206",
        },
        hover: {
          DEFAULT: "#1D4ED8",
          dark: "#170206",
          light: "#170206",
        },
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
        blob: {
          "0%": {
            transform: "translate(0px, 0px) scale(1)",
          },
          "33%": {
            transform: "translate(30px, -50px) scale(1.1)",
          },
          "66%": {
            transform: "translate(-20px, 20px) scale(0.9)",
          },
          "100%": {
            transform: "tranlate(0px, 0px) scale(1)",
          },
        },
        test: {
          "0%": {
            transform: " rotate(0deg) translate(120px, 20px) scale(0.7)",
          },
          "50%": {
            transform: " rotate(180deg) translate(120px, 20px) scale(0.5)",
          },

          "100%": {
            transform: "rotate(360deg) translate(120px, 20px) scale(0.7)",
          },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.3s ease-out",
        "accordion-up": "accordion-up 0.3s ease-out",
        blob: "blob 7s infinite",
        test: "test 7s  infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
