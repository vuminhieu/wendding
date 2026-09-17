---
title: Brainstorm — guest name via URL (?to=)
status: approved
created: 2026-09-17
project: wendding-minhieu-phuonganh
---

# Guest name on invitation via `?to=`

## Problem statement

Generic overlay says "Thân Mời" only. Couple wants per-guest feel when sending Zalo/FB links. Site is static HTML/CSS/JS. No backend, no guest list. Existing query: `?open=1` only.

## Problem-first

1. **Solution-jumping:** User proposed "type name in URL, show under Thân Mời". Signal: invitation feels impersonal.
2. **Underlying problem:** Guest should see their name on first screen and again inside the card, without a CMS.
3. **Assumptions:** Couple will copy/paste unique URLs; guests won't mind editable names; XSS from query is handled by textContent.
4. **Problem:** Static invite cannot address a guest by name. Cost: less personal Zalo send. Success: named overlay + named line under couple names; guestbook prefilled.
5. **Frames:** A) free `?to=` text (chosen). B) slug map JSON. C) hash `#name` (worse share).
6. **Evidence:** Weak (couple preference). Cheap enough to ship.
7. **Validation:** Open `?to=Đạt và Người Thương`, overlay + hero line, guestbook input, `?open=1` keeps `to`, empty `to` hides lines.
8. **Stakeholder:** Build URL param personalize; skip guest DB.

## Requirements (approved)

| Item | Decision |
|------|----------|
| URL | `?to=Đạt và Người Thương` free text |
| Overlay | Keep "Thân Mời"; name line below; then Open button |
| Inside card | Small line under Minh Hiếu & Phương Anh: `Kính mời {name}` |
| Guestbook | Prefill `#wish-name` |
| Footer | Unchanged |
| Missing/invalid `to` | Hide name lines; default invite |
| `?open=1` | Preserve `to` on replaceState |
| Out of scope | Guest list, copy-link helper, slug map, backend |

## Approach

Read `URLSearchParams` (already in `js/invitation.js`). Sanitize: trim, max 80 chars, strip controls, set via `textContent` never innerHTML. Empty after sanitize → no-op.

Touchpoints: `index.html` (placeholders), `css/invitation.css` (overlay + hero line), `js/invitation.js` (parse, render, keep `to` on open).

## Risks

- Anyone can change `to` in URL — OK for wedding card.
- Zalo may encode poorly — couple should send encoded link.
- Long names wrap overlay card — CSS wrap + max 80.

## Success

- `index.html?to=Đạt%20và%20Người%20Thương` shows name on overlay and under couple names.
- No `to` looks like current design.
- Guestbook name filled.
- No XSS if `to=<script>`.

## Next

`/ck:plan` (default) — small UI + JS, no TDD suite in repo.
