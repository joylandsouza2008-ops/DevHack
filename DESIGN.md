---
version: alpha
name: pond-design-system
description: A calm, deep-water design system for a pond and fish-health app, in two themes from one Realtime Colors palette. Dark (default) puts light pond blue ({colors.primary}) on deep indigo ({colors.background}); light, for bright outdoor sunlight, puts a deepened pond blue ({colors.light-primary}) on pale indigo-white ({colors.light-background}) with the indigo as text. Bright cyan ({colors.secondary}) fills small tags and highlights with dark text; magenta ({colors.accent}) stays in the palette but is not used in the interface. A strict three-level status palette (Safe green, Warning amber, Danger red) is reserved for pond and fish condition readings only, identical in both themes. Type is set large for readability outdoors and on low-end phones, and every text style is tuned to render Kannada (ಕನ್ನಡ) script as comfortably as English.

colors:
  # Dark theme (default): the team's Realtime Colors palette, exact values
  background: "#060351"      # deep indigo
  text: "#def0f8"
  primary: "#88cce6"         # light pond blue: every action
  primary-pressed: "#a8daee"
  on-primary: "#060351"
  secondary: "#23bcd0"       # bright cyan fill, always with dark text
  on-secondary: "#060351"
  edge-on-secondary: "#060351"   # dashed borders / border trail on secondary fills
  accent: "#a10c9f"          # magenta: kept in the palette, NOT used in the interface (see Colors)
  on-accent: "#def0f8"
  # Status: unchanged
  safe: "#1a7f37"
  safe-bg: "#e6f4ea"
  safe-text: "#0d4d20"
  warning: "#f5a524"
  warning-bg: "#fff3dc"
  warning-text: "#7a4100"
  on-warning: "#1a1200"
  danger: "#c62828"
  danger-bg: "#fdecea"
  danger-text: "#7f1414"
  on-status: "#ffffff"       # text on the solid Safe / Danger colours
  # Dark-theme surfaces and text, derived from the palette (all contrast-checked)
  surface: "#08054a"         # top bar, sections
  canvas: "#07044a"          # cards, inputs (--card in styles.css); as dark as the page so Danger stripes keep 3:1
  hairline: "#262470"
  hairline-soft: "#1a1860"
  hairline-strong: "#6f73b8"  # input and control borders (4.3:1 on canvas)
  text-secondary: "#b3c6e6"
  text-tertiary: "#9aa9d6"
  muted: "#6a6fa6"           # disabled only
  footer-bg: "#03022c"
  # Light theme (bright sunlight), made from the same palette. Status colours above are shared, unchanged.
  light-background: "#eceefa"
  light-text: "#060351"      # the palette's indigo
  light-primary: "#17698e"   # pond blue, deepened for light text on it
  light-primary-pressed: "#0f4f6c"
  light-on-primary: "#f4fbfe"
  light-secondary: "#23bcd0" # same cyan: fill only on this page (2.0:1)
  light-on-secondary: "#060351"
  light-edge-on-secondary: "#060351"
  light-accent: "#a10c9f"    # same magenta, not used
  light-on-accent: "#f8f0fb"
  light-surface: "#f6f7fd"
  light-canvas: "#fcfcff"
  light-hairline: "#d3d6ee"
  light-hairline-strong: "#646a99"
  light-text-secondary: "#2c2f6b"
  light-text-tertiary: "#4a4e85"
  light-muted: "#8d90b5"
  light-footer-bg: "#dfe2f5"
  light-warning-edge: "#7a4100"   # = warning-text: dark edge on amber stripes (amber is 2.0:1 on light cards)

---

## Overview

This is a calm, deep-water design system for a pond and fish-health app. It is used by pond owners and fish farmers, often outdoors, on phones, and in either Kannada or English. One Realtime Colors palette gives two themes:

- **Dark (default): black and white only.** Background #0A0A0A, cards #141414, lines #262626, text #FFFFFF, muted text #A3A3A3. Every action, link, active tab, toggle and chart line is white or grey; primary buttons and the chosen language / theme are **white with black text**; the logo is white. **No teal, blue or navy anywhere.** The only colours are the status colours (Safe green, Warning amber, Danger red) on alerts, badges, the status strip, the health score and the risk scale, because they carry safety meaning. (The Indigo values in the YAML header above are the light theme's night pictures, see Themes.)
- **Light, for bright outdoor sunlight:** pale indigo-white ({colors.light-background}) with the palette's indigo as text ({colors.light-text}). The main action is a deepened pond-blue pill ({colors.light-primary}) with light text.

Bright cyan ({colors.secondary}) fills small tags and highlighted items, always with dark text. **Colour only means something**: pond blue is the brand and every action, and green, amber and red are Safe, Warning and Danger. Magenta ({colors.accent}) stays in the palette but is **not used** anywhere on screen: no doodles, glows or decorative lines. The first theme follows the phone's light/dark setting; a **Light | Dark** toggle in the top bar overrides it and is remembered. The pictures (welcome pond, sky scene, pond view) show night water and stay dark in both themes.

