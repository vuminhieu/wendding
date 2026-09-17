---
title: QA — wedding countdown
status: completed
created: 2026-09-17
scope: markup + JS + grep + node math (no test framework, no browser)
---

# Test Report — 260917-1456 — wedding countdown

Static validation only. No unit/e2e suite invented. Browser skipped (no local server required; Puppeteer may be missing).

## Test Results Overview
- **Total**: 16 checkable items
- **Passed**: 16 | **Failed**: 0 | **Skipped**: 1 (browser)
- **Duration**: ~1s node math + file greps

## Coverage Metrics
N/A — no test runner / no coverage instrumentation. This is a criterion checklist, not Istanbul/c8.

## Criteria (pass/fail + evidence)

### 1. Markup IDs in `index.html`

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1.1 | `#countdown` after `#hero-invite` | **PASS** | `index.html` L80 `#hero-invite`, L84 `#countdown` (sibling after invite block, not inside `.hero-names`) |
| 1.2 | `#cd-days` / `#cd-hours` / `#cd-mins` / `#cd-secs` | **PASS** | L93, L97, L101, L105 |
| 1.3 | `#countdown-done` hidden | **PASS** | L109 `<p class="countdown-done" id="countdown-done" hidden>Hôm nay là ngày cưới</p>` |
| 1.4 | `#countdown-live` `aria-live=polite` | **PASS** | L90 `id="countdown-live" aria-live="polite"` |
| 1.5 | cells `aria-hidden` | **PASS** | L91 `#countdown-cells` has `aria-hidden="true"` (container, not each cell) |

### 2. JS in `js/invitation.js`

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 2.1 | `Date.parse("2026-10-25T00:00:00+07:00")` | **PASS** | L59 `WEDDING_DAY` |
| 2.2 | `THANKS_DAY` `2026-10-26T00:00:00+07:00` | **PASS** | L60 `Date.parse("2026-10-26T00:00:00+07:00")` |
| 2.3 | `pad2` | **PASS** | L62–64 `String(n).padStart(2, "0")`; used on hours/mins/secs L93–95 |
| 2.4 | `textContent` only (countdown path) | **PASS** | countdown writes via `done.textContent`, `live.textContent`, `cd-*.textContent` L76–100. No `innerHTML` in `renderCountdown`/`startCountdown`. Other `innerHTML` in file is hearts/calendar/guestbook, not countdown. |
| 2.5 | hidden skip | **PASS** | interval L108 `if (document.hidden) return;`; visibility handler L112 same |
| 2.6 | `visibilitychange` re-render can `clearInterval` | **PASS** | L111–114: on visible, `if (!renderCountdown()) clearInterval(id)` |

### 3. Node one-off (same math, no DOM)

Copied: `WEDDING_DAY`/`THANKS_DAY` parse, floor-mod remaining, pad2, copy branches.

Run at `nowISO=2026-09-17T07:56:10.665Z` (machine clock).

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 3.1 | remaining now → WEDDING_DAY | **PASS** | **37 days, 9 hours** (mins 3, secs 49). Copy `Còn 37 ngày 9 giờ`. Wedding epoch `1792861200000` = `2026-10-24T17:00:00.000Z` (= 00:00 +07 25/10). |
| 3.2 | `now >= WEDDING_DAY` copy | **PASS** | `now = WEDDING_DAY` → branch `wedding`, copy `Hôm nay là ngày cưới` |
| 3.3 | `now >= THANKS_DAY` copy | **PASS** | `now = THANKS_DAY` (`1792947600000` = `2026-10-25T17:00:00.000Z`) → branch `thanks`, copy `Trân trọng cảm ơn` |
| 3.4 | T-1ms still live | **PASS** | `WEDDING_DAY - 1` → live, 0d 0h 0m 0s padded `00` |

### 4. Grep constraints

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 4.1 | overlay has no countdown | **PASS** | Overlay `index.html` L18–52: names, date, invite, guest, open btn. Zero `countdown` / `cd-*` inside `#overlay`. Only countdown on page is hero L84–110 + cache query on css/js. |
| 4.2 | `DESIGN.md` has exception | **PASS** | L3 lede: “Hero cream 4-cell countdown to `00:00 25/10/2026 +07` is an intentional exception (not on overlay, not a second event clock).” Taste L12 same exception. DateBlock L181. Motion L261. |
| 4.3 | cache `v=countdown1` | **PASS** | `index.html` L10 `css/invitation.css?v=countdown1`; L423 `js/invitation.js?v=countdown1` |
| 4.4 | reduced-motion does not target `.countdown` | **PASS** | `@media (prefers-reduced-motion: reduce)` L2863–2880 lists `.sparkle`, `.music-btn…`, hover transforms, `.album-card` only. No `.countdown*` in that block. `.countdown` rules are L333–414 + responsive L2570–2578 (layout, not motion kill). |

### 5. Browser
**SKIPPED** — user: local static server not required; Puppeteer may be missing.

## Failed Tests
None.

## Performance Metrics
- Node remaining calc: instant
- No suite timing

## Build Status
- **Build**: N/A (static HTML/CSS/JS)
- **Warnings**: none from this check
- **Dependencies**: not exercised

## Critical Issues
None. 16/16 checkable items PASS.

## Recommendations
1. Low: live visual tick still unproven in browser. Optional later: open `index.html` after overlay, confirm cells update once/sec.
2. Low: `reports/extract.json` still says “No live countdown” (source extract, not DESIGN). Leave unless docs sync wanted.

## Next Steps
1. None blocking for countdown ship.
2. If visual QA needed: open invitation, screenshot `#countdown`.

## Unresolved Questions
- None on checkable criteria.
