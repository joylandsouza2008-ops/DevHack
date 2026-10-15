// Welcome screen: a light, quiet brand landing (no pond picture, no fish) and
// the Start button that hands over to the dashboard.
//
// Motion: the flat Team Orbit logo fades in once (0.6 s). Nothing else on the
// start screen moves. Start fades the screen out and removes it.
// Accessibility: "reduce motion" means no fade at all; the dashboard is
// `inert` until Start.

(function () {
  "use strict";

  const welcome = document.getElementById("welcome");
  if (!welcome) return;

  const dashboard = document.getElementById("dashboard");
  const startButton = document.getElementById("welcome-start");

  const gsap = window.gsap;                     // bundled locally: /vendor/gsap/gsap.min.js
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  let entered = false;   // true once Start was pressed

  // ---------------------------------------------------------------- Start -> dashboard

  function finishEnter() {
    welcome.remove();                          // free the screen's memory and layers
    document.body.classList.remove("has-welcome");
    // Focus the pond status, or the heading of the page the address asked for (#/alerts ...).
    const status = document.getElementById("status");
    if (status.getClientRects().length) status.focus({ preventScroll: true });
    else if (window.Router) window.Router.focusPage();
  }

  function enter() {
    if (entered) return;
    entered = true;
    window.MeenuRaksha.start();                // connect to the data stream right away
    dashboard.removeAttribute("inert");

    if (!gsap || reduceMotion.matches) {
      finishEnter();
      return;
    }
    gsap.timeline({ onComplete: finishEnter })
      .to(welcome, { opacity: 0, duration: 0.4, ease: "power2.out" })
      // clearProps: a transform left on .dashboard would pin the phone tab bar
      // (position: fixed) to the page instead of the screen.
      .from(dashboard, { y: 18, duration: 0.6, ease: "power2.out", clearProps: "transform" }, 0.2);
  }

  startButton.addEventListener("click", enter);

  // ---------------------------------------------------------------- go

  // The only motion on the start screen: the logo fades in once.
  const logo = document.getElementById("welcome-logo");
  if (gsap && logo && !reduceMotion.matches) gsap.from(logo, { opacity: 0, duration: 0.6, ease: "power1.out" });
})();
