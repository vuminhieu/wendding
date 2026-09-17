---
title: PM — hero wedding-day countdown
status: completed
created: 2026-09-17
---

# PM — hero wedding-day countdown

| Field | Value |
|-------|--------|
| Plan | `plans/260917-1449-hero-wedding-day-countdown` |
| Status | completed (both phases) |
| Review | 8/10 — no critical |
| QA | 16/16 checkable PASS; browser SKIPPED |

## Delivered

Hero 4-cell countdown after `#hero-invite` → `2026-10-25T00:00:00+07:00`. After midnight: hide cells + label; blessing. 26/10+: “Trân trọng cảm ơn”. DESIGN.md exception. Cache `?v=countdown1`.

## Verification

- Code review: `reports/260917-1458-hero-wedding-day-countdown-code-review.md`
- QA: `plans/reports/260917-1456-wedding-countdown-qa.md`
- Post-review: hide `.countdown-label` on done
- `node --check js/invitation.js` OK
- Overlay / `?to=` / ceremony `25` / music / album unchanged

## Docs

No `./docs` product set (only journals). DESIGN.md is the design contract — updated.

## Remaining optional

Cream tiles; 390px browser check vs `.hero-amp`.
