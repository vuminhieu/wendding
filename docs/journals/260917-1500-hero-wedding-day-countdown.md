---
date: 2026-09-17
session: hero-wedding-day-countdown
---

# Journal: 2026-09-17 — Hero wedding-day countdown

## Context

Static invite. Need a live 4-cell countdown under the names (after `#hero-invite`) to `2026-10-25T00:00:00+07:00`. DESIGN.md forbids extra hero chrome; this is an explicit exception.

## What Happened

- Cream 4-cell countdown: ngày / giờ / phút / giây. JS tick 1s. Target is ISO `+07` only — no `Date.UTC` / `getTimezoneOffset` math.
- After midnight 25/10: hide cells + label, show blessing. 26/10: thanks copy.
- Cache-bust `?v=countdown1`.
- Reviewer 8/10 (not a full pass). Tester 16/16 PASS, no browser.

## Decisions Made

| Decision | Rationale | Impact |
|----------|-----------|--------|
| ISO `+07` only | Wedding is Vietnam local; offset math is a timezone footgun | Tick is deterministic vs the ceremony clock |
| Hide cells after midnight, don’t zero them | Zeroed 00:00:00:00 still looks like a timer | Blessing / thanks replace the widget |
| DESIGN.md exception, not a redesign | Hero stays name-first | Countdown sits under names, not in the overlay |

## Risks / leftover

- Review 8/10 — follow remaining comments before calling it done.
- No browser QA. Optional: cream tiles + 390px visual check.

## Next Steps

- Visual pass at 390px (tile color, wrap, label).
- Re-review the 2/10 gap if comments are still open.
