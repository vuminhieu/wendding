---
phase: 2
title: Parse and apply ?to=
status: completed
priority: P2
dependencies:
  - 1
---

# Phase 2: Parse and apply ?to=

## Overview

Read `to` from the existing `URLSearchParams`, sanitize, fill overlay/hero/guestbook. Do not drop `to` when opening the envelope.

## Requirements

- Functional: valid name → show overlay + hero `Kính mời {name}` + prefill `#wish-name`.
- Invalid → leave nodes hidden, guestbook empty.
- `openInvite` keeps `to` (already true; do not `searchParams.delete`).
- Non-functional: no innerHTML; max 80 chars.

## Architecture

Add after `const alreadyOpen = ...` (~L31):

```js
const MAX_GUEST_NAME = 80;

function sanitizeGuestName(raw) {
  if (raw == null) return "";
  const name = String(raw)
    .replace(/[\u0000-\u001F\u007F]/g, "")
    .replace(/\s+/g, " ")
    .trim();
  if (!name) return "";
  return name.length > MAX_GUEST_NAME ? name.slice(0, MAX_GUEST_NAME).trim() : name;
}

function applyGuestName(name) {
  if (!name) return;
  const overlayGuest = document.getElementById("overlay-guest");
  const heroGuest = document.getElementById("hero-guest");
  const wishName = document.getElementById("wish-name");
  overlayGuest.textContent = name;
  overlayGuest.hidden = false;
  heroGuest.textContent = "Kính mời " + name;
  heroGuest.hidden = false;
  if (wishName && !wishName.value) wishName.value = name;
}

applyGuestName(sanitizeGuestName(params.get("to")));
```

`params` already exists. Call `applyGuestName` on load regardless of `alreadyOpen` so `?open=1&to=X` still fills hero + guestbook.

Wish form `reset()` after submit clears name — OK (user already sent). Do not re-apply after reset.

`openInvite` L89–91: leave as-is (`url.searchParams.set("open", "1")` preserves other params).

## Related Code Files

- Modify: `js/invitation.js`

## Implementation Steps

1. Add `sanitizeGuestName` + `applyGuestName` + one call at init.
2. Confirm `openInvite` does not delete `to`.
3. Manual checks (no test runner):
   - `index.html?to=Đạt%20và%20Người%20Thương`
   - `index.html` (no param)
   - `index.html?to=`
   - `index.html?to=%20%20`
   - `index.html?to=<script>alert(1)</script>`
   - `index.html?open=1&to=Lan`
   - name ~80+ chars
   - click Mở thiệp → address bar still has `to`

## Success Criteria

- [x] Valid `to` fills overlay, hero (`Kính mời …`), guestbook
- [x] Empty/missing/whitespace-only: hidden lines, empty guestbook
- [x] Script string is text, not executed
- [x] `open=1` + `to` skips overlay animation (existing) but still personalizes card
- [x] After Mở thiệp, `to` remains in URL

## Risk Assessment

Zalo may double-encode Vietnamese — couple should paste a working encoded URL once. Truncate at 80 may cut mid-grapheme; acceptable for wedding names. `wishName && !wishName.value` avoids overwriting if user typed before JS (script is deferred at end of body — race is negligible).
