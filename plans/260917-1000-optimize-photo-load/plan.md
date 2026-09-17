---
title: Optimize wedding photo load
description: >-
  2-size WebP pipeline + HTML/JS loader so 4G guests do not download 80MB of
  camera JPEGs.
status: completed
priority: P1
branch: main
tags:
  - frontend
  - assets
  - performance
blockedBy: []
blocks: []
created: '2026-09-17T03:01:04.673Z'
createdBy: 'ck:plan'
source: skill
---

# Optimize wedding photo load

## Overview

Thiệp vanilla đang serve JPEG camera: `hero.jpg` ~10MB, `01–07.jpg` ~72MB (`03.jpg` 36MB). Lightbox `#lb-img` gắn `01.jpg` lúc parse. `renderAlbum()` rebuild 7 `<img>` full-res mỗi swipe. Theme `.webp` đã nhẹ; nhạc `em-dong-y-i-do.mp3` 5.39MB **không** đụng round này.

Approach A (locked, `plans/reports/260917-0958-optimize-photo-load.md`): 2 cỡ WebP q80 + sửa loader. Gốc camera gitignore. Không CDN, không JPEG fallback, không TDD.

Python 3.14 + Pillow 12.2.0 đã có trên máy.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Optimize photos script](./phase-01-optimize-photos-script.md) | Completed |
| 2 | [Wire HTML JS loader](./phase-02-wire-html-js-loader.md) | Completed |
| 3 | [Verify load targets](./phase-03-verify-load-targets.md) | Completed |

## Dependencies

- Design: [../reports/260917-0958-optimize-photo-load.md](../reports/260917-0958-optimize-photo-load.md)
- Clone research (ảnh gốc / CSS tokens): [../260917-0902-clone-minimalism-do-dam/research/clone-source-report.md](../260917-0902-clone-minimalism-do-dam/research/clone-source-report.md)
- Runtime: `index.html`, `js/invitation.js`, `css/invitation.css` (album `object-fit: cover` — **không** đổi CSS trừ khi verify bắt buộc)
- Tools: Pillow (primary). Không ImageMagick/`cwebp` trên PATH.

## Success Criteria

- `hero.webp` <200KB; mỗi `card/*.webp` <150KB; mỗi `full/*.webp` <400KB
- Hero preload + `fetchpriority=high`; album card lazy (ảnh 2+)
- Lightbox không request full cho đến khi mở; idle prefetch neighbor only
- `renderAlbum` tạo DOM 1 lần; swipe chỉ đổi transform
- Runtime 0 reference `.jpg` trong `assets/photos/`
- `originals/` gitignored; WebP + script committed
- Visual: hero envelope + album + lightbox `03` chấp nhận được trên ~390px

## Out of scope

- Nén `assets/audio/em-dong-y-i-do.mp3`
- CDN / hotlink (DESIGN.md)
- Maps API, QR/STK, copy thiệp
- `NTD*.jpg` vào album (chỉ move originals, không serve)
- JPEG fallback `<picture>`
- Visual-diff vs chungdoi
- Tests / Playwright

## NOT in this plan

- Git LFS
- Responsive `srcset` 3+ breakpoints
- Prefetch all 7 full on idle
