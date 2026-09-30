---
version: alpha
name: pond-design-system
description: A calm, water-toned design system for a pond and fish-health app. Deep pond blue ({colors.primary}) anchors every primary action on a clean white canvas, soft water and reed tints (blue, teal, green) give feature cards a natural feel, and a strict three-level status palette — Safe green, Warning amber, Danger red — is reserved for pond and fish condition readings only. Type is set large for readability outdoors and on low-end phones, and every text style is tuned to render Kannada (ಕನ್ನಡ) script as comfortably as English.

colors:
  primary: "#0b4f6c"
  primary-pressed: "#083a50"
  on-primary: "#ffffff"
  brand-teal: "#0e7c7b"
  teal-light: "#d4f1ef"
  brand-water: "#1d6fa5"
  water-light: "#dff1f6"
  brand-reed: "#2f8a5b"
  reed-light: "#dcf3ea"
  moss-dark: "#0b5e4a"
  sand-light: "#f6f1e4"
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
  canvas: "#ffffff"
  surface: "#f3f8fa"
  surface-soft: "#f8fbfc"
  surface-featured: "#e8f4f8"
  hairline: "#d5e2e7"
  hairline-soft: "#e6eef1"
  hairline-strong: "#a9bfc8"
  ink-deep: "#0a1f29"
  ink: "#0f2a36"
  charcoal: "#1e3a46"
  slate: "#3f5a66"
  steel: "#56707b"
  muted: "#7b929c"
  on-dark: "#ffffff"
  on-dark-muted: "#b8cbd3"
  footer-bg: "#0a1f29"

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
  button-teal:
    backgroundColor: "{colors.brand-teal}"
    textColor: "{colors.on-primary}"
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
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "14px 28px"
    minHeight: 52px
  button-on-dark:
    backgroundColor: "{colors.on-dark}"
    textColor: "{colors.primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "14px 28px"
    minHeight: 52px
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: "10px 14px"
    minHeight: 48px
  button-link:
    backgroundColor: "transparent"
    textColor: "{colors.brand-water}"
    typography: "{typography.body-md-medium}"
    padding: "0"
    textDecoration: underline
  button-icon-circular:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
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
  card-feature-water:
    backgroundColor: "{colors.water-light}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
  card-feature-teal:
    backgroundColor: "{colors.teal-light}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
  card-feature-reed:
    backgroundColor: "{colors.reed-light}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
  card-feature-sand:
    backgroundColor: "{colors.sand-light}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
  card-pond:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
    border: "1px solid {colors.hairline}"
    borderLeft: "6px solid {status color}"
  card-stat:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.stat-display}"
    padding: "{spacing.lg}"
  card-highlighted:
    backgroundColor: "{colors.surface-featured}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xxl}"
    border: "2px solid {colors.brand-water}"
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
    textColor: "{colors.on-primary}"
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
    textColor: "{colors.on-primary}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "6px 14px"
  badge-tag-water:
    backgroundColor: "{colors.water-light}"
    textColor: "{colors.primary}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "6px 14px"
  badge-tag-reed:
    backgroundColor: "{colors.reed-light}"
    textColor: "{colors.moss-dark}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "6px 14px"
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
    border: "1px solid {colors.hairline-strong}"
    minHeight: 52px
  text-input-focused:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    border: "2px solid {colors.brand-water}"
  text-input-error:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    border: "2px solid {colors.danger}"
  search-pill:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.steel}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.xs} {spacing.md}"
    minHeight: 48px
    border: "1px solid {colors.hairline}"
  filter-dropdown:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm-medium}"
    rounded: "{rounded.full}"
    padding: "{spacing.xs} {spacing.md}"
    minHeight: 48px
    border: "1px solid {colors.hairline-strong}"
  pill-tab:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.slate}"
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
    textColor: "{colors.ink}"
    typography: "{typography.body-sm-medium}"
    rounded: "{rounded.full}"
    padding: "4px"
    minHeight: 48px
  data-table:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    border: "1px solid {colors.hairline}"
  data-row:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    padding: "{spacing.md} {spacing.lg}"
    border: "0 0 1px {colors.hairline-soft} solid"
  faq-accordion-item:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.md}"
    padding: "{spacing.xl}"
    border: "0 0 1px {colors.hairline} solid"
  hero-band:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.hero-display}"
    rounded: "0"
    padding: "{spacing.hero}"
  cta-banner-dark:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.feature}"
    padding: "{spacing.section}"
  footer-region:
    backgroundColor: "{colors.footer-bg}"
    textColor: "{colors.on-dark}"
    typography: "{typography.body-sm}"
    padding: "{spacing.section} {spacing.xxl}"
  footer-link:
    backgroundColor: "transparent"
    textColor: "{colors.on-dark-muted}"
    typography: "{typography.body-sm}"
    padding: "{spacing.xs} 0"
