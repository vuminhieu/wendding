---
title: PM — optimize photo load
status: completed
created: 2026-09-17
---

# PM — optimize photo load

Plan `plans/260917-1000-optimize-photo-load/` 3/3 done.

| Check | Result |
|-------|--------|
| hero.webp | 36.2KB |
| card max | 48.4KB (05) |
| full max | 140.2KB (05) |
| JPEG at photos root | gone (git D) |
| originals gitignored | yes |
| HTTP 8765 webp | 200 |
| HTTP hero.jpg | 404 |
| Pillow bomb | MAX_IMAGE_PIXELS=300M |
| script re-run | SKIP all |

Reviewer FAIL: accidental `.brand` delete — restored. HTML diff now only preload/hero/lb-img.

No `docs/` to update.

Unresolved: user visual on 390px live; commit WebP not originals.
