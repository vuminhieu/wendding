---
title: Brainstorm — wedding day countdown
status: agreed
created: 2026-09-17
modes: []
---

# Brainstorm — countdown ngày cưới

## Problem-first

### 1. Solution-jumping diagnosis
User asked for a countdown to `00:00 25/10/2026`. Signal: guest should *feel* the wedding approaching after opening the thiệp. Pain: date lives as static type (`25 tháng 10`, day numeral `25`) — no live urgency.

### 2. Underlying problem
Guests who open the invitation weeks ahead need a single, emotional “how soon” cue without another logistics block (timeline already removed).

### 3. Assumption challenges
| Assumption | Risk if wrong | Test |
|---|---|---|
| Midnight 25/10 is the right target | Trai party is 24/10 16:00; guests may think clock is “wrong” | Copy: “Đến ngày cưới” not “đến tiệc” |
| 4 boxes + seconds feel like paper | Seconds tick = app/LED | Compact Times numerals, no glow |
| Hero under names is visible enough | Guest name block + envelope already tall | Keep 1 row, ~56px |
| DESIGN.md “no countdown” can be overridden | Clone fidelity vs product ask | Explicit exception in DESIGN.md |

### 4. Problem statement
- **Users:** invited guests on mobile (Zalo).
- **Struggle:** hard to *feel* remaining time; two event days (24 trai / 25 lễ+gái).
- **Cause:** dates are ceremonial numerals, not a timer; overlay is for open, not info.
- **Consequence:** Save The Date is pretty but inert.
- **Success:** after open, guest sees remaining **Ngày / Giờ / Phút / Giây** to wedding-day start; after that, a blessing instead of `00:00:00`.

### 5. Alternative framings
- **A (chosen):** urgency as compact cream timer under hero names.
- **B:** urgency as burgundy paper strip — heavier, fights lễ card.
- **C:** one-line digital clock — app-like.

### 6. Evidence status
Weak–medium: user request + VN wedding-invite convention (chungdoi-style 4 cells). DESIGN.md source clone had **no** live countdown.

### 7. Validation
- Visual: hero still reads as paper; no LED, no FAB.
- Clock: `Asia/Ho_Chi_Minh`, target `2026-10-25T00:00:00+07:00`.
- After target: numbers hide; blessing shows.
- Kill if it overlaps guest name or looks like a dashboard.

### 8. Stakeholder note
Countdown is an **intentional DESIGN.md exception**, not a second event schedule. One clock, wedding-day midnight, cream hero only.

## Requirements (exact)

| Item | Decision |
|---|---|
| Expected output | Live 4-cell countdown on opened invitation |
| Target | `00:00` 25/10/2026 `Asia/Ho_Chi_Minh` |
| Place | Hero, **below names**; if `#hero-invite` visible, **below guest name** |
| UI | 4 compact cells: Ngày · Giờ · Phút · Giây |
| After midnight 25/10 | Hide cells; show blessing (“Hôm nay là ngày cưới” → later “Trân trọng cảm ơn”) |
| Out of scope | Overlay, sticky FAB, second clock for 24/10, new colors/fonts, restoring timeline |
| Touchpoints | `index.html`, `css/invitation.css`, `js/invitation.js`, `DESIGN.md` |

## Approaches evaluated

| | A cream 4-cell | B burgundy strip | C one-line digits |
|---|---|---|---|
| Pros | Matches cream hero; light; VN-invite familiar | Material match to paper boards | Smallest DOM |
| Cons | Seconds can feel “tech” if styled loud | Competes with lễ `25` numeral | Reads as digital clock |
| Verdict | **Chosen** | Rejected | Rejected |

## Agreed solution

**Approach A.** After `.hero-names` (and guest block when shown), one cream countdown:

```
❦  Còn tới ngày cưới  ❦
[ 38 ] [ 12 ] [ 05 ] [ 03 ]
Ngày    Giờ    Phút   Giây
```

- Numerals: Times, burgundy, ~28–32px, `font-variant-numeric: tabular-nums`.
- Labels: Baskerville/Times 11–12px, muted burgundy.
- Optional thin ornament lines like overlay (not a new gold system).
- JS: compute remaining vs `Date.parse('2026-10-25T00:00:00+07:00')` (or equivalent offset); `setInterval` 1000ms; pad hours/min/sec 2 digits; days unpadded or 2+.
- `document.hidden` / `visibilitychange`: skip work when tab hidden (optional, cheap).
- After `now >= target`: `hidden` on cells; show `#countdown-done` text.
- Do **not** put on overlay; overlay stays open-invite.
- Do **not** start interval until overlay can be ignored visually (ok to tick while overlay open — hero is covered).

Copy:
- Label: `Còn tới ngày cưới` (not “còn tới tiệc” — trai is 24/10).
- Done (25/10 before/during day): `Hôm nay là ngày cưới`.
- Done (after 26/10 00:00, optional same node): `Trân trọng cảm ơn` — if one string only, use `Hôm nay là ngày cưới` on the 25th and switch the next calendar day.

## Implementation notes / risks

- **Windows `prefers-reduced-motion`:** countdown is *numbers*, not CSS bob. Do not `animation: none` the values. No pulse on cells.
- **Timezone:** never `new Date(2026, 9, 25)` without +07; guest abroad should still count to VN midnight.
- **Layout:** hero already tall (envelope + names + guest). Max one row of cells; margin-top ~16–24px; no extra paper wrap.
- **A11y:** `aria-live="polite"` on a single summary (`Còn 38 ngày 12 giờ`) not every ticking second (too noisy). Visual cells `aria-hidden` if live region exists.
- **DESIGN.md:** replace “Do not add a countdown clock” with exception: hero cream 4-cell to wedding-day 00:00 only.

## Success metrics

- Opened page: 4 cells tick; overlay unchanged.
- Target instant: cells gone, blessing visible.
- No overlap with `.hero-amp` / guest name on 390px width.
- No new palette/font.

## Next

`/ck:plan` (default) from this report — not TDD (no test suite; static HTML/CSS/JS).
