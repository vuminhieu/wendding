---
title: Hero wedding-day countdown
description: >-
  Cream 4-cell countdown under hero names to 00:00 25/10/2026 +07; after
  midnight hide numbers and show a blessing. DESIGN.md exception.
status: completed
priority: P2
branch: main
tags:
  - frontend
  - invitation
blockedBy: []
blocks: []
created: "2026-09-17T07:49:50.024Z"
createdBy: "ck:plan"
source: skill
---

# Hero wedding-day countdown

## Overview

Opened thiệp needs a live “how soon” cue. One cream row under hero names (below `#hero-invite` when that block is shown): Ngày · Giờ · Phút · Giây to **wedding-day start**, not to the 24/10 trai party.

Brainstorm (agreed, HOLD SCOPE): `plans/reports/260917-1400-wedding-countdown.md`. Guest-name and photo-load plans are **completed** — same files, no unfinished overlap.

No TDD. Static HTML/CSS/JS. Fast plan.

## Locked decisions

| Item | Value |
|------|--------|
| Target | `2026-10-25T00:00:00+07:00` (`Date.parse` / ISO with offset). Never `new Date(2026, 9, 25)` local. |
| Place | Hero, **after** `#hero-invite` (sibling of `.hero-names`, not inside it — amp overlay stays) |
| UI | 4 compact cream cells; Times burgundy numerals ~28–32px, `tabular-nums`; Baskerville/Times labels 11–12px muted burgundy |
| Heading | `Còn tới ngày cưới` (not “còn tới tiệc”) |
| After `now >= target` on 25/10 | Hide cells; show `Hôm nay là ngày cưới` |
| After `now >= 2026-10-26T00:00:00+07:00` | Same node: `Trân trọng cảm ơn` |
| Overlay / FAB / 24/10 clock | **No** |
| Motion | Numbers only. No cell pulse. Do **not** add countdown to `prefers-reduced-motion` `animation: none` lists. |
| Tick | `setInterval` 1000ms. Optional skip while `document.hidden`. OK to tick under overlay. |
| A11y | One `aria-live="polite"` summary (`Còn 38 ngày 12 giờ`) updated on **day/hour change**, not every second. Visual cells `aria-hidden="true"` if live region exists. |
| Cache | Bump `index.html` `css/invitation.css?v=` and `js/invitation.js?v=` (currently `script26` / `guest10`) |

## Architecture

```
ISO +07 target
  → remaining = target - Date.now()
  → if remaining <= 0:
       hide #countdown-cells
       show #countdown-done
       text = now < 26/10 00:00+07 ? "Hôm nay là ngày cưới" : "Trân trọng cảm ơn"
       clearInterval
  → else:
       days / hours / mins / secs
       pad hours/min/sec 2 digits; days unpadded or 2+
       write textContent on #cd-days … #cd-secs
       if days or hours changed: update #countdown-live
```

No innerHTML for numbers. No new fonts/colors.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Markup and cream 4-cell CSS](./phase-01-markup-and-cream-4-cell-css.md) | Completed |
| 2 | [Tick JS plus DESIGN.md exception](./phase-02-tick-js-plus-design-md-exception.md) | Completed |

Phase 2 depends on phase 1 IDs.

## Files

- Modify: `index.html` — hero markup + cache-bust
- Modify: `css/invitation.css` — `.countdown*` cream row
- Modify: `js/invitation.js` — `startCountdown()` + interval
- Modify: `DESIGN.md` — exception (lede, taste list, DateBlock, motion “No countdown tick”)

## Success criteria

- Opened page: 4 cells tick; overlay unchanged
- Instant at/after 00:00 25/10 +07: cells gone, blessing visible; 26/10+ → “Trân trọng cảm ơn”
- Guest abroad still counts to VN midnight
- No overlap with `.hero-amp` / guest name at 390px
- Ceremony day numeral `25` stays a date, not a timer
- No LED/glow/FAB/second clock

## Out of scope

Overlay countdown, sticky FAB, clock to 24/10 16:00, restoring timeline, new palette/font, pause-tab as a requirement (optional cheap skip only).

## Cook

`/ck:cook C:\Users\ADMIN\hieuvm\wendding-minhieu-phuonganh\plans\260917-1449-hero-wedding-day-countdown\plan.md`

Low risk. Skip red-team/validate unless asked. 2 phases → skip Claude Task hydration.

## Review (2026-09-17)

Code review: [reports/260917-1458-hero-wedding-day-countdown-code-review.md](./reports/260917-1458-hero-wedding-day-countdown-code-review.md) — **8/10**. Locked AC met. No critical. Overlay / `?to=` / ceremony `25` / music / album unchanged.

### Next steps (optional polish, not a rewrite)
- [x] Hide `.countdown-label` when blessing is shown (`js/invitation.js` + `.countdown-label[hidden]`).
- If cream *tiles* are required, add `--ink-cream` fill + hairline on `.countdown-cell` and recheck 390px one-row.
- Browser-check 390px vs `.hero-amp` (static review only).
