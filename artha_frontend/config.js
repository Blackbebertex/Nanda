// Auto-generated at build — do not edit
window.ARTHA_CONFIG = {
  BACKEND_URL: "http://localhost:8000",
};
(function () {
  var params = new URLSearchParams(window.location.search);
  var override = params.get("api") || params.get("backend");
  if (override) {
    window.ARTHA_CONFIG.BACKEND_URL = override.startsWith("http")
      ? override.replace(/\/$/, "")
      : "https://" + override.replace(/\/$/, "");
  }
})();
