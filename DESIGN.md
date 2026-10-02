---
version: alpha
name: pond-design-system
description: A calm, deep-water design system for a pond and fish-health app, in two themes from one Realtime Colors palette. Dark (default) puts light pond blue ({colors.primary}) on deep indigo ({colors.background}); light, for bright outdoor sunlight, puts a deepened pond blue ({colors.light-primary}) on pale indigo-white ({colors.light-background}) with the indigo as text. Bright cyan ({colors.secondary}) fills banners, tags and highlights with dark text, and magenta ({colors.accent}) is decoration only. A strict three-level status palette (Safe green, Warning amber, Danger red) is reserved for pond and fish condition readings only, identical in both themes. Type is set large for readability outdoors and on low-end phones, and every text style is tuned to render Kannada (ಕನ್ನಡ) script as comfortably as English.

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
  accent: "#a10c9f"          # magenta: DECORATION ONLY (see Colors)
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
  light-accent: "#a10c9f"    # same magenta, decoration only
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

- **Dark (default):** deep indigo ({colors.background}) with light, cool text ({colors.text}). The main action is a light pond-blue pill ({colors.primary}) with dark text.
- **Light, for bright outdoor sunlight:** pale indigo-white ({colors.light-background}) with the palette's indigo as text ({colors.light-text}). The main action is a deepened pond-blue pill ({colors.light-primary}) with light text.

Bright cyan ({colors.secondary}) fills banners, tags and highlighted items, always with dark text. Magenta ({colors.accent}) is the accent, and it is **decoration only**: doodles, glows and lines in the pictures, never text, never a control, never next to a status. The first theme follows the phone's light/dark setting; a **Light | Dark** toggle in the top bar overrides it and is remembered. The pictures (welcome pond, sky scene, pond view) show night water and stay dark in both themes.

The most important job of the interface is to make pond condition clear at a glance. Green, amber and red mean only one thing each: **Safe**, **Warning** and **Danger**. These colors never appear as decoration, and each status always comes with an icon and a word, never color alone. Status colours are identical in both themes. On the dark page, status banners keep their light backgrounds, so alerts are the brightest thing on screen; on the light page their 2px solid status border sets them apart.

Text is set larger than a typical web app: body text is 18px, and nothing that must be read is smaller than 15px. Every style is tuned so Kannada (ಕನ್ನಡ) renders as comfortably as English, with generous line height and no negative letter-spacing.

**Key Characteristics:**
- Deep indigo (dark) or pale indigo-white (light) with pond-blue pill CTAs ({colors.primary} + `{rounded.full}`)
- Bright cyan ({colors.secondary}) for banners, tags and highlighted items, always with dark text
- Magenta ({colors.accent}) for decoration only
- A strict Safe/Warning/Danger palette used only for condition status, always paired with an icon and a label
- Large, readable type: 18px body, 52px-tall buttons, 48px minimum touch targets
- Noto Sans + Noto Sans Kannada on every surface, with line heights tall enough for Kannada vowel signs and conjuncts
- Darkest-water footer ({colors.footer-bg})

## Colors

All contrast ratios below are measured (WCAG 2.x formula). Text needs at least 4.5:1; borders, stripes and icons need at least 3:1.

