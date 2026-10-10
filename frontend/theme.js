// Theme before the first paint (no flash): the saved choice, else the phone's
// light/dark setting. The toggle in the top bar changes it (app.js).
// Loaded in <head> before the styles; it is a file so the page needs no inline scripts.
(function () {
  var theme = null;
  try { theme = localStorage.getItem("meenuraksha-theme"); } catch (e) { /* storage blocked */ }
  if (theme !== "light" && theme !== "dark") {
    theme = window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  }
  document.documentElement.setAttribute("data-theme", theme);
})();
