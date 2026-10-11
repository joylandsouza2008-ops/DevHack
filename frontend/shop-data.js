// Shop products (the #/shop page, frontend/shop.js). Plain data, no logic.
//
// Prices are ESTIMATED component costs in rupees, not offers: nothing is for
// sale yet and no payment is ever taken. Every price is shown as "est. ₹X"
// with "Estimated component cost. Prices may change." under the grid.
// If you change a price here, it changes everywhere (cards, cart, copied list).
//
// Each product: id, icon (a drawing in shop.js), price (₹, whole rupees) and,
// in English (en) and Kannada (kn): name, desc (short description),
// measures (what it measures) and why ("why you need it").

(function () {
  "use strict";

  const PRODUCTS = [
    {
      id: "test-kit",
      icon: "testKit",
      price: 1200,
      name: { en: "Ammonia + pH test kit", kn: "ಅಮೋನಿಯಾ + pH ಟೆಸ್ಟ್ ಕಿಟ್" },
      desc: { en: "Drops and a colour chart for a weekly check by hand.",
              kn: "ವಾರಕ್ಕೊಮ್ಮೆ ಕೈಯಿಂದ ಪರೀಕ್ಷಿಸಲು ಹನಿಗಳು ಮತ್ತು ಬಣ್ಣದ ಚಾರ್ಟ್." },
      measures: { en: "Ammonia, pH", kn: "ಅಮೋನಿಯಾ, pH" },
      why: { en: "Type the results into the app's test-kit form (More page) to see if the pond is safe.",
             kn: "ಫಲಿತಾಂಶವನ್ನು ಆ್ಯಪ್‌ನ ಟೆಸ್ಟ್ ಕಿಟ್ ಫಾರ್ಮ್‌ನಲ್ಲಿ (ಇತರೆ ಪುಟ) ನಮೂದಿಸಿ, ಕೊಳ ಸುರಕ್ಷಿತವೇ ಎಂದು ನೋಡಿ." },
    },
    {
      id: "night-watch",
      icon: "nightWatch",
      price: 23000,
      name: { en: "Night-Watch kit", kn: "ನೈಟ್-ವಾಚ್ ಕಿಟ್" },
      desc: { en: "Optical oxygen (DO) and temperature sensor, ESP32 board, 4G, solar panel, in a waterproof IP65 box.",
              kn: "ಆಪ್ಟಿಕಲ್ ಆಮ್ಲಜನಕ (DO) ಮತ್ತು ತಾಪಮಾನ ಸೆನ್ಸರ್, ESP32 ಬೋರ್ಡ್, 4G, ಸೌರ ಫಲಕ, ನೀರು ನುಗ್ಗದ IP65 ಪೆಟ್ಟಿಗೆಯಲ್ಲಿ." },
      measures: { en: "Dissolved oxygen, water temperature", kn: "ಕರಗಿದ ಆಮ್ಲಜನಕ, ನೀರಿನ ತಾಪಮಾನ" },
      why: { en: "Watches oxygen all night and warns you before dawn, when fish are most at risk.",
             kn: "ರಾತ್ರಿಯಿಡೀ ಆಮ್ಲಜನಕವನ್ನು ಗಮನಿಸಿ, ಮೀನುಗಳಿಗೆ ಹೆಚ್ಚು ಅಪಾಯವಿರುವ ಬೆಳಗಿನ ಜಾವಕ್ಕೂ ಮೊದಲೇ ಎಚ್ಚರಿಸುತ್ತದೆ." },
    },
    {
      id: "full-pond",
      icon: "fullPond",
      price: 35000,
      name: { en: "Full Pond kit", kn: "ಫುಲ್ ಪಾಂಡ್ ಕಿಟ್" },
      desc: { en: "The Night-Watch kit plus an industrial pH probe with a signal isolator.",
              kn: "ನೈಟ್-ವಾಚ್ ಕಿಟ್ ಜೊತೆಗೆ ಸಿಗ್ನಲ್ ಐಸೊಲೇಟರ್ ಇರುವ ಕೈಗಾರಿಕಾ pH ಪ್ರೋಬ್." },
      measures: { en: "Dissolved oxygen, water temperature, pH", kn: "ಕರಗಿದ ಆಮ್ಲಜನಕ, ನೀರಿನ ತಾಪಮಾನ, pH" },
      why: { en: "Adds pH, day and night, to the overnight oxygen watch.",
             kn: "ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಕಾವಲಿನ ಜೊತೆಗೆ ಹಗಲು-ರಾತ್ರಿ pH ಅನ್ನೂ ಗಮನಿಸುತ್ತದೆ." },
    },
    {
      id: "do-cap",
      icon: "sensorCap",
      price: 4000,
      name: { en: "Spare: DO sensor cap", kn: "ಬಿಡಿಭಾಗ: DO ಸೆನ್ಸರ್ ಕ್ಯಾಪ್" },
      desc: { en: "Replacement cap for the optical oxygen sensor.",
              kn: "ಆಪ್ಟಿಕಲ್ ಆಮ್ಲಜನಕ ಸೆನ್ಸರ್‌ಗೆ ಬದಲಿ ಕ್ಯಾಪ್." },
      measures: { en: "Part of the oxygen sensor", kn: "ಆಮ್ಲಜನಕ ಸೆನ್ಸರ್‌ನ ಭಾಗ" },
      why: { en: "The cap wears out over time and must be replaced to keep oxygen readings right.",
             kn: "ಕಾಲಾನಂತರದಲ್ಲಿ ಕ್ಯಾಪ್ ಸವೆಯುತ್ತದೆ. ಆಮ್ಲಜನಕದ ಅಳತೆ ಸರಿಯಾಗಿರಲು ಅದನ್ನು ಬದಲಾಯಿಸಬೇಕು." },
    },
    {
      id: "solar-10w",
      icon: "solar",
      price: 1500,
      name: { en: "Spare: 10 W solar panel + charge board", kn: "ಬಿಡಿಭಾಗ: 10 W ಸೌರ ಫಲಕ + ಚಾರ್ಜ್ ಬೋರ್ಡ್" },
      desc: { en: "Panel and charging board that keep the sensor box powered.",
              kn: "ಸೆನ್ಸರ್ ಪೆಟ್ಟಿಗೆಗೆ ವಿದ್ಯುತ್ ನೀಡುವ ಫಲಕ ಮತ್ತು ಚಾರ್ಜಿಂಗ್ ಬೋರ್ಡ್." },
      measures: { en: "Power for the sensor box", kn: "ಸೆನ್ಸರ್ ಪೆಟ್ಟಿಗೆಗೆ ವಿದ್ಯುತ್" },
      why: { en: "Replaces a panel or board damaged by weather, so the sensor keeps running.",
             kn: "ಹವಾಮಾನದಿಂದ ಹಾಳಾದ ಫಲಕ ಅಥವಾ ಬೋರ್ಡ್ ಬದಲಿಸಿ, ಸೆನ್ಸರ್ ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳುತ್ತದೆ." },
    },
  ];

  const api = { PRODUCTS };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }   // Node tests
  window.ShopData = api;
})();