### Brand palette: dark theme (default)
| Token | Hex | Use | Contrast |
|---|---|---|---|
| **Background** ({colors.background}) | `#060351` | Page background (deep indigo) | text on it 15.7:1 |
| **Text** ({colors.text}) | `#def0f8` | Headlines and body text | 15.9:1 on cards |
| **Primary** ({colors.primary}) | `#88cce6` | Primary buttons, active tabs, links, focus rings, highlighted-card borders | 10.4:1 on background; dark text on it 10.4:1 |
| **Primary Pressed** ({colors.primary-pressed}) | `#a8daee` | Pressed state of primary buttons | dark text on it 12.2:1 |
| **On Primary** ({colors.on-primary}) | `#060351` | Text on primary | |
| **Secondary** ({colors.secondary}) | `#23bcd0` | **Fill**: simulated-data banner, tags, selected pond, WhatsApp bubble, CTA banners | dark text on it 8.1:1 |
| **Edge on Secondary** ({colors.edge-on-secondary}) | `#060351` | Dashed borders and the border trail on secondary fills | 8.1:1 on secondary |
| **Accent** ({colors.accent}) | `#a10c9f` | **Decoration only** (see below) | **2.7:1 on the background: never text, never a control** |

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
| **Accent** ({colors.light-accent}) | `#a10c9f` | Decoration only, as in dark | 5.9:1 on the background |
| **Surface / Canvas** | `#f6f7fd` / `#fcfcff` | Top bar and sections / cards and inputs | |
| **Text Secondary / Tertiary** | `#2c2f6b` / `#4a4e85` | Secondary / tertiary text | 11.9:1 / 7.5:1 on cards |
| **Hairline / Hairline Strong** | `#d3d6ee` / `#646a99` | Dividers / control borders | strong 5.0:1 on cards |
| **Footer** ({colors.light-footer-bg}) | `#dfe2f5` | Bottom toolbar | |

Tokens with no light value (status colours, the font) are shared by both themes.

**How to use the accent (magenta):** purple and magenta are allowed again, but the accent is **decoration only**: hand-drawn doodles, page and card glows, the cursor spotlight, and highlight lines in the pictures (the welcome pond, the sky scene). It is never text (2.7:1 on the dark page), never a fill behind text, never a stripe, badge, border or icon that carries meaning, never on anything clickable, and never right next to a status. `tests/test_contrast.py` enforces that only `.doodle` and `.sc-accent` use it.

**Accent vs status colours, including colour blindness** (OKLab difference x100, 15+ = clearly different; colour blindness simulated with Machado et al. 2009):

| | Normal vision | Protanopia | Deuteranopia | Tritanopia |
|---|---|---|---|---|
| vs **Danger** red | 21 | 21 | 21 | **12** |
| vs Warning amber | 41 | 42 | 39 | 28 |
| vs Safe green | 36 | 26 | 17 | 26 |

For the common red-green colour blindness (protanopia, deuteranopia) the magenta stays clearly different from Danger red. For **tritanopia** (blue-yellow, about 1 in 10 000 people) it becomes a dark rose only 12 apart from red: that is the reason the accent stays decoration only, away from every status (see Known Gaps).

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
- `styles.css` defines the dark tokens on `:root, .dark-scope` and the light overrides on `:root[data-theme="light"]`. A small script in `index.html` sets `data-theme` before the first paint: the saved choice (`localStorage` key `meenuraksha-theme`), else `prefers-color-scheme`.
- **Pictures stay dark:** the welcome pond, the sky scene and the pond view carry the `dark-scope` class, so they keep dark tokens on the light page.
- **Background waves:** `tools/recolor_backgrounds.py` writes `*-brand.svg` (dark, 16% opacity) and `*-light.svg` (light, 10% opacity) from the theme tokens. Re-run it after changing primary, secondary or background.
- **The sky scene** uses its own indigo, blues, cyan, an orchid dusk and pale pearl (`SKY` in `scene.js`); sunrise and sunset are light and position, never orange, red or green.
- `tests/test_contrast.py` checks every pair in both themes, the waves, the sky and the card gradients.

## Typography

### Font Family
**Noto Sans** (Latin) + **Noto Sans Kannada** (Kannada), both under the SIL Open Font License. The two are designed to match, so mixed Kannada and English lines (for example, "ಆಮ್ಲಜನಕ 6.2 mg/L") share the same weight and baseline.

**The fonts are bundled locally so the app works offline.** Never load them from Google Fonts or any other CDN. They live in `frontend/fonts/`, and every page links the local stylesheet:

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

