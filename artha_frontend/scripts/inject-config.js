/**
 * Injects production BACKEND_URL into config.js for Render static deploy.
 */
const fs = require("fs");
const path = require("path");

const raw = process.env.BACKEND_URL || process.env.RENDER_EXTERNAL_URL || "http://localhost:8000";
const backendUrl = raw.startsWith("http") ? raw : `https://${raw}`;

const config = `// Auto-generated at build time
window.ARTHA_CONFIG = {
  BACKEND_URL: "${backendUrl.replace(/\/$/, "")}",
};
`;

const out = path.join(__dirname, "..", "config.js");
fs.writeFileSync(out, config, "utf8");
console.log("Wrote config.js with BACKEND_URL =", backendUrl);
