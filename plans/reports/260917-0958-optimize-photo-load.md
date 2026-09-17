---
title: Optimize wedding photo load
status: agreed
created: 2026-09-17
topic: image-performance
modes: []
approach: A
---

# Optimize wedding photo load

## Summary

Khách 4G load ảnh thiệp rất lâu vì `assets/photos/` đang serve JPEG camera (~80MB cho 8 ảnh dùng). Không phải CSS theme. Hướng A: 2 cỡ WebP + sửa loader HTML/JS. Không CDN. Không nén nhạc.

## Problem-first

### 1. Solution-jumping diagnosis

User hỏi "tối ưu load ảnh cho đẹp hơn" — cảm giác cần hiệu ứng/CSS. Pain thật: byte + decode + JS rebuild.

### 2. Underlying problem

Trình duyệt phải tải + decode JPEG full-res cho card ~200px và lightbox chưa mở.

### 3. Assumption challenges

| Assumption | Risk if wrong | Validation |
|------------|---------------|------------|
| WebP q80 gần như gốc trên phone | Grain/váy hơi mềm | So sánh hero + 03.jpg trên 390px |
| Pillow/`sharp` đủ, không cần magick | Script fail | Chạy 1 ảnh thử trước batch |
| Album giữ DOM hết flicker | Cache browser vẫn re-decode nếu src đổi | Giữ cùng src card; chỉ transform |
| NTD*.jpg không cần | User muốn thêm album sau | Không xóa; không serve |

### 4. Problem statement

- Users: khách mời 4G/Wi-Fi yếu, chủ yếu điện thoại.
- Struggle: envelope/album/lightbox trắng lâu, fan giật khi swipe.
- Cause: `hero.jpg` 10MB; `01–07.jpg` ~72MB (`03.jpg` 36MB). Lightbox `#lb-img` `src=01.jpg` lúc parse. `buildThumbs` + `renderAlbum` gắn full JPG; mỗi swipe `innerHTML=""` tạo lại 7 img.
- Consequence: first paint chậm, decode block main thread, tốn data.
- Success: hero hiện <1s 4G tốt; album card hiện trước khi cuới tới; lightbox mở <500ms nếu đã prefetch; nhìn gần gốc trên phone.

### 5. Alternative framings

- Frame A (chosen): bytes + loader — 2 cỡ WebP + HTML/JS.
- Frame B: 1 WebP ~1200px — ít file, album vẫn nặng hơn cần.
- Frame C: chỉ recompress JPEG — lightbox/thumb vẫn kéo 11MB lúc load.

### 6. Evidence status

Strong (file size trên disk + code path).

### 7. Validation plan

- Network: hero WebP <200KB; 7 card <150KB/ảnh; 7 full <400KB/ảnh.
- Visual: hero envelope + album + lightbox `03` không vỡ rõ trên 390–430px.
- Behavior: swipe album không tạo request mới cho card đã hiện; lightbox không request full cho đến khi mở (hoặc prefetch sau idle).
- Kill: nếu q80 vẫn xấu → hạ resize, không tăng q lên 95 (file phình).

### 8. Stakeholder message

Chậm vì ảnh gốc 10–36MB/file. Nén 2 cỡ WebP + không load full lúc mở trang. Gốc camera giữ `originals/`. QR/STK/nhạc không đụng.

## Requirements (exact)

- Expected output: WebP card/full (+ hero); `scripts/optimize-photos.py` hoặc `.mjs`; sửa `index.html` + `js/invitation.js`.
- Acceptance: targets KB ở trên; hero `fetchpriority=high` + preload; album `loading=lazy` (ảnh 2+); lightbox empty/`src` card đến khi open; album DOM ổn định.
- Out of scope: CDN, nén mp3, Maps, NTD*.jpg vào album, visual-diff vs chungdoi.
- Constraints: vanilla; no hotlink (DESIGN.md); no ImageMagick on PATH — Python Pillow hoặc npx sharp; Windows.
- Touchpoints: `assets/photos/`, `index.html`, `js/invitation.js`, new `scripts/`.

## Chosen approach A

### Asset layout

```
assets/photos/originals/   # move camera JPG here; gitkeep; optional git-lfs later
assets/photos/card/        # 01.webp … 07.webp  max edge 800, webp q80
assets/photos/full/        # 01.webp … 07.webp  max edge 1600, webp q80
assets/photos/hero.webp    # max edge 1600, q80
```

JPEG gốc hiện tại move vào `originals/` (kể cả NTD*). Runtime không reference `.jpg`.

### HTML

- `<link rel="preload" as="image" href="assets/photos/hero.webp">`
- Hero `<img src="assets/photos/hero.webp" fetchpriority="high" decoding="async" width height>`
- `#lb-img` không `src` full lúc load (placeholder rỗng hoặc card[0])
- Không preload 7 full

### JS

- `PHOTOS_CARD` / `PHOTOS_FULL` arrays
- `renderAlbum` **một lần**: 7 card img; swipe chỉ đổi transform/opacity/z-index
- `buildThumbs` dùng card
- `openLightbox` set `full` src; optional `requestIdleCallback` prefetch full kế bên
- `decoding="async"` trên album img

### Script

- One-shot `scripts/optimize-photos.py` (Pillow) hoặc `scripts/optimize-photos.mjs` (sharp)
- Prefer Python nếu `pip install pillow` ok; else `npx --yes sharp-cli` / small mjs + sharp
- Idempotent; skip if dest newer
- Print before/after KB

### JPEG fallback

Không bắt buộc round này. Safari iOS 14+ WebP ok. Nếu cần sau: `<picture>` + jpeg sibling.

## Risks

- Pillow chưa cài → cài user-local hoặc chuyển sharp
- `03.jpg` 36MB decode lúc optimize chậm trên máy dev — chấp nhận
- Git repo phình nếu commit cả originals + webp — originals nên `.gitignore` hoặc LFS; **serve chỉ webp**
- Album aspect 2:3 crop `object-fit:cover` — resize theo short edge, không letterbox

## Success metrics

| Check | Target |
|-------|--------|
| hero.webp | <200KB |
| each card | <150KB |
| each full | <400KB |
| first hero paint | không chờ album |
| swipe | 0 new card requests after first album paint |
| lightbox open | 1 full request (or cache) |

## Next

`/ck:plan` (default) — feature mới, không có test suite. Không `--tdd`.

## Decisions locked

- `assets/photos/originals/` gitignored. Commit WebP + `scripts/optimize-photos.*` only.
- Prefetch lightbox full: neighbors only (idle), not all 7.
- Next: `/ck:plan` (default, not `--tdd`).

## Unresolved

- None for this round.