---

## Overview

This is a calm, water-toned design system for a pond and fish-health app. It is used by pond owners and fish farmers, often outdoors, on phones, and in either Kannada or English. Every screen opens on a clean white canvas. The main action is always a deep pond-blue pill button ({colors.primary}). Soft water, teal and reed tints give feature cards a natural, outdoor feel. The palette is only blues, teals and greens: there is no purple or lavender anywhere in the system.

The most important job of the interface is to make pond condition clear at a glance. Green, amber and red mean only one thing each: **Safe**, **Warning** and **Danger**. These colors never appear as decoration, and each status always comes with an icon and a word, never color alone.

Text is set larger than a typical web app: body text is 18px, and nothing that must be read is smaller than 15px. Every style is tuned so Kannada (ಕನ್ನಡ) renders as comfortably as English, with generous line height and no negative letter-spacing.

**Key Characteristics:**
- White canvas with deep pond-blue pill CTAs ({colors.primary} + `{rounded.full}`)
- Water, teal, reed and sand tints for feature cards
- A strict Safe/Warning/Danger palette used only for condition status, always paired with an icon and a label
- Large, readable type: 18px body, 52px-tall buttons, 48px minimum touch targets
- Noto Sans + Noto Sans Kannada on every surface, with line heights tall enough for Kannada vowel signs and conjuncts
- Deep-water dark footer ({colors.footer-bg})

## Colors

### Brand & Accent
- **Pond Blue** ({colors.primary}): Primary buttons, active tabs, dark CTA banners. White text on it measures 8.9:1.
- **Pond Blue Pressed** ({colors.primary-pressed}): Pressed state for primary actions.
- **Water Blue** ({colors.brand-water}): Links, focus rings, highlighted-card border. 5.4:1 on white.
- **Water Light** ({colors.water-light}): Pale blue feature-card and tag background.
- **Teal** ({colors.brand-teal}): Secondary filled button. White text on it measures 5.0:1.
- **Teal Light** ({colors.teal-light}): Pale teal feature-card background.
- **Reed Green** ({colors.brand-reed}): Decorative accent for illustrations and icons only. Not for status.
- **Reed Light** ({colors.reed-light}): Pale green feature-card and tag background.
- **Moss Dark** ({colors.moss-dark}): Text on reed-tinted chips.
- **Sand Light** ({colors.sand-light}): Warm, neutral feature-card background (a pond-bank tone) for variety.

### Status (Safe / Warning / Danger)
These colors are reserved for pond and fish condition: water quality, oxygen, temperature, pH, ammonia and alerts.

| Level | Solid | Background | Text on background | Icon | Contrast |
|---|---|---|---|---|---|
| **Safe** | {colors.safe} `#1a7f37` | {colors.safe-bg} | {colors.safe-text} | check-circle | white on solid 5.1:1 · text on bg 8.8:1 |
| **Warning** | {colors.warning} `#f5a524` | {colors.warning-bg} | {colors.warning-text} | alert-triangle | dark ink on solid 9.1:1 · text on bg 7.4:1 |
| **Danger** | {colors.danger} `#c62828` | {colors.danger-bg} | {colors.danger-text} | alert-octagon | white on solid 5.6:1 · text on bg 9.1:1 |

