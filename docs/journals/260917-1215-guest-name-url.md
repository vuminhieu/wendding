---
date: 2026-09-17
session: guest-name-url
---

# Journal: 2026-09-17 — Guest name via `?to=`

## Context

Static wedding invite. Guest personalization from URL only — no backend, no slug map, no copy helper. Plan: `plans/260917-1203-guest-name-url/` (completed). Brainstorm locked the surface.

## What Happened

- Locked: free-text `?to=`, overlay “Thân Mời” + name, hero “Kính mời {name}”, prefill `#wish-name`.
- Phase 1: placeholders `#overlay-guest` / `#hero-guest`; CSS `:has()` spacing + `.hero-guest`.
- Phase 2: `sanitizeGuestName` (80 chars, strip C0, collapse ws) + `applyGuestName` via `textContent`. `openInvite` keeps `to`. Cache-bust `?v=guest1`.
- Reviewer 8/8 PASS. Tester 6/6 PASS.
- Plan YAML already completed via `ck plan check`. No architecture docs to update.

## Decisions Made

| Decision | Rationale | Impact |
|----------|-----------|--------|
| Truncate over 80, don’t hide | Over-long names still personalize | Overflow clipped, UI still shows a name |
| Do not prefill RSVP `#rsvp-name` | Guestbook only | RSVP stays empty |
| Footer unchanged | Out of scope | No extra personalization there |

## Next Steps

- Visual check in browser (overlay + hero + guestbook).
- Confirm Zalo/FB encoding of Vietnamese `?to=` still round-trips.
