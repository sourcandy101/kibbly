import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import { VitePWA } from "vite-plugin-pwa";

// On GitHub Pages the app is served under /kibbly/; locally it stays at the root.
const base = process.env.GITHUB_ACTIONS ? "/kibbly/" : "/";

export default defineConfig({
  base,
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["icon.svg"],
      manifest: {
        name: "Kibbly",
        short_name: "Kibbly",
        description: "Knows every dog. Feeds every dog.",
        theme_color: "#FFE7F0",
        background_color: "#FFE7F0",
        display: "standalone",
        start_url: "./",
        scope: "./",
        icons: [{ src: "icon.svg", sizes: "any", type: "image/svg+xml", purpose: "any" }],
      },
    }),
  ],
  test: {
    environment: "node",
    include: ["src/**/*.test.js"],
  },
});
