---
phase: 3
title: Verify load targets
status: completed
priority: P1
dependencies:
  - 2
effort: S
---

# Phase 3: Verify load targets

## Overview

Đo file size + network trên `http://127.0.0.1:8765/` (và `?open=1`). Soát visual hero/album/lightbox `03`. Không viết test suite.

## Requirements

- Functional: overlay → mở thiệp → album swipe → lightbox 03 → thumbs
- Non-functional: KB targets; hero không chờ album; swipe 0 new card requests

## Architecture

Manual verification, no Playwright.

Network (DevTools, Disable cache, Fast 3G optional):

| Request | When | Max |
|---------|------|-----|
| `hero.webp` | document parse | <200KB, high priority |
| `card/01.webp` | album in DOM | <150KB |
| `card/02–07.webp` | lazy / near | <150KB each |
| `full/*.webp` | lightbox open or idle neighbor | <400KB each |
| `*.jpg` photos | never | 0 |

Không assert audio.

Visual (phone width ~390):

- Envelope hero: mặt không vỡ block, crop cover giống cũ
- Album fan: cover 2:3 ok
- Lightbox `03` (file gốc nặng nhất): da/váy chấp nhận được vs JPEG; nếu xấu rõ → rerun script q/edge per phase 1 retry rules, **không** bump q lên 95

## Related Code Files

- Modify: only if verify fails (script quality loop or leftover jpg)
- Do not add test files

## Implementation Steps

1. `Get-ChildItem` sizes: hero, card, full — so với target; paste table vào phase notes nếu lệch.
2. Serve repo (`python -m http.server 8765` nếu chưa chạy).
3. Cold load `/` : hero request present; no full webp; no jpg photos.
4. `/?open=1`: album cards appear; swipe 6 lần — Network filter `card` = 7 unique, no repeat after cached.
5. Open lightbox from center card: 1 `full/0N.webp`. Next/prev: neighbor (may already be prefetch).
6. Visual check hero + 03 lightbox.
7. Grep repo html/js: `photos/.*\.jpg` must be empty (except script/docs/originals path strings in py/gitignore).

## Success Criteria

- [x] All KB targets hold on disk
- [x] Cold load: hero webp + no photo jpeg + no full until lightbox (except idle neighbor after album)
- [x] Swipe does not rebuild album img DOM (spot-check: same node in Elements)
- [x] Lightbox 03 visually acceptable
- [x] Server 200 for new webp paths

## Risk Assessment

- Idle prefetch có thể kéo 2 full sớm — chấp nhận; không prefetch 7
- Cached reload che regression — luôn Disable cache khi đo
- Local 127.0.0.1 không mô phỏng 4G thật; KB + request timing là proxy
