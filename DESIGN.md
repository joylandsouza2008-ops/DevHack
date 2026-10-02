---
version: alpha
name: pond-design-system
description: A calm, deep-water design system for a pond and fish-health app, in a dark theme. Light pond blue ({colors.primary}) marks every primary action on a near-black water background ({colors.background}), deep indigo-blue ({colors.secondary}) fills banners and highlighted cards, and a strict three-level status palette (Safe green, Warning amber, Danger red) is reserved for pond and fish condition readings only. Type is set large for readability outdoors and on low-end phones, and every text style is tuned to render Kannada (ಕನ್ನಡ) script as comfortably as English.

colors:
  # Brand palette (Realtime Colors)
  background: "#06131a"
  text: "#def0f8"
  primary: "#88cce6"
  primary-pressed: "#a8daee"
  on-primary: "#06131a"
  secondary: "#1f2f91"
  on-secondary: "#def0f8"
  accent: "#22d3ee"          # aqua: decorative highlights only (see Colors)
  on-accent: "#06131a"       # light text on aqua fails (1.5:1)
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
  surface: "#081820"         # top bar, sections
  canvas: "#0a1b23"          # cards, inputs
  hairline: "#1e3742"
  hairline-soft: "#152c36"
  hairline-strong: "#5a7f8f"  # input and control borders (4.1:1 on canvas)
  text-secondary: "#a9c6d3"
  text-tertiary: "#86a7b5"
  muted: "#5f7c89"           # disabled only
  footer-bg: "#030b10"

typography:
  hero-display:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 56px
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: 0
  display-lg:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 44px
    fontWeight: 600
    lineHeight: 1.3
  heading-1:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 36px
    fontWeight: 600
    lineHeight: 1.35
  heading-2:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 30px
    fontWeight: 600
    lineHeight: 1.4
  heading-3:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 26px
    fontWeight: 600
    lineHeight: 1.4
  heading-4:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 22px
    fontWeight: 600
    lineHeight: 1.45
  heading-5:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.5
  subtitle:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.7
  body-md-medium:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.7
  body-sm:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.7
  body-sm-medium:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.7
  caption:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.6
  caption-bold:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1.6
  button-md:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.4
  status-label:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 18px
    fontWeight: 700
    lineHeight: 1.4
  stat-display:
    fontFamily: Noto Sans, Noto Sans Kannada
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.2
    fontVariantNumeric: tabular-nums

rounded:
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
  xxl: 20px
  xxxl: 28px
  feature: 32px
  full: 9999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 20px
  xl: 24px
  xxl: 32px
  xxxl: 40px
  section-sm: 48px
  section: 64px
  section-lg: 96px
  hero: 112px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "14px 28px"
    minHeight: 52px
  button-primary-pressed:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
  button-primary-disabled:
    backgroundColor: "{colors.hairline}"
    textColor: "{colors.muted}"
  button-secondary-filled:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "14px 28px"
    minHeight: 52px
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "14px 28px"
    minHeight: 52px
    border: "2px solid {colors.primary}"
  button-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-status}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "14px 28px"
    minHeight: 52px
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: "10px 14px"
    minHeight: 48px
  button-link:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.body-md-medium}"
    padding: "0"
    textDecoration: underline
  button-icon-circular:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.text}"
    rounded: "{rounded.full}"
    size: 48px
    border: "1px solid {colors.hairline-strong}"
  card-base:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
    border: "1px solid {colors.hairline}"
  card-feature:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
    border: "1px solid {colors.hairline}"
  card-feature-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
  card-feature-deep:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
    border: "1px solid {colors.hairline}"
  card-pond:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
    border: "1px solid {colors.hairline}"
    borderLeft: "6px solid {status color}"
  card-stat:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    typography: "{typography.stat-display}"
    padding: "{spacing.lg}"
  card-highlighted:
    backgroundColor: "{colors.secondary}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xxl}"
    border: "2px solid {colors.primary}"
  status-banner-safe:
    backgroundColor: "{colors.safe-bg}"
    textColor: "{colors.safe-text}"
    typography: "{typography.status-label}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md} {spacing.lg}"
    border: "2px solid {colors.safe}"
    icon: check-circle
  status-banner-warning:
    backgroundColor: "{colors.warning-bg}"
    textColor: "{colors.warning-text}"
    typography: "{typography.status-label}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md} {spacing.lg}"
    border: "2px solid {colors.warning}"
    icon: alert-triangle
  status-banner-danger:
    backgroundColor: "{colors.danger-bg}"
    textColor: "{colors.danger-text}"
    typography: "{typography.status-label}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md} {spacing.lg}"
    border: "2px solid {colors.danger}"
    icon: alert-octagon
  badge-safe:
    backgroundColor: "{colors.safe}"
    textColor: "{colors.on-status}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "6px 14px"
  badge-warning:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.on-warning}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "6px 14px"
  badge-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-status}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "6px 14px"
  badge-tag:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "6px 14px"
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.text}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
    border: "1px solid {colors.hairline-strong}"
    minHeight: 52px
  text-input-focused:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.text}"
    border: "2px solid {colors.primary}"
  text-input-error:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.text}"
    border: "2px solid {colors.danger}"
  search-pill:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-tertiary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.xs} {spacing.md}"
    minHeight: 48px
    border: "1px solid {colors.hairline}"
  filter-dropdown:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.text}"
    typography: "{typography.body-sm-medium}"
    rounded: "{rounded.full}"
    padding: "{spacing.xs} {spacing.md}"
    minHeight: 48px
    border: "1px solid {colors.hairline-strong}"
  pill-tab:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.text-secondary}"
    typography: "{typography.body-sm-medium}"
    rounded: "{rounded.full}"
    padding: "{spacing.xs} {spacing.lg}"
    minHeight: 48px
    border: "1px solid {colors.hairline}"
  pill-tab-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.full}"
    border: "1px solid {colors.primary}"
  language-toggle:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    typography: "{typography.body-sm-medium}"
    rounded: "{rounded.full}"
    padding: "4px"
    minHeight: 48px
  data-table:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.text}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    border: "1px solid {colors.hairline}"
  data-row:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.text}"
    padding: "{spacing.md} {spacing.lg}"
    border: "0 0 1px {colors.hairline-soft} solid"
  faq-accordion-item:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.md}"
    padding: "{spacing.xl}"
    border: "0 0 1px {colors.hairline} solid"
  hero-band:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text}"
    typography: "{typography.hero-display}"
    rounded: "0"
    padding: "{spacing.hero}"
  cta-banner:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    rounded: "{rounded.feature}"
    padding: "{spacing.section}"
  footer-region:
    backgroundColor: "{colors.footer-bg}"
    textColor: "{colors.text}"
    typography: "{typography.body-sm}"
    padding: "{spacing.section} {spacing.xxl}"
  footer-link:
    backgroundColor: "transparent"
    textColor: "{colors.text-secondary}"
    typography: "{typography.body-sm}"
    padding: "{spacing.xs} 0"
