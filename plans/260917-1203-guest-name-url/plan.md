---
title: Guest name via URL (?to=)
description: >-
  Static invite reads ?to= and shows the guest name under overlay “Thân Mời” and
  as “Kính mời {name}” under hero couple names; prefill guestbook.
status: completed
priority: P2
branch: main
tags:
  - frontend
  - invitation
blockedBy: []
blocks: []
created: '2026-09-17T05:04:25.822Z'
createdBy: 'ck:plan'
source: skill
---

# Guest name via URL (?to=)

## Overview

Thiệp tĩnh. Khách mở link Zalo/FB với `?to=Đạt và Người Thương`. Overlay giữ “Thân Mời”, thêm tên ngay dưới. Trong thiệp: dòng `Kính mời {name}` dưới Minh Hiếu & Phương Anh. Prefill `#wish-name`. Không backend, không slug map, không helper copy.

Brainstorm: `plans/reports/260917-1201-guest-name-url.md`. Photo-load plan completed — không overlap.

`openInvite()` đã `replaceState` set `open=1` trên `URL` hiện tại — `to` giữ nguyên nếu không xóa. Sanitize + DOM fill là việc mới.

## Locked decisions

| Item | Value |
|------|--------|
| Param | `to` (free text) |
| Overlay | “Thân Mời” + name line; name node hidden until valid |
| Hero | `Kính mời {name}` under `.hero-names` |
| Guestbook | `#wish-name` value = name |
| RSVP `#rsvp-name` | không đụng |
| Footer | không đụng |
| Invalid/empty/missing | hide both lines; default invite |
| XSS | `textContent` / input `.value` only |
| Max | 80 chars after trim; strip C0 controls |
| `?open=1` | keep `to` (current `openInvite` already does) |

## Architecture

```
location.search
  → URLSearchParams.get("to")
  → sanitizeGuestName()
  → if name:
       overlayGuest.textContent = name; hidden=false
       heroGuest.textContent = "Kính mời " + name; hidden=false
       wishName.value = name
     else:
       both nodes stay hidden
```

No innerHTML. Decode is native (`URLSearchParams`).

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [HTML+CSS placeholders](./phase-01-html-css-placeholders.md) | Completed |
| 2 | [Parse and apply ?to=](./phase-02-parse-and-apply-to.md) | Completed |

Phase 2 depends on phase 1 IDs.

## Files

- Modify: `index.html` — overlay + hero nodes; CSS cache-bust
- Modify: `css/invitation.css` — `.overlay-guest`, `.hero-guest`
- Modify: `js/invitation.js` — sanitize + apply; do not drop `to` in `openInvite`

## Success criteria

- `?to=Đạt%20và%20Người%20Thương` → overlay name + hero `Kính mời Đạt và Người Thương` + guestbook filled
- no `to` / `to=` / whitespace → UI như hiện tại; over 80 chars after trim → truncate (not hide)
- `?to=<script>alert(1)</script>` → text, no execute
- `?to=X&open=1` → overlay skipped (existing), names still in card + guestbook
- `openInvite` URL still has `to`

## Out of scope

Guest list, copy-link UI, RSVP prefill, footer repeat, backend.

## Cook

`/ck:cook C:\Users\ADMIN\hieuvm\wendding-minhieu-phuonganh\plans\260917-1203-guest-name-url\plan.md`

Low risk. Skip red-team/validate unless user wants.
