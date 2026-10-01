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

# Install the packages needed to read the datasets
pip install pandas openpyxl
```

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
