import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
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
        start_url: "/",
        icons: [{ src: "icon.svg", sizes: "any", type: "image/svg+xml", purpose: "any" }],
      },
    }),
  ],
  test: {
    environment: "node",
    include: ["src/**/*.test.js"],
  },
});