---

## Overview

This is a calm, deep-water design system for a pond and fish-health app. It is used by pond owners and fish farmers, often outdoors, on phones, and in either Kannada or English. It uses a **dark theme**: every screen sits on near-black water ({colors.background}) with light, cool text ({colors.text}). The main action is always a light pond-blue pill button ({colors.primary}) with dark text. Deep indigo-blue ({colors.secondary}) fills banners, tags and highlighted cards. The palette comes from Realtime Colors; there is no purple or lavender anywhere in the system.

The most important job of the interface is to make pond condition clear at a glance. Green, amber and red mean only one thing each: **Safe**, **Warning** and **Danger**. These colors never appear as decoration, and each status always comes with an icon and a word, never color alone. On the dark page, status banners keep their light backgrounds, so alerts are the brightest thing on screen.

Text is set larger than a typical web app: body text is 18px, and nothing that must be read is smaller than 15px. Every style is tuned so Kannada (ಕನ್ನಡ) renders as comfortably as English, with generous line height and no negative letter-spacing.

**Key Characteristics:**
- Near-black water background with light pond-blue pill CTAs ({colors.primary} + `{rounded.full}`)
- Deep indigo-blue ({colors.secondary}) for banners, tags and highlighted cards, always with light text
- A strict Safe/Warning/Danger palette used only for condition status, always paired with an icon and a label
- Large, readable type: 18px body, 52px-tall buttons, 48px minimum touch targets
- Noto Sans + Noto Sans Kannada on every surface, with line heights tall enough for Kannada vowel signs and conjuncts
- Darkest-water footer ({colors.footer-bg})

## Colors

All contrast ratios below are measured (WCAG 2.x formula). Text needs at least 4.5:1; borders, stripes and icons need at least 3:1.

### Brand palette
| Token | Hex | Use | Contrast |
|---|---|---|---|
| **Background** ({colors.background}) | `#06131a` | Page background | text on it 16.1:1 |
| **Text** ({colors.text}) | `#def0f8` | Headlines and body text | 15.0:1 on cards |
| **Primary** ({colors.primary}) | `#88cce6` | Primary buttons, active tabs, links, focus rings, highlighted-card borders | 10.6:1 on background; dark text on it 10.6:1 |
| **Primary Pressed** ({colors.primary-pressed}) | `#a8daee` | Pressed state of primary buttons | dark text on it 12.5:1 |
| **On Primary** ({colors.on-primary}) | `#06131a` | Text on primary | |
| **Secondary** ({colors.secondary}) | `#1f2f91` | **Fill only**: simulated-data banner, tags, highlighted cards, CTA banners | text on it 9.6:1; **1.7:1 on the background, so never as text or a border** |
| **Accent** ({colors.accent}) | `#22d3ee` | Decorative highlights only (see below) | 10.4:1 on the background, 9.7:1 on cards; dark ({colors.on-accent}) text on it 10.4:1; **light text on it 1.5:1, never** |

