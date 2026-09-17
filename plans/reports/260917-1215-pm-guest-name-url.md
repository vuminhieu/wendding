---
title: PM — guest name via URL
status: completed
created: 2026-09-17
---

# PM — guest name via URL

Plan `plans/260917-1203-guest-name-url/` 2/2 done.

| Check | Result |
|-------|--------|
| Overlay `#overlay-guest` | hidden default; textContent from `to` |
| Hero `#hero-guest` | `Kính mời {name}` sibling of `.hero-names` |
| Guestbook `#wish-name` | prefilled |
| RSVP / footer | untouched |
| XSS | textContent + .value |
| Max | truncate 80 |
| Reviewer | 8/8 PASS |
| Tester | 6/6 PASS |
| docs/ | none; journal `docs/journals/260917-1215-guest-name-url.md` |

Unresolved: visual on phone/Zalo encode; user commit.