The most important job of the interface is to make pond condition clear at a glance. Green, amber and red mean only one thing each: **Safe**, **Warning** and **Danger**. These colors never appear as decoration, and each status always comes with an icon and a word, never color alone. Status colours are identical in both themes. On the dark page, status banners keep their light backgrounds, so alerts are the brightest thing on screen; on the light page their 2px solid status border sets them apart.

Text is set larger than a typical web app: body text is 18px, and nothing that must be read is smaller than 15px. Every style is tuned so Kannada (ಕನ್ನಡ) renders as comfortably as English, with generous line height and no negative letter-spacing.

**Key Characteristics:**
- Deep indigo (dark) or pale indigo-white (light) with pond-blue CTAs ({colors.primary}, 12px corners like the cards)
- Bright cyan ({colors.secondary}) for small tags and highlighted items, always with dark text
- Calm and flat: one colour per meaning, hairline borders, no decorative shadows, glows, blobs or waves
- Motion only where it means something: a level change, a reading moving, the countdown, a Danger alert
- No emoji anywhere (screens, SMS, WhatsApp): one outline icon set, and words for levels
- A strict Safe/Warning/Danger palette used only for condition status, always paired with an icon and a label
- Large, readable type: 18px body, 52px-tall buttons, 48px minimum touch targets
- Noto Sans + Noto Sans Kannada on every surface, with line heights tall enough for Kannada vowel signs and conjuncts
- Darkest-water footer ({colors.footer-bg})

## Colors

All contrast ratios below are measured (WCAG 2.x formula). Text needs at least 4.5:1; borders, stripes and icons need at least 3:1.

### Dark theme (default): black and white

| Token | Hex | Use | Contrast |
|---|---|---|---|
| **Background** | `#0A0A0A` | Page, footer, phone tab bar | white text 19.8:1 |
| **Card / Surface** | `#141414` | Cards, top bar, notes, inner panels | white text 18.4:1; muted #A3A3A3 7.3:1 |
| **Lines** | `#262626` | Hairlines, dividers, the start page's orbit circles | decorative |
| **Control borders** | `#737373` | Inputs, selects, toggles | 3.9:1 on cards |
| **Text / Muted** | `#FFFFFF` / `#A3A3A3` | Text / secondary text, units | |
| **Primary** | `#FFFFFF`, text on it `#000000` | Buttons, active tab, chosen toggle, links, focus ring, chart line | black on white 21:1 |
| **Secondary fill** | `#D4D4D4`, text on it `#000000` | "Simulated data" chips, tags, the chosen pond | 14:1 |
| **Status** | unchanged | Safe / Warning / Danger, as in the light theme | stripes on cards: Safe 3.6:1, Danger 3.3:1, Warning 9.0:1 |

`tests/test_contrast.py` checks that every dark-theme colour token is a grey (red = green = blue), except the status colours and the unused magenta.

### Previous dark palette (kept for reference; no longer used)
| Token | Hex | Use | Contrast |
|---|---|---|---|
| **Background** ({colors.background}) | `#060351` | Page background (deep indigo) | text on it 15.7:1 |
| **Text** ({colors.text}) | `#def0f8` | Headlines and body text | 15.9:1 on cards |
| **Primary** ({colors.primary}) | `#88cce6` | Primary buttons, active tabs, links, focus rings, highlighted-card borders | 10.4:1 on background; dark text on it 10.4:1 |
| **Primary Pressed** ({colors.primary-pressed}) | `#a8daee` | Pressed state of primary buttons | dark text on it 12.2:1 |
| **On Primary** ({colors.on-primary}) | `#060351` | Text on primary | |
| **Secondary** ({colors.secondary}) | `#23bcd0` | **Fill**: "Simulated data" chip, tags, selected pond, WhatsApp bubble | dark text on it 8.1:1 |
| **Edge on Secondary** ({colors.edge-on-secondary}) | `#060351` | A dark edge on a secondary fill, when one is needed | 8.1:1 on secondary |
| **Accent** ({colors.accent}) | `#a10c9f` | **Not used in the interface** (see below) | 2.7:1 on the background |

### Brand palette: light theme (bright sunlight)
Made from the same palette: the indigo becomes the text, the pond blue is deepened so light text sits on it, and cyan and magenta are used unchanged.

