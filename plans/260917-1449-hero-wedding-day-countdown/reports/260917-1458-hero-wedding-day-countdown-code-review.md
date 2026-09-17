---
title: Code review — hero wedding-day countdown
status: completed
created: 2026-09-17
score: 8/10
scope: index.html, css/invitation.css, js/invitation.js, DESIGN.md
plan: plans/260917-1449-hero-wedding-day-countdown
---

# Code Review — 260917-1458 — hero wedding-day countdown

## Code Review Summary

### Scope
- Files reviewed: `index.html`, `css/invitation.css`, `js/invitation.js`, `DESIGN.md`
- Plan files: `plan.md`, `phase-01-markup-and-cream-4-cell-css.md`, `phase-02-tick-js-plus-design-md-exception.md`
- Lines of code analyzed: ~203 inserted across 4 files (+ surrounding overlay/guest/album/music/date contracts)
- Review focus: spec compliance vs plan + user AC; regression on overlay/`?to=`/date numeral/music/album; public contracts; vanilla patterns; lint/build
- Updated plans: `plans/260917-1449-hero-wedding-day-countdown/plan.md`, phase-01, phase-02
- Verification: `git diff HEAD` on 4 product files; `node --check js/invitation.js` → `JS_SYNTAX_OK`; no `package.json` / no TS / no linter config. No browser pass this review.

### Overall Assessment
Core countdown is correctly placed, timezone-safe, and scoped. Overlay/guest/music/album/date-numeral contracts intact. Two real gaps vs “cream 4-cell” + post-target copy: cells have no cream surface, and the “Còn tới ngày cưới” heading stays after the blessing swap. Neither is a ship-blocker for the locked functional AC. Score **8/10**.

### Spec checklist

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | Hero cream 4-cell **after** `#hero-invite`, **not** inside `.hero-names` | PASS (place) / WARN (cream surface) | `index.html:80-110` sibling after `#hero-invite`; `.hero-names` ends `:79` |
| 2 | Target **only** `Date.parse('2026-10-25T00:00:00+07:00')` | PASS | `js/invitation.js:59` `WEDDING_DAY`. No `new Date(2026, 9, 25)` for countdown. `THANKS_DAY` is the allowed 26/10 branch (`:60`) |
| 3 | Cells Ngày Giờ Phút Giây; Times burgundy `tabular-nums`; no pulse/glow/FAB/overlay clock | PASS | markup `:91-107`; CSS `:393-401`; no countdown keyframes; overlay `:18-52` has no countdown |
| 4 | `now >= target` hide cells + “Hôm nay là ngày cưới”; `>= 26/10 00:00+07` “Trân trọng cảm ơn” | PASS (logic) / WARN (label leftover) | `js/invitation.js:73-80`; CSS flex override `:382-384` |
| 5 | `aria-live` polite summary on **day/hour** change only | PASS | `index.html:90`; summary gate `:97-101` via `live.dataset.summary` |
| 6 | `prefers-reduced-motion` does not freeze/hide numbers | PASS | reduce block `css/invitation.css:2863-2880` does not mention `.countdown*` |
| 7 | DESIGN.md exception documented | PASS | lede `:3`, taste `:12`, DateBlock `:177-181`, HeroCountdown `:183-187`, motion `:261` |
| 8 | Cache bump css **and** js `?v=countdown1` | PASS | `index.html:10`, `:423` |
| 9 | Overlay unchanged (open-invite only) | PASS | overlay CTA still `#open-invite` `:45`; `openInvite` still click-only `:522` |
| 10 | Guest `?to=`, ceremony `25`, music, album | PASS | see regressions |

---

### Critical Issues
None.

No XSS in countdown path (`textContent` only). No overlay clock. No Maps keys. No broken open/`?to=`/`?open=1` contract.

---

### High Priority Findings
None that block the locked functional AC.

---

### Medium Priority Improvements

**M1. Post-target heading still says “Còn tới ngày cưới”**
When `now >= WEDDING_DAY`, JS hides `#countdown-cells` and shows `#countdown-done`, but `.countdown-label` is never hidden.

- Impact: opened page on 25/10 reads “Còn tới ngày cưới” + “Hôm nay là ngày cưới” (then “Trân trọng cảm ơn”). AT also gets the stale heading plus live blessing.
- Evidence: markup `index.html:85-109`; hide path `js/invitation.js:73-80` only toggles `cells`/`done`.
- Plan AC hid cells + blessing only — heading not specified — still contradictory UX.
- Fix (do not apply here): hide `.countdown-label` in the done branch, or swap the label text.

**M2. “Cream cells” are unboxed numbers**
Phase 1 / DESIGN.md HeroCountdown: “4 cream cells”. `.countdown-cell` is a flex column: `min-width: 48px`, no cream fill, no radius, no hairline. Page cream (`--surface-page`) shows through.

