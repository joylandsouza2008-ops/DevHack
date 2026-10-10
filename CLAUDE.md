# AquaNexus — DevHack 2026, PS 1.1
Early-warning web app for small aquaculture farmers in coastal Karnataka.
Predicts pond water-quality risk (Safe / Warning / Danger) and shows alerts in Kannada + English.

## Stack
- Backend: Python, FastAPI, scikit-learn
- Frontend: HTML, Tailwind, JavaScript, GSAP/Lottie animations, Chart.js
- Data: Aquaculture Water Dataset (Mendeley), Pondsdata (Kaggle)
- Software only, no hardware. Sensor data is simulated from datasets.

## Rules
- I'm a beginner in Python; explain what each file does.
- Build the core (model + API + basic page) before animations.
- Follow DESIGN.md for all styling.
- After building UI, test it with playwright-cli and take screenshots.
- Simulated data (backend/simulator.py) must be labelled "Simulated data" / "ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ" wherever the app shows it, and must never be used to train or report model accuracy.