| Token | Hex | Use | Contrast |
|---|---|---|---|
| **Background** ({colors.light-background}) | `#eceefa` | Page background | text on it 16.0:1 |
| **Text** ({colors.light-text}) | `#060351` | Headlines and body text | 18.0:1 on cards |
| **Primary** ({colors.light-primary}) | `#17698e` | Same jobs as dark primary | 5.3:1 on background; light text on it 5.8:1 |
| **Primary Pressed** ({colors.light-primary-pressed}) | `#0f4f6c` | Pressed primary buttons (darker, not lighter) | light text on it 8.5:1 |
| **On Primary** ({colors.light-on-primary}) | `#f4fbfe` | Text on primary: **light** in this theme | |
| **Secondary** ({colors.light-secondary}) | `#23bcd0` | Fill, as in dark | dark text on it 8.1:1; **2.0:1 on the page, so fill only, never text or a border** |
| **Edge on Secondary** ({colors.light-edge-on-secondary}) | `#060351` | Dashed borders / border trail on secondary | 8.1:1 on secondary |
| **Accent** ({colors.light-accent}) | `#a10c9f` | Not used, as in dark | 5.9:1 on the background |
| **Surface / Canvas** | `#f6f7fd` / `#fcfcff` | Top bar and sections / cards and inputs | |
| **Text Secondary / Tertiary** | `#2c2f6b` / `#4a4e85` | Secondary / tertiary text | 11.9:1 / 7.5:1 on cards |
| **Hairline / Hairline Strong** | `#d3d6ee` / `#646a99` | Dividers / control borders | strong 5.0:1 on cards |
| **Footer** ({colors.light-footer-bg}) | `#dfe2f5` | Bottom toolbar | |

Tokens with no light value (status colours, the font) are shared by both themes.

**The accent (magenta) is not used.** Colour only means something in this app (brand or status), and a decorative magenta next to Danger red read as a second alarm colour. The token stays in the palette; `tests/test_contrast.py` checks that no style or script uses it. The fish drawings in the disease guide are one-colour line art in the text colour.

**Accent vs status colours, including colour blindness** (OKLab difference x100, 15+ = clearly different; colour blindness simulated with Machado et al. 2009):

| | Normal vision | Protanopia | Deuteranopia | Tritanopia |
|---|---|---|---|---|
| vs **Danger** red | 21 | 21 | 21 | **12** |
| vs Warning amber | 41 | 42 | 39 | 28 |
| vs Safe green | 36 | 26 | 17 | 26 |

For the common red-green colour blindness (protanopia, deuteranopia) the magenta stays clearly different from Danger red. For **tritanopia** (blue-yellow, about 1 in 10 000 people) it becomes a dark rose only 12 apart from red: one more reason it is not used on screen (see Known Gaps).

**Secondary vs primary:** cyan and pond blue are close (difference 9), so never use secondary as the only difference from primary. Clickable things are always {colors.primary}; secondary is a fill with dark text.

### Status (Safe / Warning / Danger), unchanged
These colors are reserved for pond and fish condition: water quality, oxygen, temperature, pH, ammonia and alerts.

| Level | Solid | Background | Text on background | Icon | Contrast |
|---|---|---|---|---|---|
| **Safe** | {colors.safe} `#1a7f37` | {colors.safe-bg} | {colors.safe-text} | check-circle | white ({colors.on-status}) on solid 5.1:1 · text on bg 8.8:1 · solid on cards: dark 3.7:1, light 5.0:1 |
| **Warning** | {colors.warning} `#f5a524` | {colors.warning-bg} | {colors.warning-text} | alert-triangle | dark ({colors.on-warning}) on solid 9.1:1 · text on bg 7.4:1 · solid on cards: dark 9.1:1, **light 2.0:1** (see below) |
| **Danger** | {colors.danger} `#c62828` | {colors.danger-bg} | {colors.danger-text} | alert-octagon | white ({colors.on-status}) on solid 5.6:1 · text on bg 9.1:1 · solid on cards: dark 3.3:1, light 5.5:1 |

- Status colors are always used as these fixed pairs. **Status text colors only ever sit on their own light status background**: Danger text directly on the dark page is 1.8:1 and unreadable.
- On dark cards ({colors.canvas}) the solid colors pass 3:1 as left-border stripes (Safe 3.7, Warning 9.1, Danger 3.3). The dark cards are kept as dark as the indigo page for this reason: a lighter, bluer card drops Danger below 3:1.
- **Light theme, amber:** amber is only 2.0:1 on light cards, so amber stripes and timeline dots get a 2px dark amber edge ({colors.light-warning-edge}, which is the unchanged warning-text, 8.0:1 on cards). Amber shapes without an edge (gauge arc, health ring) always sit next to the Warning word and icon.
- Text on the amber Warning solid is always dark ({colors.on-warning}). White text on amber fails contrast.
- Red and green look alike to color-blind users. The **icon shape and the word** (Safe / ಸುರಕ್ಷಿತ, Warning / ಎಚ್ಚರಿಕೆ, Danger / ಅಪಾಯ) are what carry the meaning; color only reinforces it.

### Surface (dark theme values; the light theme's are in its table above)
- **Background** ({colors.background}): Page background.
- **Surface** ({colors.surface}): Top bar and section backgrounds.
- **Canvas** ({colors.canvas}): Cards and inputs.
- **Hairline** ({colors.hairline}) / **Hairline Soft** ({colors.hairline-soft}): Decorative 1px borders and dividers.
- **Hairline Strong** ({colors.hairline-strong}): Input and control borders (4.3:1 on cards, 4.2:1 on the background).
- **Footer** ({colors.footer-bg}): Darkest water, for the footer.

