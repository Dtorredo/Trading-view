---
name: Luminous Ledger
colors:
  surface: '#10131a'
  surface-dim: '#10131a'
  surface-bright: '#363941'
  surface-container-lowest: '#0b0e15'
  surface-container-low: '#191b23'
  surface-container: '#1d2027'
  surface-container-high: '#272a31'
  surface-container-highest: '#32353c'
  on-surface: '#e1e2ec'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#e1e2ec'
  inverse-on-surface: '#2e3038'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffb2b7'
  on-tertiary: '#67001b'
  tertiary-container: '#ff516a'
  on-tertiary-container: '#5b0017'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdadb'
  tertiary-fixed-dim: '#ffb2b7'
  on-tertiary-fixed: '#40000d'
  on-tertiary-fixed-variant: '#92002a'
  background: '#10131a'
  on-background: '#e1e2ec'
  surface-variant: '#32353c'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-desktop: 40px
  margin-mobile: 16px
  container-max-width: 1440px
---

## Brand & Style
The design system is engineered for a premium high-frequency FinTech environment where precision, speed, and clarity are paramount. The brand personality is "Technological Sophistication"—it feels like a high-end cockpit, prioritizing data density without sacrificing elegance.

The design style leverages **Glassmorphism** and **Minimalism**. By using translucent layers over a deep charcoal canvas, the UI creates a sense of physical depth and focus. High-contrast accents are used sparingly to direct attention to critical financial movements, while structural elements remain recessed. The emotional response should be one of "Controlled Power" and "Institutional Trust."

## Colors
The palette is built on a "Deep Dark" foundation to reduce eye strain during extended trading sessions. 

- **Base Layer:** `#09090b` (Deep Slate) serves as the primary canvas.
- **Surface Layer:** `#0f172a` (Charcoal) is used for elevated glass panels.
- **Action Primary:** `#3b82f6` (Electric Blue) is reserved for primary calls to action, active states, and system-level indicators.
- **Success/Positive:** `#10b981` (Emerald) denotes gains, "buy" signals, and completed transactions.
- **Danger/Negative:** `#f43f5e` (Crimson) denotes losses, "sell" signals, and critical alerts.
- **Borders:** Use a subtle, semi-transparent white (`rgba(255, 255, 255, 0.08)`) to define glass edges without introducing visual noise.

## Typography
This design system utilizes **Inter** for its clinical precision and modern geometric construction, ensuring readability in dense data environments. For financial figures, ticker symbols, and secondary metadata, **Inter** is employed to provide a technical, monospaced feel that ensures tabular numbers align perfectly.

Headlines should use tighter letter spacing to maintain a "premium" feel. Body copy remains legible with generous line heights. Always use monospaced variants for fluctuating price data to prevent layout "jitter" during real-time updates.

## Layout & Spacing
The layout follows a **Fluid Grid** system within a max-width container of 1440px. The spacing rhythm is based on a 4px baseline grid to ensure mathematical alignment of technical charts and data tables.

- **Desktop:** 12-column grid with 24px gutters.
- **Tablet:** 8-column grid with 20px gutters.
- **Mobile:** 4-column grid with 16px gutters and 16px side margins.

Information density is high. Use `16px` (4 units) for standard padding within glass cards, and `24px` (6 units) for section separation.

## Elevation & Depth
Depth is created through **Glassmorphism** rather than traditional drop shadows.
- **Level 1 (Base):** Deep Slate background.
- **Level 2 (Panels):** Charcoal surface with `backdrop-filter: blur(12px)` and a 1px `solid` border. The border should have a linear gradient from top-left (`rgba(255,255,255,0.12)`) to bottom-right (`rgba(255,255,255,0.02)`).
- **Level 3 (Modals/Popovers):** Higher transparency, `blur(20px)`, and a subtle outer glow using the primary color at 5% opacity to indicate focus.

Avoid heavy black shadows; instead, use "Inner Glows" (1px white stroke at low opacity) on the top edge of elements to simulate a light source from above.

## Shapes
The shape language is "Refined Modern." All glass panels, buttons, and input fields use a **0.5rem (8px)** corner radius. This provides a balance between the clinical feel of sharp corners and the overly casual nature of fully rounded shapes.

- **Standard Elements:** 8px (`rounded-md`).
- **Large Containers:** 16px (`rounded-lg`).
- **Contextual Chips:** 4px (`rounded-sm`) to maintain a technical, "tag-like" appearance.

## Components
### Buttons
- **Primary:** Solid Electric Blue with white text. Subtle inner-top highlight.
- **Secondary:** Glass-style (translucent) with a 1px white border.
- **Ghost:** No background, Blue text, appears on hover with a 5% blue fill.

### Data Cards
Glass containers containing a headline, a monospaced value, and a "Mini-Sparkline" chart. Sparklines use Emerald for positive trends and Crimson for negative.

### Input Fields (Position Sizing)
Darker than the panel surface (`#050505`). High-contrast focus state with a 1px Electric Blue border. Include "Quick-action" percentage chips (25%, 50%, Max) inside the trailing edge of the input.

### Charts
- **Grid Lines:** Minimal, using `rgba(255,255,255,0.03)`.
- **Area Charts:** Use a vertical gradient from the accent color (Emerald/Crimson) to transparent.
- **Tooltips:** High-blur glass panels with monospaced data labels.

### Chips & Status
Small, uppercase monospaced text. Status indicators use a small "Glowing Dot" (box-shadow) next to the label to indicate real-time connectivity or market status.
