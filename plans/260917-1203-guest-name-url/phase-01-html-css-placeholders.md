---
phase: 1
title: HTML+CSS placeholders
status: completed
priority: P2
dependencies: []
---

# Phase 1: HTML+CSS placeholders

## Overview

Add hidden guest-name nodes on overlay and hero, plus CSS so they match existing type. Empty/hidden by default — no JS yet.

## Requirements

- Functional: overlay name under “Thân Mời”; hero line under couple names; both `hidden` until JS unhides.
- Non-functional: wrap long names; no layout shift when hidden; match overlay/hero type.

## Architecture

Static markup only. JS in phase 2 sets `textContent` and removes `hidden`.

## Related Code Files

- Modify: `index.html`
- Modify: `css/invitation.css`
- Modify: `index.html` stylesheet query (`?v=pagebg1` → `?v=guest1`)

## Implementation Steps

1. Overlay, after `.overlay-invite`, before `#open-invite`:

```html
<p class="overlay-guest" id="overlay-guest" hidden></p>
```

2. Hero, after `.hero-names` (sibling, not inside the flex names column so `&` overlay stays):

```html
<p class="hero-guest" id="hero-guest" hidden></p>
```

3. CSS — overlay: same family as `.overlay-invite`, slightly smaller (~16px), burgundy ~0.85 opacity, wrap, `word-break: break-word`, max-width 100%, `margin: 0 0 20px`. Keep `.overlay-invite { margin-bottom: 24px }` when guest hidden; when guest shown, reduce invite bottom margin via `.overlay-invite:has(+ .overlay-guest:not([hidden])) { margin-bottom: 8px }` **or** always `margin-bottom: 8px` on invite and let guest own the 24px gap (simpler: invite `margin-bottom: 8px`, guest `margin-bottom: 24px`; hidden guest collapses so invite-to-button gap shrinks ~16px). **Preferred:** keep invite `margin-bottom: 24px`; guest `margin: -12px 0 24px` only when not hidden — messy. **Do this:** `.overlay-invite { margin-bottom: 8px }` and `.overlay-guest { margin: 0 0 24px }`; when guest `[hidden]`, add `.overlay-invite { margin-bottom: 24px }` restored via:

```css
.overlay-invite {
  margin-bottom: 24px;
}
.overlay-guest {
  margin: 8px 0 24px;
  font-family: var(--font-overlay);
  font-size: 16px;
  font-weight: 400;
  color: rgba(81, 20, 25, 0.88);
  line-height: 1.35;
  word-break: break-word;
}
.overlay-guest:not([hidden]) + .open-btn {
  /* no-op; guest already has bottom margin */
}
.overlay-invite:has(+ .overlay-guest:not([hidden])) {
  margin-bottom: 0;
}
```

`:has()` OK (this site already modern). Fallback if worried: always 8px invite + 24px guest including when hidden — then default gap becomes 8px (too tight). Stick with `:has()`.

4. Hero guest:

```css
.hero-guest {
  position: relative;
  z-index: 10;
  margin: 12px 0 0;
  padding: 0 24px;
  text-align: center;
  font-family: var(--font-overlay);
  font-size: 16px;
  font-weight: 400;
  color: var(--ink-burgundy);
  line-height: 1.4;
  word-break: break-word;
}
```

5. Bump CSS `?v=guest1`.

## Success Criteria

- [x] `#overlay-guest` exists, `hidden`, empty, after “Thân Mời”
- [x] `#hero-guest` exists, `hidden`, empty, after `.hero-names`
- [x] No `to` looks like current overlay/hero (gap to Open button unchanged via `:has()`)
- [x] CSS wraps long names; no overflow of overlay card

## Risk Assessment

`:has()` unsupported in very old WebViews — Zalo in-app is Chromium-based; acceptable. If broken, invite-to-button gap stays 24px plus guest margin (slightly looser). No JS in this phase.