### Text
- **Text** ({colors.text}): Headlines and body text (15.9:1 on cards).
- **Text Secondary** ({colors.text-secondary}): Secondary text and metadata (10.8:1 on cards).
- **Text Tertiary** ({colors.text-tertiary}): Tertiary text and placeholders (8.0:1 on cards). This is the dimmest color allowed for readable text.
- **Muted** ({colors.muted}): Disabled labels only (dark 3.9:1, light 3.0:1). Never use it for text people need to read.
- **On Secondary** ({colors.on-secondary}): Dark text on the cyan secondary fill (8.1:1).

### Themes
- `styles.css` defines the dark (black and white) tokens on `:root` and the light overrides on `:root[data-theme="light"]`. A small script in `index.html` sets `data-theme` before the first paint: the saved choice (`localStorage` key `meenuraksha-theme`), else `prefers-color-scheme`.
- **Pond view** (`pond-view.js`): a flat picture that follows the theme: a rounded rectangle of water in one flat colour, three flat fish swimming slowly, and small bubbles rising. More oxygen, more bubbles (2 at 0 mg/L, up to 16 at 12 mg/L); the fish slow down in Warning and more in Danger. Light: soft teal water (`--pond-water` #CFE8EA) with deep teal fish; dark: dark grey water (#262626) with light grey fish. No gradients and no Three.js; 30 fps at most, stops off screen or in a hidden tab, still with "reduce motion".
- **Start page** follows the theme: light in light mode; black and white in dark mode (white logo and text, white Start button with black text, dark language box with the chosen language white).
- **Known exception:** the sensor-kit wiring diagram in the Shop keeps its own colours (orange, blue, grey) in dark mode, because its legend uses them to tell power, control and sensor parts apart. It sits on #141414.
- **Plain page:** the page is one flat colour. No background waves, blobs, glows or gradient washes behind the cards.
- **Simulated clock:** one plain line above the status, "Simulated time: 15 Oct, 20:20, Night", with the "Simulated data" tag. No night-scene illustration.
- `tests/test_contrast.py` checks every pair in both themes and that the page stays flat (no waves, doodles, decorative shadows, magenta, illustrations that are only decoration, or Three.js).

## Typography

### Font Family
**Manrope** for titles and big numbers (page titles, section headings, the status word, readings, the health score, the countdown), via `--font-display`. It has Latin letters only, so Kannada letters in a title fall back to Noto Sans Kannada, letter by letter. Bundled in `frontend/fonts/` (SIL Open Font License), like the others.

**Noto Sans** (Latin) + **Noto Sans Kannada** (Kannada) for everything else, both under the SIL Open Font License. The two are designed to match, so mixed Kannada and English lines (for example, "ಆಮ್ಲಜನಕ 6.2 mg/L") share the same weight and baseline.

**The fonts are bundled locally, so the app works on cheap phones and slow internet.** Never load them from Google Fonts or any other CDN. They live in `frontend/fonts/`, and every page links the local stylesheet:

```html
<link rel="stylesheet" href="/fonts/fonts.css">
```

```css
font-family: "Noto Sans", "Noto Sans Kannada", "Tunga", "Nirmala UI", system-ui, sans-serif;
```

- The `.woff2` files are variable fonts: one file per script covers every weight from 400 to 700.
- `unicode-range` means a browser only downloads the Kannada file on pages that contain Kannada text.
- `Tunga` and `Nirmala UI` are Windows' built-in Kannada fonts, kept as a last-resort fallback.
- `font-display: swap` is already set in `fonts.css`.
- Set `lang="kn"` on Kannada content (or on `<html>` when the UI is in Kannada) so browsers pick the right shaping and line-breaking.

### Hierarchy

| Token | Size | Weight | Line Height | Use |
|---|---|---|---|---|
| `{typography.hero-display}` | 56px | 600 | 1.25 | Landing hero headline |
| `{typography.display-lg}` | 44px | 600 | 1.3 | Major section openers |
| `{typography.heading-1}` | 36px | 600 | 1.35 | Page titles |
| `{typography.heading-2}` | 30px | 600 | 1.4 | Section headings |
| `{typography.heading-3}` | 26px | 600 | 1.4 | Card titles, pond names |
| `{typography.heading-4}` | 22px | 600 | 1.45 | Feature tile titles |
| `{typography.heading-5}` | 20px | 600 | 1.5 | FAQ questions, small cards |
| `{typography.subtitle}` | 20px | 400 | 1.6 | Hero subtitle, lead paragraphs |
| `{typography.body-md}` | 18px | 400 | 1.7 | **Default body text** |
| `{typography.body-md-medium}` | 18px | 500 | 1.7 | Emphasised body, links |
| `{typography.body-sm}` | 16px | 400 | 1.7 | Secondary body, footer |
| `{typography.body-sm-medium}` | 16px | 500 | 1.7 | Tabs, filters |
| `{typography.caption}` | 15px | 400 | 1.6 | Helper text, timestamps (the smallest allowed size) |
| `{typography.caption-bold}` | 15px | 600 | 1.6 | Badges, tags |
| `{typography.button-md}` | 18px | 600 | 1.4 | Button labels |
| `{typography.status-label}` | 18px | 700 | 1.4 | Safe / Warning / Danger banners |
| `{typography.stat-display}` | 48px | 600 | 1.2 | Sensor readings (tabular numbers) |

### The scale used in the app
One scale, as CSS tokens in `styles.css` (`--fs-*`):

| Token | Size | Use |
|---|---|---|
| `--fs-title` | 28-32px | Page title (one per page) |
| `--fs-section` | 22px | Section heading (`h2`), left-aligned |
| `--fs-sub` | 18px, 600 | Sub-heading inside a section (`h3`), card titles in grids |
| `--fs-body` | 18px | Body text and important sentences |
| `--fs-small` | 16px | Helper text under headings, notes, quiet buttons |
| `--fs-caption` | 15px | Captions, tags, chips, **units** |

Readings use tabular numbers; their **units are smaller and muted** (`--fs-caption`, text-tertiary), so the number is what the eye reads first.

### Principles
- **Large by default.** Body text is 18px and nothing readable is under 15px. The UI must still work when the phone's text size is set to 200%, so size everything in `rem` and never fix heights on text containers.
- **Tall line heights for Kannada.** Kannada vowel signs (ಿ ೀ ು ೂ ೃ) and stacked conjuncts (ಒತ್ತಕ್ಷರ) extend well above and below the Latin x-height. Body uses 1.7, headings at least 1.25, and nothing goes below 1.2. Tighter leading clips or collides the marks.
- **No negative letter-spacing** on anything that can show Kannada: it breaks up Kannada conjunct clusters. Use `letter-spacing: 0`. The one exception is the big **AquaNexus** name on the start screen, which is always Latin letters (`lang="en"`).
- **No ALL-CAPS labels**, with one deliberate exception: the small "Team Orbit presents" line on the start screen (in Kannada it shows as written, without extra letter spacing). Kannada has no letter case, so use weight (600/700) for emphasis everywhere else.
- **Never use faux bold or italics on Kannada.** Load real 600/700 weights. For emphasis, use weight or color, not italics.
- **Tabular numbers for readings** (`font-variant-numeric: tabular-nums`) so live values don't jitter. Keep digits as Western Arabic numerals (0–9) in both languages unless users ask for Kannada numerals (೦–೯).

## Kannada & Bilingual Support

- **Allow for text expansion.** Kannada labels usually run 20–40% longer than English ones. Buttons, tabs and badges size to their content (`min-width`, never fixed `width`) and may wrap to two lines rather than truncate.
- **Don't truncate status or safety text** with ellipses. Wrap it instead.
- **Language toggle** (`language-toggle`): a two-segment pill labeled in each language's own script, **ಕನ್ನಡ | English**, never flags. Remember the choice between visits.
- **Line breaking:** Kannada breaks at spaces. Don't apply `word-break: break-all`, which splits syllables. Use `overflow-wrap: anywhere` only as a last resort inside narrow table cells.
- **Font check:** test with strings that stack deep, such as ಕ್ಷ್ಮ, ಸ್ತ್ರೀ, ಆಮ್ಲಜನಕ, ಮೀನುಗಳ ಆರೋಗ್ಯ, to confirm nothing is clipped at the top or bottom of buttons, inputs and table rows.
- **Units stay in Latin script** (°C, mg/L, pH, ppm) in both languages.

## Layout

### Spacing System
- **Base unit**: 4px (8px primary increment)
- **Tokens**: `{spacing.xxs}` (4px) · `{spacing.xs}` (8px) · `{spacing.sm}` (12px) · `{spacing.md}` (16px) · `{spacing.lg}` (20px) · `{spacing.xl}` (24px) · `{spacing.xxl}` (32px) · `{spacing.xxxl}` (40px) · `{spacing.section-sm}` (48px) · `{spacing.section}` (64px) · `{spacing.section-lg}` (96px) · `{spacing.hero}` (112px)
- **Section rhythm**: landing pages use `{spacing.section-lg}`; app dashboards tighten to `{spacing.xxl}` between cards.
- **Card internal padding**: `{spacing.xl}` (24px) for compact cards; `{spacing.xxl}` (32px) for feature panels.

### Grid & Container
- 1200px max-width with 24px gutters on computers; 16px minimum side padding on phones. Spacing between blocks is on an 8px grid (8, 16, 24, 32).
- **Pond page dashboard** (1024px and wider): two independent columns, 7 : 5. Left: the simulated clock line, the status block, the oxygen chart, time until danger. Right: the flat pond view, the Pond health panel, the latest readings. Phones: one column, left column first.
- My ponds: one `card-pond` per pond in a responsive grid (1-up phone → 2-up tablet → 3-up desktop).
- Reading lines stay under ~70 characters wide, and slightly narrower for Kannada.

## Elevation & Depth

The system is **flat**, like still water: every surface is a solid fill with a 1px `{colors.hairline}` border, and **no card has a shadow**. Cards are never nested inside cards; inside a card, parts are separated by thin dividers or small inner panels. Dialogs get a dark backdrop, not a shadow.

There is no 3D in the app and no drop shadow.
- **Start screen**: a quiet brand landing that **follows the theme**: light (its own palette in `welcome.css`: background #F4F7F6, text #0F2A33, muted #4D646B, accent #0B7A85, lines #DCE5E3), or black and white in the dark theme. Flat colours only: no gradients, light rays or fish. Top bar: the logo and "Team Orbit" on the left, the language switch on the right (white box, the chosen language dark with white text). Computers: two columns. Left: "Team Orbit presents" (small, uppercase, teal, a short teal rule before it; no capitals or letter spacing in Kannada), **AquaNexus** in Manrope 800 at about 96 px with tight letter spacing (allowed here only: the name is Latin letters, `lang="en"`), ಮೀನು ರಕ್ಷಕ in teal, the tagline in muted text, a dark Start button (12 px corners), and three short facts split by thin lines. Right: the **flat Team Orbit logo** (about 220 px) centred in two thin 1 px orbit paths, with a small teal dot on the outer one. Phones: stacked, the logo on top (about 120 px), full-width Start. **The only motion is the logo fading in once (0.6 s)**; nothing else on the start screen moves. Three.js is not loaded on the start screen (the 3D pond loads after Start). The sample Warning card sits below the first screen, smaller.

## Shapes

### Border Radius Scale

Three values only (`styles.css`):

| Token | Value | Use |
|---|---|---|
| `--radius-card` | 12px | **Every** card, panel, status banner, scene, dialog, **and every button** (also the page tabs on computers) |
| `--radius-inner` | 8px | Inputs, notes, checklist items, tags and other small parts inside a card (chips: 6px) |
| pill | 9999px | **Only** small chips and toggles: status badges, language / theme / pond toggles, SMS / WhatsApp switch |

## Components

> Hover states are not documented here. Only default, pressed, focus and disabled states are.

### Buttons

**`button-primary`**: the light pond-blue button used for the main action on a screen ("Check pond", "Save reading").
- Background `{colors.primary}`, text `{colors.on-primary}`, `{typography.button-md}`, padding `0 24px`, min-height 52px, 12px corners (`--radius-card`).
- Pressed state: `{colors.primary-pressed}`. Disabled: `{colors.hairline}` background with `{colors.muted}` text.

**`button-secondary-filled`**: bright cyan ({colors.secondary}) pill with dark text, for a secondary filled action.

**`button-secondary`**: a quiet outlined pill: 1px `{colors.hairline-strong}` border, `{colors.text}` text, no fill. **Each page has one primary action**; everything else is secondary or ghost (for example on Shop, "Add to cart" is secondary because there are five of them).

**`button-danger`**: red pill, used only for destructive or emergency actions ("Delete pond", "Call for help").

**`button-danger`** uses white ({colors.on-status}) text on `{colors.danger}`, never `{colors.on-primary}`, which is dark.

**`button-ghost`**: quiet rectangular button, min-height 48px.

**`button-link`**: underlined inline link in `{colors.primary}`.

**`button-icon-circular`**: 48×48px circular icon button. It always has an `aria-label` in the current language.

**Focus**: every interactive element shows a 3px `{colors.primary}` outline with a 2px offset on `:focus-visible`.

### Cards & Containers

**`card-base`**: `{colors.canvas}` card with a 16px radius and a hairline border.

All cards look the same: `{colors.canvas}`, hairline border, `--radius-card`. No "feature" variants with other fills or radii.

**`card-pond`**: the core dashboard card for one pond. It has a `{colors.canvas}` background, a hairline border, and a **6px left border in the pond's current status color**. It shows the pond name (`heading-3`), a status badge, 2–4 key readings in `stat-display`, and a "last updated" caption.

**`card-stat`**: a single large reading ("6.2 mg/L") in Manrope with tabular numbers; the unit is smaller and muted. On the Pond page the readings sit in **one** card as a two-column grid split by thin lines (no box per reading).

**Pond health panel**: the 0-100 score ring next to a slim risk scale (Danger 0-39 | Warning 40-74 | Safe 75-100) with a marker at the score, and the legend under it. Replaces the old separate gauge card.

**`card-highlighted`**: a pale water background with a 2px `{colors.primary}` border, for a recommended or featured item.

### Status

**`status-banner-safe` / `status-banner-warning` / `status-banner-danger`**: full-width banners at the top of a pond screen.
- **Safe** is calm: the card colour, a hairline and a 4px green left edge, the green icon and the word in the text colour.
- **Warning** and **Danger** keep their own light status background, a 2px border in the status colour and the matching dark text. **Danger is the only loud thing in the app** (the status strip turns solid red with a slow ring; destructive buttons such as "Delete all my data" are only outlined in red).
- **One status, said once:** the status strip (every page) and this block say the level. Other parts of the Pond page do not repeat "Safe": the Pond health panel shows the score on a Danger / Warning / Safe scale, the pond view has a plain caption, and readings get a badge only in Warning or Danger.
- Structure: **icon + status word + one-line reason + next step**. For example: (warning icon) **Warning**: Oxygen is low (4.1 mg/L). Run the aerator.
- Danger banners use `role="alert"`. Safe and Warning banners use `role="status"`.

**`badge-safe` / `badge-warning` / `badge-danger`**: solid pill badges with an icon and a word. The Warning badge uses dark text.

**`badge-tag`**: neutral category tag (cyan fill, dark text) such as fish species or pond type. Never used to show status.

**`sim-tag`** ("Simulated data" / "ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ"): a small **solid** cyan chip with dark text, 6px radius, no outline. Same words in both languages, on everything that shows simulated values. In the status strip it never wraps under the level word; long Kannada wraps inside the chip.

**Notes** (simulated-data banner, "Preview only", "Not for sale yet"): `{colors.surface}` with a hairline border and a pond-blue info icon, body-sm text. Calm: the words carry the message, not a loud fill.

**Data-source tags** ("AI assistant: can make mistakes", "Live sensor", "Manual test-kit reading"): quiet outlined tags in text-secondary, never styled like a button.

### Inputs & Forms

**`text-input`**: `{colors.canvas}` field with a `{colors.hairline-strong}` border (4.1:1), `{typography.body-md}`, min-height 52px, and the label always visible above it (not placeholder-only).

**`text-input-focused`**: 2px `{colors.primary}` border.

**`text-input-error`**: 2px `{colors.danger}` border plus an error message below in `{colors.danger-text}` with an icon.

**`search-pill`** and **`filter-dropdown`**: min-height 48px.

Numeric inputs for readings use `inputmode="decimal"` and show the unit as a suffix.

### Tabs & Toggles

**`pill-tab`** / **`pill-tab-active`**: inactive tabs have `{colors.text-secondary}` text on `{colors.canvas}`; the active tab is `{colors.primary}` with dark `{colors.on-primary}` text. Min-height 48px.

**`language-toggle`**: a segmented pill, **ಕನ್ನಡ | English**. The active segment is `{colors.primary}` with `{colors.on-primary}` text.

**Theme toggle**: the same segmented pill, **Light | Dark** (ತಿಳಿ | ಗಾಢ), each with a sun or moon icon *and* the word, never icon only. It sits next to the language toggle in the top bar and remembers the choice.

### Tables

**`data-table`** / **`data-row`**: reading history. `{typography.body-md}`, 16px × 20px cell padding, a status dot + word in the status column, and horizontal scroll on phones rather than squeezing columns.

### Navigation

**Top bar**: sticky `{colors.surface}` bar, ~64px tall (it grows if Kannada labels wrap), with the app name in text on the left and the language toggle plus a primary action on the right. Below 1024px it collapses to a menu button.

**Bottom navigation (mobile app screens)**: 3–5 items, each with an icon and a text label (never icon-only), and 56px-tall targets.

### Signature Components

**`hero-band`**: centered `hero-display` headline, subtitle, button row and a pond illustration below.

**`cta-banner`**: bright cyan banner (`{colors.secondary}`, dark text) with a `{rounded.feature}` radius, a centered headline and a `button-primary`.

**Team Orbit touches** (small, static details from the team's name; the pond stays the main identity):
- **Team Orbit logo** (`frontend/assets/team-orbit-logo.svg`, exactly as the team gave it): a thick ring, an orbit line crossing it (the ring is cut where the line passes), and a moon at the line's upper-right end. One colour (`currentColor`): **#0B7A85 on light backgrounds, white in the dark theme** (`--logo` in `styles.css`). It is inlined on the start screen (top bar and the big logo), in the app header and in the footer credit; **each inline copy has its own mask id** (`to-cut-welcome-bar`, `to-cut-welcome-logo`, `to-cut-header`, `to-cut-footer`). The favicon is `team-orbit-favicon.svg`: the same logo with the two colours built in, because a browser tab has no text colour to inherit. The start screen shows "Team Orbit presents" / "ಟೀಮ್ ಆರ್ಬಿಟ್ ಪ್ರಸ್ತುತಪಡಿಸುತ್ತದೆ"; the footer says "AquaNexus by Team Orbit (Nexus Orbit)" / "AquaNexus · ನಿರ್ಮಾಣ: ಟೀಮ್ ಆರ್ಬಿಟ್ (Nexus Orbit)".
- **App name:** **AquaNexus**, written in Latin letters in both languages. On the welcome screen the Kannada tagline **ಮೀನು ರಕ್ಷಕ** ("fish protector") sits under the name, in `{colors.primary}`.
- None of them use status colours or the magenta accent.

**`footer-region`** / **`footer-link`**: deep-water footer (`{colors.footer-bg}`) with `{colors.text-secondary}` links at 16px.

## Do's and Don'ts

### Do
- Use `{colors.primary}` light pond blue for the one main action on each screen
- Keep green, amber and red strictly for Safe / Warning / Danger, always with an icon and a word
- Put dark text ({colors.on-warning}) on amber
- Keep body text at 18px and use nothing readable below 15px
- Test every screen in Kannada, with long labels and deep conjuncts
- Use 12px corners on buttons and cards; pills only for chips and toggles
- Keep touch targets at 48px or larger

### Don't
- Don't use the magenta accent ({colors.accent}) anywhere on screen
- Don't add decorative blobs, waves, gradient washes, glows, rings, bubbles or doodles (the pond pictures are the only illustrations)
- Don't use emoji, in the UI or in SMS / WhatsApp text: use the outline icons and words ("AquaNexus DANGER - Pond 1: ...")
- Don't animate for decoration: no scroll reveals, word-by-word headings, cursor ripples, magnetic buttons, card tilt (except the start card) or orbiting dots
- Don't use green, amber or red decoratively, in either theme (pictures, waves, glows and doodles included)
- Don't draw decoration: no drawn phone frames, loading mascots, night-scene illustrations or a badge on every list item. One clear heading per card, short helper text under it
- Don't put an amber stripe on a light card without its dark edge ({colors.light-warning-edge})
- Don't use status colors for decoration, branding or category tags
- Don't use secondary ({colors.secondary}) as text or as a border; it is a fill with dark text (only 2.0:1 on the light page), and it is close to primary, so never the only difference from it
- Don't put status text colors (e.g. {colors.danger-text}) directly on the dark page; only on their own light status background
- Don't use {colors.on-primary} for text on status colors; use {colors.on-status} (or {colors.on-warning} on amber)
- Don't rely on color alone to show status
- Don't use negative letter-spacing, ALL-CAPS labels or line heights below 1.2
- Don't give buttons or tabs fixed widths, which clip Kannada labels
- Don't use `{colors.muted}` for any text people need to read
- Don't put shadows on cards or buttons. Keep the look flat and calm.

## Responsive Behavior

### Breakpoints
| Name | Width | Key Changes |
|---|---|---|
| Mobile (small) | < 480px | Single column. Hero 32px. Bottom nav. Pond cards 1-up. |
| Mobile (large) | 480 – 767px | Hero 36px. Stat cards 2-up. |
| Tablet | 768 – 1023px | Pond cards 2-up. Pill tabs visible. |
| Desktop | 1024 – 1279px | Pond cards 3-up. Top nav expanded. Hero 48px. |
| Wide Desktop | ≥ 1280px | Full 56px hero. |

### Touch Targets
- Buttons: 52px tall. Icon buttons, tabs, filters and toggles: at least 48×48px.
- Keep at least 8px between adjacent targets.

### Collapsing Strategy
- **Top nav**: collapses to a menu button below 1024px. The language toggle stays visible at all widths.
- **Hero typography**: 56px → 48px → 36px → 32px.
- **Data tables**: horizontal scroll on phones, with the first column (date/time) kept visible.
- **Footer**: multi-column → 2-column → accordion on small phones.

## Iteration Guide

1. Focus on ONE component at a time
2. Reference component names and tokens directly
3. Run `npx @google/design.md lint DESIGN.md` after edits
4. Add new variants as separate `components:` entries
5. Default to `{typography.body-md}` (18px) for body text
6. Any new color must come from the brand palette (or be derived from it), must pass 4.5:1 for text (3:1 for borders and icons) in **both** themes, and must not look like a status color. Add it to both theme blocks in `styles.css` and run `python -m pytest tests/test_contrast.py`
7. Use 12px corners (`--radius-card`) on buttons; pills only for chips and toggles
8. Check every new component in both Kannada and English before calling it done

## Known Gaps

- In the light theme the gauge arc and health ring use plain amber for Warning (2.0:1 on cards); the word and icon beside them carry the meaning
- For tritanopia the magenta accent is only 12 apart from Danger red (15 wanted). It does not matter today because the accent is not used on screen; a slightly bluer magenta such as `#900caf` would reach 16 if it is ever used
- Animation timings: 150-200ms ease for small changes; every animation stops with `prefers-reduced-motion`. Kept on purpose: level change (status colours fade), numbers counting to a new reading, the countdown, the Danger banner and strip's slow ring, the loading fish
- Exact Safe/Warning/Danger thresholds (oxygen, pH, temperature, ammonia) belong in the app's domain logic, not in this file
- Charts for reading history need their own palette spec; reuse the status colors only for threshold bands
