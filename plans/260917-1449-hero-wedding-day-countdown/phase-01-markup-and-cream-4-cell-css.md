---
phase: 1
title: Markup and cream 4-cell CSS
status: completed
priority: P2
effort: S
dependencies: []
---

# Phase 1: Markup and cream 4-cell CSS

## Overview

Insert the countdown DOM under the hero (after guest block) and style a single cream row so it reads as paper, not a dashboard. JS in phase 2 fills numbers; this phase can leave placeholder digits.

## Requirements

- Functional: markup exists with stable IDs; 4 cells + done line + live summary; default shows cells, done hidden.
- Non-functional: one row ~56px cells; margin-top 16–24px; no extra paper wrap; no new colors/fonts; no pulse.

## Architecture

Insert **after** `#hero-invite`, still inside `<header>`, **not** inside `.hero-names`:

```html
<div class="countdown" id="countdown">
  <p class="countdown-label">
    <span class="countdown-orn" aria-hidden="true">❦</span>
    Còn tới ngày cưới
    <span class="countdown-orn" aria-hidden="true">❦</span>
  </p>
  <p class="countdown-live" id="countdown-live" aria-live="polite"></p>
  <div class="countdown-cells" id="countdown-cells" aria-hidden="true">
    <div class="countdown-cell"><span class="countdown-num" id="cd-days">—</span><span class="countdown-unit">Ngày</span></div>
    <div class="countdown-cell"><span class="countdown-num" id="cd-hours">—</span><span class="countdown-unit">Giờ</span></div>
    <div class="countdown-cell"><span class="countdown-num" id="cd-mins">—</span><span class="countdown-unit">Phút</span></div>
    <div class="countdown-cell"><span class="countdown-num" id="cd-secs">—</span><span class="countdown-unit">Giây</span></div>
  </div>
  <p class="countdown-done" id="countdown-done" hidden>Hôm nay là ngày cưới</p>
</div>
```

Visually hide `.countdown-live` (clip/sr-only) — it is for AT, not a second heading.

## Related Code Files

- Modify: `index.html` — insert block; bump `css/invitation.css?v=` (leave JS bump for phase 2 or bump both here)
- Modify: `css/invitation.css` — after `.hero-guest` (~L323)

## Implementation Steps

1. Insert markup after `#hero-invite` (before `</header>`).
2. Style:
   - `.countdown`: centered, `margin-top: 20px`, `padding: 0 20px`, `z-index: 10`
   - `.countdown-label`: Times/Baskerville ~12px, letter-spacing, `--ink-burgundy` or 80%
   - `.countdown-orn`: muted, small; optional thin lines via `::before/::after` like overlay — not a new gold system
   - `.countdown-cells`: flex, `justify-content: center`, `gap: 10–14px`, one row, no wrap on 390px (shrink gap/num if needed)
   - `.countdown-num`: Times 28–32px (clamp), weight 300–400, `--ink-burgundy`, `font-variant-numeric: tabular-nums`, `min-width` so 2-digit hours don’t jump
   - `.countdown-unit`: Baskerville 11–12px, muted burgundy
   - `.countdown-done`: same family as label, shown only when not `[hidden]`
   - `.countdown-live`: visually hidden
3. Do **not** add keyframes or hover scale on cells.
4. Mobile block (~L2454 `.hero-names`): if needed, slightly smaller nums; still one row.
5. Cache-bust CSS query in `index.html`.

## Success Criteria

- [x] `#countdown` is after `#hero-invite`, not inside `.hero-names` (`index.html:80-110`)
- [x] Four cells + hidden `#countdown-done` + `aria-live` node exist (`index.html:90-109`)
- [x] 390px: one row in CSS (`flex-wrap: nowrap`, 4×48px + gaps); `.hero-amp` overlap not browser-verified
- [x] Cream/burgundy/Times only; no glow, no pulse, no burgundy paper board — cells unboxed (type on page cream)
- [x] CSS cache query bumped (`index.html:10` `?v=countdown1`)

## Risk Assessment

Hero is already tall (envelope + names + guest). Mitigation: no extra wrap, tight vertical rhythm. Amp is `position: absolute` on `.hero-names` — countdown as sibling avoids covering `&`.