### Principles
- **Large by default.** Body text is 18px and nothing readable is under 15px. The UI must still work when the phone's text size is set to 200%, so size everything in `rem` and never fix heights on text containers.
- **Tall line heights for Kannada.** Kannada vowel signs (ಿ ೀ ು ೂ ೃ) and stacked conjuncts (ಒತ್ತಕ್ಷರ) extend well above and below the Latin x-height. Body uses 1.7, headings at least 1.25, and nothing goes below 1.2. Tighter leading clips or collides the marks.
- **No negative letter-spacing, anywhere.** It breaks up Kannada conjunct clusters. Use `letter-spacing: 0` for all scripts.
- **No ALL-CAPS labels.** Kannada has no letter case, so uppercase styling creates an inconsistent look between languages. Use weight (600/700) for emphasis instead.
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
- 1200px max-width with 24–32px gutters; 16px minimum side padding on phones.
- Dashboard: one `card-pond` per pond in a responsive grid (1-up phone → 2-up tablet → 3-up desktop).
- Reading lines stay under ~70 characters wide, and slightly narrower for Kannada.

## Elevation & Depth

The system is mostly flat, like still water. Depth is used sparingly.

| Level | Treatment | Use |
|---|---|---|
| 0 (flat) | No shadow; `{colors.hairline}` border | Default cards, table rows, inputs |
| 1 (subtle) | `rgba(10, 31, 41, 0.05) 0px 1px 2px 0px` | Tappable cards |
| 2 (card) | `rgba(10, 31, 41, 0.08) 0px 4px 12px 0px` | Feature cards |
| 3 (overlay) | `rgba(10, 31, 41, 0.14) 0px 16px 48px -8px` | Modals, dropdowns, alert sheets |

## Shapes

### Border Radius Scale

| Token | Value | Use |
|---|---|---|
| `{rounded.xs}` | 4px | Small chips |
| `{rounded.sm}` | 6px | Compact badges |
| `{rounded.md}` | 8px | Inputs, search field, tables |
| `{rounded.lg}` | 12px | Status banners |
| `{rounded.xl}` | 16px | Standard and pond cards |
| `{rounded.xxl}` | 20px | Larger cards |
| `{rounded.xxxl}` | 28px | Feature cards |
| `{rounded.feature}` | 32px | Dark CTA banner |
| `{rounded.full}` | 9999px | All buttons, pill tabs, badges |

## Components

> Hover states are not documented here. Only default, pressed, focus and disabled states are.

### Buttons

**`button-primary`**: the light pond-blue pill used for the main action on a screen ("Check pond", "Save reading").
- Background `{colors.primary}`, text `{colors.on-primary}`, `{typography.button-md}`, padding `14px 28px`, min-height 52px, `{rounded.full}`.
- Pressed state: `{colors.primary-pressed}`. Disabled: `{colors.hairline}` background with `{colors.muted}` text.

**`button-secondary-filled`**: bright cyan ({colors.secondary}) pill with dark text, for a secondary filled action.

**`button-secondary`**: an outlined pill with a 2px `{colors.primary}` border and `{colors.primary}` text.

**`button-danger`**: red pill, used only for destructive or emergency actions ("Delete pond", "Call for help").

**`button-danger`** uses white ({colors.on-status}) text on `{colors.danger}`, never `{colors.on-primary}`, which is dark.

**`button-ghost`**: quiet rectangular button, min-height 48px.

**`button-link`**: underlined inline link in `{colors.primary}`.

**`button-icon-circular`**: 48×48px circular icon button. It always has an `aria-label` in the current language.

**Focus**: every interactive element shows a 3px `{colors.primary}` outline with a 2px offset on `:focus-visible`.

### Cards & Containers

**`card-base`**: `{colors.canvas}` card with a 16px radius and a hairline border.

