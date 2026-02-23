import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        midnight: "#0B0C10",
        nebula: "#5B2C6F",
        plasma: "#00E5FF"
      }
    }
  },
  plugins: []
};

export default config;
