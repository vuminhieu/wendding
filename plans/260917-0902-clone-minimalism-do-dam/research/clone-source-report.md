---
title: Clone Minimalism Đỏ Đậm — source synthesis
status: completed
created: 2026-09-17
---

# Research Report: Clone Minimalism Đỏ Đậm

**Conducted:** 2026-09-17 09:02  
**Source:** live dumps + `DESIGN.md` + `reports/extract.json`  
**URL:** https://chungdoi.com/vi/mau-thiep/minimalism-do-dam/demo

## Executive Summary

Project already extracted live DOM/CSS. No more web research needed. Clone is vanilla HTML/CSS/JS matching opened invitation (`?open=1`) plus closed envelope overlay.

Authoritative: opened live HTML in `assets/research/_extracted/pretty/`. `DESIGN.md` tokens are correct except dress swatches (live = circles, not squares) and Đón khách on banquet card (live `17:30`, extract.json `17:00`). Timeline keeps `17:00`. Do not ship Maps API key from dump.

## Research Methodology

- Sources: DESIGN.md, extract.json, 14 section dumps, local assets
- Date: 2026-09-16 extract → 2026-09-17 clone
- Terms: paper multiply, envelope overlay, Viaoda Libre, ienvHintPulse

## Key Findings

### 1. Page stack (14 invitation children)

1. Overlay (closed) → 2. Header → 3. Ceremony paper → 4. Album → 5. Banquet paper → 6. Venue/map → 7. Dress → 8. Timeline → 9. Guestbook → 10. Gift → 11. Footer → 12. Brand → music FAB + dialogs

### 2. Material

Cream `#FFF7EB` sheet on dark chrome. Paper = `#511419` + `paper.webp` opacity 0.4 multiply + `4px 4px 10px rgba(0,0,0,0.25)`. Boards 560px, not full 900.

### 3. Type (7 faces)

Cormorant Garamond, Viaoda Libre, The Nautigal, Ms Madi, Times, Baskerville, Uchen. Overlay also Lora. Ban Pattaya/Roboto.

### 4. Security / assets

- Map: `output=embed` query URL. No AIza key.
- Audio/photos/theme: local `assets/`.
- Gift QR: local `assets/qr/`. Demo bank names stay as dumped (TRAN TUAN KIET / LE MINH ANH) until couple data swap.

### 5. Motion

`drFloat`, `ambient-fall`, `seal-pulse`, `shine`, `ienvHintPulse`, `animate-spin-cd`, sparkles. Hover scale 1.03–1.10. Reduced-motion: no loops.

## Implementation Recommendations

Ship `index.html` + `css/invitation.css` + `js/invitation.js`. Open via `?open=1` or “Mở thiệp”. Guestbook/RSVP = localStorage. Album = 7 local photos, 3D fan + lightbox.

## Common Pitfalls

- Using extract.json 17:00 on banquet card (wrong; live 17:30)
- Square dress swatches (live circles)
- Hotlinking CDN / Maps key
- Pattaya/Roboto
- Countdown clock on `03`

## Unresolved

- Couple real bank/QR vs demo
- Couple names vs dump (Hoàng Long / Bảo Ngọc)
- Exact envelope-open keyframes (46 recorded; clone uses opacity/transform exit)

## Next

Open `index.html`. Visual-diff vs live demo at 900px.