**`card-feature`** and the variants **`card-feature-secondary`** (cyan fill, dark text) and **`card-feature-deep`** (`{colors.surface}` with a hairline border): 28px radius, 32px padding. These are decorative, so a feature card never means a status.

**`card-pond`**: the core dashboard card for one pond. It has a `{colors.canvas}` background, a hairline border, and a **6px left border in the pond's current status color**. It shows the pond name (`heading-3`), a status badge, 2–4 key readings in `stat-display`, and a "last updated" caption.

**`card-stat`**: a single large reading ("6.2 mg/L") in `stat-display`, with its label and unit beneath in `body-sm`.

**`card-highlighted`**: a pale water background with a 2px `{colors.primary}` border, for a recommended or featured item.

### Status

**`status-banner-safe` / `status-banner-warning` / `status-banner-danger`**: full-width banners at the top of a pond screen.
- The status's own light background, 2px solid border in the status color, `{typography.status-label}` text in the matching dark text color, and a 24px leading icon. On the dark page these are the brightest elements on screen.
- Structure: **icon + status word + one-line reason + next step**. For example: ⚠ **Warning**: Oxygen is low (4.1 mg/L). Run the aerator.
- Danger banners use `role="alert"`. Safe and Warning banners use `role="status"`.

**`badge-safe` / `badge-warning` / `badge-danger`**: solid pill badges with an icon and a word. The Warning badge uses dark text.

**`badge-tag`**: neutral category tag (cyan fill, dark text) such as fish species or pond type. Never used to show status.

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

**`footer-region`** / **`footer-link`**: deep-water footer (`{colors.footer-bg}`) with `{colors.text-secondary}` links at 16px.

## Do's and Don'ts

### Do
- Use `{colors.primary}` light pond blue for the one main action on each screen
- Keep green, amber and red strictly for Safe / Warning / Danger, always with an icon and a word
- Put dark text ({colors.on-warning}) on amber
- Keep body text at 18px and use nothing readable below 15px
- Test every screen in Kannada, with long labels and deep conjuncts
- Use `{rounded.full}` on every button, tab and badge
- Keep touch targets at 48px or larger

### Don't
- Don't use the magenta accent ({colors.accent}) for anything but decoration: no text, fills behind text, stripes, badges, icons that carry meaning, or controls, and never next to a status
- Don't use green, amber or red decoratively, in either theme (sky, waves, glows and doodles included)
- Don't put an amber stripe on a light card without its dark edge ({colors.light-warning-edge})
- Don't use status colors for decoration, branding or category tags
- Don't use secondary ({colors.secondary}) as text or as a border; it is a fill with dark text (only 2.0:1 on the light page), and it is close to primary, so never the only difference from it
- Don't put status text colors (e.g. {colors.danger-text}) directly on the dark page; only on their own light status background
- Don't use {colors.on-primary} for text on status colors; use {colors.on-status} (or {colors.on-warning} on amber)
- Don't rely on color alone to show status
- Don't use negative letter-spacing, ALL-CAPS labels or line heights below 1.2
- Don't give buttons or tabs fixed widths, which clip Kannada labels
- Don't use `{colors.muted}` for any text people need to read
- Don't use heavy shadows. Keep the look flat and calm.

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
7. Use pill-shaped buttons (`{rounded.full}`) everywhere
8. Check every new component in both Kannada and English before calling it done

## Known Gaps

- In the light theme the gauge arc and health ring use plain amber for Warning (2.0:1 on cards); the word and icon beside them carry the meaning
- For tritanopia the magenta accent is only 12 apart from Danger red (15 wanted). It is kept because the accent is decoration only; a slightly bluer magenta such as `#900caf` would reach 16 if this ever needs closing
- Animation timings are not set; use 150–200ms ease and respect `prefers-reduced-motion`
- Exact Safe/Warning/Danger thresholds (oxygen, pH, temperature, ammonia) belong in the app's domain logic, not in this file
- Charts for reading history need their own palette spec; reuse the status colors only for threshold bands
