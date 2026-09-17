---
phase: 2
title: Wire HTML JS loader
status: completed
priority: P1
dependencies:
  - 1
effort: S
---

# Phase 2: Wire HTML JS loader

## Overview

Trỏ HTML/JS sang WebP 2 cỡ. Preload hero. Album DOM ổn định. Lightbox full chỉ khi mở + prefetch neighbor idle.

## Requirements

- Functional: hero/album/thumbs/lightbox vẫn 7 ảnh, swipe/lightbox/keyboard giữ hành vi hiện tại
- Non-functional: first paint không chờ 7 full; 0 JPEG photo requests; no CSS redesign

## Architecture

**HTML `index.html` `<head>`** (sau CSS link):

```html
<link rel="preload" as="image" href="assets/photos/hero.webp">
```

Hero img (~line 55):

```html
<img src="assets/photos/hero.webp" alt="" width="800" height="1200" fetchpriority="high" decoding="async">
```

(`width`/`height` gần tỉ lệ crop envelope — đo frame CSS nếu cần; mục tiêu chống CLS.)

Lightbox `#lb-img` (~line 355): **bỏ** `src="assets/photos/01.jpg"`. Để không `src`, hoặc `src=""` + `alt=""`. JS set full khi `openLightbox`.

**JS `invitation.js`:**

```js
const PHOTO_IDS = ["01", "02", "03", "04", "05", "06", "07"];
const PHOTOS_CARD = PHOTO_IDS.map((id) => `assets/photos/card/${id}.webp`);
const PHOTOS_FULL = PHOTO_IDS.map((id) => `assets/photos/full/${id}.webp`);
```

Xóa `PHOTOS` JPEG array. Mọi chỗ `PHOTOS.length` → `PHOTO_IDS.length`.

`renderAlbum`:
- Nếu `#album-fan` chưa có `.album-card` (lần đầu): tạo 7 button+img (`src=PHOTOS_CARD[i]`, `decoding="async"`, `loading` = `i===0 ? "eager" : "lazy"`). Click handler đóng closure index.
- Dots: tạo 1 lần; lần sau chỉ toggle `is-active`.
- `applyAlbumTransforms()`: loop existing cards, set transform/opacity/zIndex/boxShadow. **Không** `fan.innerHTML = ""` khi swipe.
- `stepAlbum` / card click (không phải center) gọi `applyAlbumTransforms` thôi.

`buildThumbs`: `PHOTOS_CARD`; `loading="lazy"`.

`renderLb`: `lbImg.src = PHOTOS_FULL[lbIndex]`.

`openLightbox`: `renderLb` rồi `showModal`; `prefetchNeighbor(lbIndex)`.

`prefetchNeighbor(i)`:

```js
function prefetchFull(src) {
  const img = new Image();
  img.src = src;
}
function prefetchNeighbor(i) {
  const n = PHOTO_IDS.length;
  const run = () => {
    prefetchFull(PHOTOS_FULL[(i + 1) % n]);
    prefetchFull(PHOTOS_FULL[(i - 1 + n) % n]);
  };
  if ("requestIdleCallback" in window) requestIdleCallback(run, { timeout: 2000 });
  else setTimeout(run, 200);
}
```

Không prefetch all 7.

Grep bắt buộc: không còn `assets/photos/0` + `.jpg` hoặc `hero.jpg` trong `index.html` / `js/`.

## Related Code Files

- Modify: `index.html`
- Modify: `js/invitation.js`
- Do not modify: `css/invitation.css` unless CLS needs explicit width/height only on img attributes
- Do not touch: audio, QR, guestbook, RSVP

## Implementation Steps

1. Head preload + hero src + fetchpriority/decoding/dimensions.
2. Strip lightbox default src.
3. Replace photo constants; split create vs apply in album.
4. Thumbs card; lightbox full; neighbor prefetch.
5. Grep leftover jpg photo paths.

## Success Criteria

- [x] No `assets/photos/*.jpg` referenced in html/js
- [x] Hero uses `hero.webp` + preload
- [x] Album cards use `card/*.webp`; swipe does not recreate img nodes
- [x] Thumbs use card; `#lb-img` uses full only after open/nav
- [x] Neighbor full prefetch only (idle)
- [x] Existing album/lightbox/keyboard behavior preserved

## Risk Assessment

- Empty `#lb-img` src có thể request page URL — dùng omit attribute, không `src=""`.
- Click listener duplicate nếu `renderAlbum` tạo lại cards — chỉ create khi `fan.childElementCount === 0`.
- `loading=lazy` trên card 0: **không** — card 0 eager.
