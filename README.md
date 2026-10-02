# MeenuRaksha

Early-warning web app for small aquaculture farmers in coastal Karnataka.
It predicts pond water-quality risk (**Safe / Warning / Danger**) and shows alerts in Kannada and English.
Software only: sensor readings are simulated from public datasets.

Built for DevHack 2026, problem statement 1.1.

## Project layout

| Path | What it is |
|---|---|
| `CLAUDE.md` | Project brief and working rules for Claude Code |
| `DESIGN.md` | Design system: colors, type, components, Kannada support |
| `config/thresholds.toml` | All Safe / Warning / Danger threshold numbers, with their sources |
| `backend/risk_classifier.py` | Rule-based classifier: readings → risk level + reason |
| `backend/risk_messages.py` | Farmer-facing alert text in English and Kannada |
| `backend/do_features.py` | Builds the DO-forecast inputs from recent readings (shared by training and app) |
| `backend/do_forecast.py` | Loads the saved model, forecasts DO 1/3/6 h ahead (experiment only, not shown in the app) |
| `backend/time_to_danger.py` | "Time until danger": if DO is falling, when it may reach 3 mg/L (English + Kannada) |
| `backend/simulator.py` | **Simulated** demo readings (normal day / night oxygen crash). Demo only, never for accuracy |
| `backend/health_score.py` | Pond health score 0–100, always inside its status's range (Safe 75–100, Warning 40–74, Danger 0–39) |
| `backend/main.py` | FastAPI web server: API endpoints + serves the page |
| `ml/train_do_forecast.py` | Trains and evaluates the DO forecast (`python -m ml.train_do_forecast`) |
| `ml/experiment_3h_average.py` | Experiment: forecasting the 3-hour average DO (not adopted, see docs) |
| `ml/evaluate_time_to_danger.py` | Checks "time until danger" on real Pondsdata (`python -m ml.evaluate_time_to_danger`) |
| `models/` | Saved DO forecast model and its test scores |
| `tests/` | Automated tests (`python -m pytest`; browser-side logic: `node --test tests/js`). `tests/conftest.py` blocks the real internet and stops any test that runs over 60 s |
| `docs/thresholds.md` | Threshold table, decisions and sources (for the presentation) |
| `docs/do_forecast.md` | DO forecast method, results and chart (for the presentation) |
| `docs/health_score.md` | How the 0–100 health score is worked out, with examples |
| `docs/time_to_danger.md` | "Time until danger" method and results on real + simulated data |
| `docs/screenshots/` | App screenshots (simulated demo) |
| `frontend/` | The web page: `index.html`, dashboard (`styles.css`, `app.js`), welcome screen (`welcome.css`, `welcome.js`) |
| `frontend/health-ring.js`, `history.js`, `voice.js` | Health score ring, alert history (saved in the browser), voice alerts (phone's own voices, only when tapped) |
| `frontend/vendor/gsap/` | GSAP 3.15.0 animation library, bundled locally (works offline) |
| `frontend/assets/` | Dashboard background waves: original artwork + brand-blue copies (`*-brand.svg`) used by the app |
| `tools/recolor_backgrounds.py` | Regenerates the brand-blue wave copies after the artwork is edited |
| `frontend/fonts/` | Noto Sans + Noto Sans Kannada, bundled so the app works offline |
| `.claude/skills/` | Shared Claude Code skills for the team |
| `data/` | Datasets. **Not in git**: download them yourself (steps below) |

## Setup

```bash
git clone https://github.com/joylandsouza2008-ops/DevHack.git
cd DevHack

# Create a Python virtual environment (a private package folder for this project)
python -m venv .venv

# Activate it
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# Install the packages this project needs
pip install -r requirements.txt

# Run the tests
python -m pytest
node --test tests/js          # browser-side logic (needs Node.js)

# Start the app, then open http://127.0.0.1:8000  (API docs: http://127.0.0.1:8000/docs)
uvicorn backend.main:app --reload
```

The app shows **simulated** demo data, clearly labelled "Simulated data". Pick a pond and a scenario (Normal day / Night oxygen crash). Each second of real time is 20 minutes of simulated time.

On Windows, if printing Kannada text in the terminal gives a `UnicodeEncodeError`, run `set PYTHONIOENCODING=utf-8` first (PowerShell: `$env:PYTHONIOENCODING="utf-8"`).

## Datasets

The `data/` folder is listed in `.gitignore`, so every teammate downloads the datasets once. After both steps below, it should look exactly like this (file names must match):

```
data/
├── Aquaculture - Water Quality Dataset/
│   └── WQD.xlsx
├── Aquaponds Dataset.csv
├── Fish Ponds.csv
├── Ponds data.csv
├── Ponds.csv
└── Ponds1.csv
```

### 1. Aquaculture Water Quality Dataset (Mendeley)

1. Open https://data.mendeley.com/datasets/y78ty2g293/2 (DOI: 10.17632/y78ty2g293.2).
2. Click **Download All** and unzip it.
3. Put `WQD.xlsx` in `data/Aquaculture - Water Quality Dataset/`.

### 2. Pondsdata (Kaggle)

1. Open https://www.kaggle.com/datasets/apgopi/pondsdata (a free Kaggle account is required).
2. Click **Download**, unzip, and put the five `.csv` files directly in `data/`.

Or, with the [Kaggle CLI](https://github.com/Kaggle/kaggle-api) set up:

```bash
kaggle datasets download -d apgopi/pondsdata -p data --unzip
```

### Check your download

```bash
python -c "import pandas as pd; print(pd.read_excel('data/Aquaculture - Water Quality Dataset/WQD.xlsx').shape, pd.read_csv('data/Ponds data.csv', low_memory=False).shape)"
```

Expected output: `(4300, 15) (74796, 11)`

### What's in each file

| File | Rows × cols | Target column | Notes |
|---|---|---|---|
| `WQD.xlsx` (Mendeley) | 4,300 × 15 | `Water Quality`: 0 = Excellent, 1 = Good, 2 = Poor | 14 water parameters. No missing values. Looks synthetic: some values are physically unrealistic (temperature up to 84 °C, pH 0–14). |
| `Ponds data.csv` (Kaggle) | 74,796 × 11 | `label`: 0 / 1 (meaning not documented) | Main file: 3 ponds in Guntur, AP, Feb 2022 – Jan 2023, a reading roughly every 20 min. 38 blank rows, a few `#VALUE!` cells, 37 duplicate rows. |
| `Fish Ponds.csv` (Kaggle) | 74,758 × 8 | `label`: 0 / 1 | Same readings as `Ponds data.csv`, with station/date/time removed. No missing values. |
| `Ponds1.csv` (Kaggle) | 74,796 × 10 | none | Same readings as `Ponds data.csv`, without the label. |
| `Aquaponds Dataset.csv` (Kaggle) | 50,000 × 11 | `label_3class`: 0 / 1 / 2 (meaning not documented) | Shuffled 50k sample of the same readings, with an exactly balanced 3-class label. |
| `Ponds.csv` (Kaggle) | 18,102 × 9 | none | A separate, lower-resolution recording (Feb – Apr 2022), with different value ranges. No label. |

Kaggle sensor columns: `NITRATE(PPM)`, `PH`, `AMMONIA(mg/l)`, `TEMP`, `DO`, `TURBIDITY`, `MANGANESE(mg/l)`.