**How to use the accent (aqua):** it is clearly different from all three status colors (OKLab difference 31 from Safe, 28 from Warning, 42 from Danger; 15+ is clearly different), and it is not orange, so it can't be mistaken for amber Warning. But it is **almost the same color as primary** (difference 6.2, and 1.2 for color-blind viewers), so the two can't be told apart by color. Use aqua only for decorative highlights (water shimmer, an icon accent, a highlight line in an illustration). Never use it to mean something different from primary, never as the only difference between two states, and never on anything clickable: clickable things are always {colors.primary}. Text on an aqua fill is always dark ({colors.on-accent}).

### Status (Safe / Warning / Danger), unchanged
These colors are reserved for pond and fish condition: water quality, oxygen, temperature, pH, ammonia and alerts.

| Level | Solid | Background | Text on background | Icon | Contrast |
|---|---|---|---|---|---|
| **Safe** | {colors.safe} `#1a7f37` | {colors.safe-bg} | {colors.safe-text} | check-circle | white ({colors.on-status}) on solid 5.1:1 · text on bg 8.8:1 · solid vs page 3.7:1 |
| **Warning** | {colors.warning} `#f5a524` | {colors.warning-bg} | {colors.warning-text} | alert-triangle | dark ({colors.on-warning}) on solid 9.1:1 · text on bg 7.4:1 · solid vs page 9.2:1 |
| **Danger** | {colors.danger} `#c62828` | {colors.danger-bg} | {colors.danger-text} | alert-octagon | white ({colors.on-status}) on solid 5.6:1 · text on bg 9.1:1 · solid vs page 3.4:1 |

- Status colors are always used as these fixed pairs. **Status text colors only ever sit on their own light status background**: Danger text directly on the dark page is 1.8:1 and unreadable.
- On cards ({colors.canvas}) the solid colors still pass 3:1 as left-border stripes (Safe 3.5, Warning 8.6, Danger 3.1).
- Text on the amber Warning solid is always dark ({colors.on-warning}). White text on amber fails contrast.
- Red and green look alike to color-blind users. The **icon shape and the word** (Safe / ಸುರಕ್ಷಿತ, Warning / ಎಚ್ಚರಿಕೆ, Danger / ಅಪಾಯ) are what carry the meaning; color only reinforces it.

### Surface
- **Background** ({colors.background}): Page background.
- **Surface** ({colors.surface}): Top bar and section backgrounds.
- **Canvas** ({colors.canvas}): Cards and inputs.
- **Hairline** ({colors.hairline}) / **Hairline Soft** ({colors.hairline-soft}): Decorative 1px borders and dividers.
- **Hairline Strong** ({colors.hairline-strong}): Input and control borders (4.1:1 on cards, 4.4:1 on the background).
- **Footer** ({colors.footer-bg}): Darkest water, for the footer.

### Text
- **Text** ({colors.text}): Headlines and body text (15.0:1 on cards).
- **Text Secondary** ({colors.text-secondary}): Secondary text and metadata (9.8:1 on cards).
- **Text Tertiary** ({colors.text-tertiary}): Tertiary text and placeholders (6.9:1 on cards). This is the dimmest color allowed for readable text.
- **Muted** ({colors.muted}): Disabled labels only (4.0:1). Never use it for text people need to read.
- **On Secondary** ({colors.on-secondary}): Text on secondary fills (9.6:1).

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

**`button-secondary-filled`**: deep indigo-blue ({colors.secondary}) pill with light text, for a secondary filled action.

**`button-secondary`**: an outlined pill with a 2px `{colors.primary}` border and `{colors.primary}` text.

**`button-danger`**: red pill, used only for destructive or emergency actions ("Delete pond", "Call for help").

**`button-danger`** uses white ({colors.on-status}) text on `{colors.danger}`, never `{colors.on-primary}`, which is dark.

**`button-ghost`**: quiet rectangular button, min-height 48px.

**`button-link`**: underlined inline link in `{colors.primary}`.

**`button-icon-circular`**: 48×48px circular icon button. It always has an `aria-label` in the current language.

**Focus**: every interactive element shows a 3px `{colors.primary}` outline with a 2px offset on `:focus-visible`.