- Evidence: `css/invitation.css:386-391` vs tokens `--ink-cream: #ece4d8` unused on cells.
- Phase 1 also said “no extra paper wrap” / “no burgundy paper board” — so unboxed is defensible, but they do not read as cells vs a dashboard-or-paper row.
- 390px one-row: 4×48px + 3×12px gap = 228px; `flex-wrap: nowrap` `:379`. Static math only; no browser.

**M3. `cd-*` nodes assumed present**
`renderCountdown` guards `cells`/`done` (`js/invitation.js:70`) then unconditionally writes `#cd-days`… (`:92-95`). Partial DOM → throw → interval never clears. Current `index.html` has all four IDs. Low production risk.

---

### Low Priority Suggestions

**L1. Blessing live-region write is not gated**
Done branch always sets `live.textContent` (`:79`). Boot-after-target is one shot (`startCountdown` returns). Fine. If interval ever failed to clear, AT would re-announce every 1s. Interval does clear on `false`.

**L2. Two `visibilitychange` listeners**
Countdown `:111-114` and album `:626-629` are independent. No clash. Could share one listener later; YAGNI.

**L3. Desktop-only size bump**
Phase 1 asked smaller nums in the mobile `.hero-names` block. Implementation enlarged at `min-width: 768px` (`css/invitation.css:2570-2580`): gap 16px, num 32px. Mobile stays `clamp(26px, 7vw, 32px)` — OK, not a miss.

**L4. `HeroCountdown` DESIGN.md section is extra vs the four mandated patches.** Justified; matches existing DateBlock pattern.

---

### Positive Observations
- Placement is correct: sibling of `.hero-names` / `#hero-invite`, so `.hero-amp { position:absolute }` cannot cover the row (`css/invitation.css:293-303`, `index.html:75-110`).
- TZ-safe ISO `+07:00` via `Date.parse`; remaining math floor + `%` matches plan; `pad2` on h/m/s; days unpadded (`js/invitation.js:83-95`).
- `aria-hidden="true"` on visual cells + clipped `.countdown-live` (`css/invitation.css:362-372`).
- Flex `[hidden] { display:none }` needed because `.countdown-cells { display:flex }` would otherwise beat the UA `hidden` rule (`:382-384`). Same pattern as `.overlay[hidden]`.
- Cache queries both bumped to `countdown1`.
- DESIGN.md drops the blanket ban in all four required spots; ceremony numeral still “not a timer”.
- Vanilla IIFE, `getElementById`, `textContent`, `setInterval(1000)` — matches existing `invitation.js`.
- Overlay still names + date + open button only.

---

### Regression / public contracts

| Contract | Result | Evidence |
|----------|--------|----------|
| Overlay open | PASS | `#open-invite` `index.html:45`; `openInvite` `js/invitation.js:167-190`; listener `:522`. No countdown in overlay `:18-52`. |
| `?to=` guest name | PASS | `applyGuestName` still `:44-57`; `openInvite` `url.searchParams.set("open","1")` only (`:187-189`); no `delete("to")`. `#hero-invite` still `hidden` until name (`index.html:80`). |
| Ceremony day numeral `25` | PASS | static `index.html:151`, `:258`. Not `role="timer"`. Calendar `new Date(2026, 9, 1)` is weekday offset only (`js/invitation.js:195`). |
| Music | PASS | `#music-btn` / `playMusic` / overlay-open play path unchanged (`:151-165`, `:172`, `:518`, `:523-526`). |
| Album | PASS | PHOTO_IDS, `renderAlbum`, nav, autoplay, drag block untouched. Extra `visibilitychange` does not remove album’s. |
| `?open=1` | PASS | `alreadyOpen` `:31`, `:514-520`. |
| Public IDs/query | PASS | additive `#countdown*` / `#cd-*` only; cache query intentionally changed. |

---

### Type / lint / build
- No `package.json`, no TS, no eslint/prettier config in repo.
- `node --check js/invitation.js` → OK.
- No new type/lint/build errors to report. CSS/HTML not machine-linted.

---

### Recommended Actions
1. Hide or rewrite `.countdown-label` when blessing is shown (M1).
2. If “cream cells” must read as paper tiles, add a light cream fill + hairline using existing `--ink-cream` / burgundy — no new palette (M2). Confirm 390px still one row.
3. Optional: null-guard `cd-*` (M3).
4. Browser-check 390px vs `.hero-amp` and overlay-open; this review did not run a browser.

Do **not** rewrite the feature for style nits. Do **not** add overlay/FAB/24/10 clocks.

---

### Metrics
- Type coverage: N/A (vanilla JS)
- Test coverage: N/A (no runner). Prior QA `plans/reports/260917-1456-wedding-countdown-qa.md` did not flag M1/M2.
- Linting issues: 0 known (no linter)
- Score: **8/10**
- Critical: 0 · Warnings: 2 (M1, M2) · Suggestions: 4

---

### Unresolved questions
- Is unboxed type-on-cream enough to satisfy “cream cells”, or are light tiles required?
- Should the heading hide with the cells after midnight 25/10?
- 390px overlap with `.hero-amp` unverified in a real viewport.