- Text on the amber Warning solid is always dark ({colors.on-warning}). White text on amber fails contrast.
- Red and green look alike to color-blind users. The **icon shape and the word** (Safe / ಸುರಕ್ಷಿತ, Warning / ಎಚ್ಚರಿಕೆ, Danger / ಅಪಾಯ) are what carry the meaning; color only reinforces it.

### Surface
- **Canvas White** ({colors.canvas}): Page background and primary card surface.
- **Surface** ({colors.surface}): Subtle, slightly blue-tinted section backgrounds and search-field rest.
- **Surface Soft** ({colors.surface-soft}): Quieter section divisions.
- **Surface Featured** ({colors.surface-featured}): Pale water tint for a highlighted card.
- **Hairline** ({colors.hairline}): 1px borders and dividers.
- **Hairline Soft** ({colors.hairline-soft}): Quieter table-row dividers.
- **Hairline Strong** ({colors.hairline-strong}): Input borders.

### Text
- **Ink Deep** ({colors.ink-deep}): Headlines on tinted cards.
- **Ink** ({colors.ink}): Primary headlines and body text (15:1 on white).
- **Charcoal** ({colors.charcoal}): Body emphasis.
- **Slate** ({colors.slate}): Secondary text and metadata (7.3:1).
- **Steel** ({colors.steel}): Tertiary text and placeholders (5.3:1). This is the lightest color allowed for readable text.
- **Muted** ({colors.muted}): Disabled labels only (3.3:1). Never use it for text people need to read.
- **On Dark** ({colors.on-dark}) / **On Dark Muted** ({colors.on-dark-muted}): Text on the dark footer and CTA banners.

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
| `{rounded.xxxl}` | 28px | Tinted feature cards |
| `{rounded.feature}` | 32px | Dark CTA banner |
| `{rounded.full}` | 9999px | All buttons, pill tabs, badges |

## Components

> Hover states are not documented here. Only default, pressed, focus and disabled states are.

### Buttons

**`button-primary`**: the pond-blue pill used for the main action on a screen ("Check pond", "Save reading").
- Background `{colors.primary}`, text `{colors.on-primary}`, `{typography.button-md}`, padding `14px 28px`, min-height 52px, `{rounded.full}`.
- Pressed state: `{colors.primary-pressed}`. Disabled: `{colors.hairline}` background with `{colors.muted}` text.

**`button-teal`**: teal pill for a secondary filled action.

**`button-secondary`**: an outlined pill with a 2px `{colors.primary}` border and pond-blue text.

**`button-danger`**: red pill, used only for destructive or emergency actions ("Delete pond", "Call for help").

**`button-on-dark`**: white pill on dark banners.

**`button-ghost`**: quiet rectangular button, min-height 48px.

**`button-link`**: underlined inline link in `{colors.brand-water}`.

**`button-icon-circular`**: 48×48px circular icon button. It always has an `aria-label` in the current language.

**Focus**: every interactive element shows a 3px `{colors.brand-water}` outline with a 2px offset on `:focus-visible`.

### Cards & Containers

**`card-base`**: white card with a 16px radius and a hairline border.

**`card-feature`** and the tinted variants **`card-feature-water`**, **`card-feature-teal`**, **`card-feature-reed`** and **`card-feature-sand`**: 28px radius, 32px padding, `{colors.ink}` text. Tints are decorative only, so a reed-green card doesn't mean "safe".

**`card-pond`**: the core dashboard card for one pond. It has a white background, a hairline border, and a **6px left border in the pond's current status color**. It shows the pond name (`heading-3`), a status badge, 2–4 key readings in `stat-display`, and a "last updated" caption.

