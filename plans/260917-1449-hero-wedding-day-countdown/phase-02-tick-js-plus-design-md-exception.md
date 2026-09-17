---
phase: 2
title: Tick JS plus DESIGN.md exception
status: completed
priority: P2
effort: S
dependencies: [1]
---

# Phase 2: Tick JS plus DESIGN.md exception

## Overview

Drive the phase-1 IDs from remaining time to VN wedding-day midnight, swap to blessing after the target, and document the DESIGN.md exception so the day numeral `25` stays a date, not a second clock.

## Requirements

- Functional: live 4-cell tick; pad h/m/s 2 digits; days unpadded or 2+; hide cells at/after target; blessing copy by calendar day +07.
- Non-functional: timezone-safe; no innerHTML; no second-by-second `aria-live`; optional pause when `document.hidden`.

## Architecture

In `js/invitation.js` (IIFE, near other boot):

```
const WEDDING_DAY = Date.parse("2026-10-25T00:00:00+07:00");
const THANKS_DAY  = Date.parse("2026-10-26T00:00:00+07:00");

function pad2(n) { return String(n).padStart(2, "0"); }

function renderCountdown() {
  const now = Date.now();
  const cells = document.getElementById("countdown-cells");
  const done = document.getElementById("countdown-done");
  const live = document.getElementById("countdown-live");
  if (!cells || !done) return false;

  if (now >= WEDDING_DAY) {
    cells.hidden = true;
    done.hidden = false;
    done.textContent = now >= THANKS_DAY
      ? "Trân trọng cảm ơn"
      : "Hôm nay là ngày cưới";
    if (live) live.textContent = done.textContent;
    return false; // stop interval
  }

  let ms = WEDDING_DAY - now;
  const days = Math.floor(ms / 86400000); ms %= 86400000;
  const hours = Math.floor(ms / 3600000); ms %= 3600000;
  const mins = Math.floor(ms / 60000); ms %= 60000;
  const secs = Math.floor(ms / 1000);

  document.getElementById("cd-days").textContent = String(days);
  document.getElementById("cd-hours").textContent = pad2(hours);
  document.getElementById("cd-mins").textContent = pad2(mins);
  document.getElementById("cd-secs").textContent = pad2(secs);

  const summary = `Còn ${days} ngày ${hours} giờ`;
  if (live && live.dataset.summary !== summary) {
    live.dataset.summary = summary;
    live.textContent = summary;
  }
  return true;
}

function startCountdown() {
  if (!renderCountdown()) return;
  const id = setInterval(() => {
    if (document.hidden) return;
    if (!renderCountdown()) clearInterval(id);
  }, 1000);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) renderCountdown();
  });
}

startCountdown();
```

Call at boot (hero is covered by overlay — ticking underneath is OK). Missing nodes → no-op.

**Do not** use `new Date(2026, 9, 25)` (guest local TZ). **Do** use ISO with `+07:00`.

## Related Code Files

- Modify: `js/invitation.js` — countdown helpers + `startCountdown()`
- Modify: `index.html` — bump `js/invitation.js?v=`
- Modify: `DESIGN.md`:
  - Lede L3: drop blanket “No live countdown”; point to hero exception
  - Taste L12: replace “Do not add a countdown clock…” with: ceremony numeral is not a timer; **exception:** cream 4-cell under hero to `00:00 25/10/2026 +07` only
  - DateBlock L179–181: numeral stays static; countdown is a **separate** hero module
  - Motion L255: remove “No countdown tick” or rephrase: no CSS tick animation on the day numeral; JS number updates on hero cells are allowed

## Implementation Steps

1. Add constants + `renderCountdown` / `startCountdown`; `textContent` only.
2. Stop interval after first non-positive remaining.
3. On `visibilitychange` to visible, one extra render (avoids stale seconds after tab sleep).
4. Bump JS cache query.
5. Patch the four DESIGN.md spots; do not re-introduce a global ban.

## Success Criteria

- [x] Before target: cells tick every 1s; overlay still open-invite only (`startCountdown` + overlay unchanged)
- [x] `Date.parse('2026-10-25T00:00:00+07:00')` is the only target (`js/invitation.js:59`)
- [x] At/after that instant: cells + label `hidden`, blessing shown (`js/invitation.js` post-target branch)
- [x] At/after 26/10 00:00 +07: “Trân trọng cảm ơn” (`THANKS_DAY` `:60`, `:76-77`)
- [x] `aria-live` updates on day/hour change only (`live.dataset.summary` `:97-101`)
- [x] `prefers-reduced-motion` does not freeze/hide the numbers (reduce block does not target `.countdown*`)
- [x] DESIGN.md exception explicit; ceremony `25` still “not a timer”
- [x] JS cache query bumped (`index.html:423` `?v=countdown1`)

## Risk Assessment

Wrong TZ → clock “off” vs trai 16:00 24/10. Mitigation: copy “ngày cưới” + ISO +07. Loud AT: don’t live-announce seconds. Tab throttle: `hidden` skip + render on visible.