### Cards & Containers

**`card-base`**: `{colors.canvas}` card with a 16px radius and a hairline border.

**`card-feature`** and the variants **`card-feature-secondary`** (indigo-blue fill, light text) and **`card-feature-deep`** (`{colors.surface}` with a hairline border): 28px radius, 32px padding. These are decorative, so a feature card never means a status.

**`card-pond`**: the core dashboard card for one pond. It has a `{colors.canvas}` background, a hairline border, and a **6px left border in the pond's current status color**. It shows the pond name (`heading-3`), a status badge, 2–4 key readings in `stat-display`, and a "last updated" caption.

**`card-stat`**: a single large reading ("6.2 mg/L") in `stat-display`, with its label and unit beneath in `body-sm`.

**`card-highlighted`**: a pale water background with a 2px `{colors.primary}` border, for a recommended or featured item.

### Status

**`status-banner-safe` / `status-banner-warning` / `status-banner-danger`**: full-width banners at the top of a pond screen.
- The status's own light background, 2px solid border in the status color, `{typography.status-label}` text in the matching dark text color, and a 24px leading icon. On the dark page these are the brightest elements on screen.
- Structure: **icon + status word + one-line reason + next step**. For example: ⚠ **Warning**: Oxygen is low (4.1 mg/L). Run the aerator.
- Danger banners use `role="alert"`. Safe and Warning banners use `role="status"`.

**`badge-safe` / `badge-warning` / `badge-danger`**: solid pill badges with an icon and a word. The Warning badge uses dark text.

**`badge-tag`**: neutral category tag (indigo-blue fill, light text) such as fish species or pond type. Never used to show status.

### Inputs & Forms

**`text-input`**: `{colors.canvas}` field with a `{colors.hairline-strong}` border (4.1:1), `{typography.body-md}`, min-height 52px, and the label always visible above it (not placeholder-only).

**`text-input-focused`**: 2px `{colors.primary}` border.

**`text-input-error`**: 2px `{colors.danger}` border plus an error message below in `{colors.danger-text}` with an icon.

**`search-pill`** and **`filter-dropdown`**: min-height 48px.

Numeric inputs for readings use `inputmode="decimal"` and show the unit as a suffix.

### Tabs & Toggles

**`pill-tab`** / **`pill-tab-active`**: inactive tabs have `{colors.text-secondary}` text on `{colors.canvas}`; the active tab is `{colors.primary}` with dark `{colors.on-primary}` text. Min-height 48px.

**`language-toggle`**: a segmented pill, **ಕನ್ನಡ | English**. The active segment is `{colors.primary}` with dark `{colors.on-primary}` text.

### Tables

**`data-table`** / **`data-row`**: reading history. `{typography.body-md}`, 16px × 20px cell padding, a status dot + word in the status column, and horizontal scroll on phones rather than squeezing columns.

### Navigation

**Top bar**: sticky `{colors.surface}` bar, ~64px tall (it grows if Kannada labels wrap), with the app name in text on the left and the language toggle plus a primary action on the right. Below 1024px it collapses to a menu button.

**Bottom navigation (mobile app screens)**: 3–5 items, each with an icon and a text label (never icon-only), and 56px-tall targets.

### Signature Components

**`hero-band`**: centered `hero-display` headline, subtitle, button row and a pond illustration below.

**`cta-banner`**: deep indigo-blue banner (`{colors.secondary}`) with a `{rounded.feature}` radius, a centered headline and a `button-primary`.

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
- Don't use purple, violet or lavender anywhere
- Don't use status colors for decoration, branding or category tags
- Don't use the accent ({colors.accent}) on buttons or links, or as the only difference from primary: the two look almost the same
- Don't put light text on the accent; use {colors.on-accent} (dark)
- Don't use secondary ({colors.secondary}) as text or as a border on the dark background (1.7:1); it is a fill only
- Don't put status text colors (e.g. {colors.danger-text}) directly on the dark page; only on their own light status background
- Don't use {colors.on-primary} (dark) for text on status colors; use {colors.on-status}
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
6. Any new color must come from the brand palette (or be derived from it), must pass 4.5:1 for text (3:1 for borders and icons) on the dark background, and must not look like a status color
7. Use pill-shaped buttons (`{rounded.full}`) everywhere
8. Check every new component in both Kannada and English before calling it done

## Known Gaps

- Only the dark theme is defined. A light theme (e.g. for bright outdoor sunlight) is not yet designed
- Animation timings are not set; use 150–200ms ease and respect `prefers-reduced-motion`
- Exact Safe/Warning/Danger thresholds (oxygen, pH, temperature, ammonia) belong in the app's domain logic, not in this file
- Charts for reading history need their own palette spec; reuse the status colors only for threshold bands
