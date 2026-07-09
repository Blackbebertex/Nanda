// Runtime config — override BACKEND_URL for production (Render sets via build script)
window.ARTHA_CONFIG = {
  BACKEND_URL: window.ARTHA_BACKEND_URL || "http://localhost:8000",
};