**`card-stat`**: a single large reading ("6.2 mg/L") in `stat-display`, with its label and unit beneath in `body-sm`.

**`card-highlighted`**: a pale water background with a 2px `{colors.brand-water}` border, for a recommended or featured item.

### Status

**`status-banner-safe` / `status-banner-warning` / `status-banner-danger`**: full-width banners at the top of a pond screen.
- Tinted background, 2px solid border in the status color, `{typography.status-label}` text in the matching dark text color, and a 24px leading icon.
- Structure: **icon + status word + one-line reason + next step**. For example: ⚠ **Warning**: Oxygen is low (4.1 mg/L). Run the aerator.
- Danger banners use `role="alert"`. Safe and Warning banners use `role="status"`.

**`badge-safe` / `badge-warning` / `badge-danger`**: solid pill badges with an icon and a word. The Warning badge uses dark text.

**`badge-tag-water` / `badge-tag-reed`**: neutral category tags such as fish species or pond type. These are never used to show status.

### Inputs & Forms

**`text-input`**: white field with a strong hairline border, `{typography.body-md}`, min-height 52px, and the label always visible above it (not placeholder-only).

**`text-input-focused`**: 2px `{colors.brand-water}` border.

**`text-input-error`**: 2px `{colors.danger}` border plus an error message below in `{colors.danger-text}` with an icon.

**`search-pill`** and **`filter-dropdown`**: min-height 48px.

Numeric inputs for readings use `inputmode="decimal"` and show the unit as a suffix.

### Tabs & Toggles

**`pill-tab`** / **`pill-tab-active`**: inactive tabs have `{colors.slate}` text on white; the active tab is `{colors.primary}` with white text. Min-height 48px.

**`language-toggle`**: a segmented pill, **ಕನ್ನಡ | English**. The active segment is `{colors.primary}` with white text.

### Tables

**`data-table`** / **`data-row`**: reading history. `{typography.body-md}`, 16px × 20px cell padding, a status dot + word in the status column, and horizontal scroll on phones rather than squeezing columns.

### Navigation

**Top bar**: sticky white bar, ~64px tall (it grows if Kannada labels wrap), with the app name in text on the left and the language toggle plus a primary action on the right. Below 1024px it collapses to a menu button.

**Bottom navigation (mobile app screens)**: 3–5 items, each with an icon and a text label (never icon-only), and 56px-tall targets.

### Signature Components

**`hero-band`**: centered `hero-display` headline, subtitle, button row and a pond illustration below.

**`cta-banner-dark`**: deep pond-blue banner (`{colors.primary}`) with a `{rounded.feature}` radius, a centered headline and a `button-on-dark`.

**`footer-region`** / **`footer-link`**: deep-water footer (`{colors.footer-bg}`) with `{colors.on-dark-muted}` links at 16px.

## Do's and Don'ts

### Do
- Use `{colors.primary}` pond blue for the one main action on each screen
- Keep green, amber and red strictly for Safe / Warning / Danger, always with an icon and a word
- Put dark text ({colors.on-warning}) on amber
- Keep body text at 18px and use nothing readable below 15px
- Test every screen in Kannada, with long labels and deep conjuncts
- Use `{rounded.full}` on every button, tab and badge
- Keep touch targets at 48px or larger

### Don't
- Don't use purple, violet or lavender anywhere
- Don't use status colors for decoration, branding or category tags
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
6. Any new color must be a blue, teal or green, must pass 4.5:1 for text, and must not look like a status color
7. Use pill-shaped buttons (`{rounded.full}`) everywhere
8. Check every new component in both Kannada and English before calling it done

## Known Gaps

- Dark-mode token values are not yet defined
- Animation timings are not set; use 150–200ms ease and respect `prefers-reduced-motion`
- Exact Safe/Warning/Danger thresholds (oxygen, pH, temperature, ammonia) belong in the app's domain logic, not in this file
- Charts for reading history need their own palette spec; reuse the status colors only for threshold bands
