---
title: QA — guest name via ?to=
status: completed
created: 2026-09-17
scope: index.html, css/invitation.css, js/invitation.js
method: file-level + extracted Node logic (no product test runner)
---

# Test Report — 260917-1211 — guest name `?to=`

Static wedding site. No `package.json` tests. Product files **not** changed.

## Test Results Overview

- **Total**: 51 Node assertions + 6 must-confirm checks
- **Passed**: 51 / 51 Node | 6 / 6 must-confirm
- **Failed**: 0
- **Skipped**: browser/visual (out of requested scope)
- **Duration**: ~1s syntax + logic
- **Verdict**: **PASS**

## Must-confirm matrix

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | `#overlay-guest` + `#hero-guest` exist, hidden default | **PASS** | `index.html` L45, L80: empty `<p … hidden></p>` |
| 2 | `sanitizeGuestName` + `applyGuestName` match plan | **PASS** | `textContent`; max 80; strip C0/`DEL`; collapse `\s+`; trim |
| 3 | `applyGuestName` before `alreadyOpen` overlay hide | **PASS** | call L56; `if (alreadyOpen)` L439 |
| 4 | `openInvite` uses `URL` + `set("open","1")`, no delete `to` | **PASS** | L114–116; no `searchParams.delete` |
| 5 | CSS `:has()` overlay spacing; hero-guest sibling after names | **PASS** | CSS L1772–1774; HTML L75–80 not inside `.hero-names` |
| 6 | No RSVP prefill | **PASS** | `applyGuestName` never touches `#rsvp-name` |

## Coverage Metrics

No Istanbul/c8. Static site.

| Area | Covered by this run | Notes |
|------|---------------------|-------|
| Sanitize | yes | 15 cases incl. 80/81, controls, XSS string |
| Apply | yes | mock DOM; empty noop; unhide; guestbook; RSVP |
| Init order | yes | source index compare |
| openInvite URL | yes | extract + `URLSearchParams.set` sim |
| Markup/CSS | yes | regex + sibling slice |

**Line/branch %**: N/A (no runner). Guest-name path fully inspected.

## Failed Tests

None (after harness fix). Two first-run fails were **test bugs**, not product:

1. `sanitize:collapse-ws` used `"Đạt và\nNgười"` — `\n` is C0 (`\u0000-\u001F`), stripped **before** `\s+` collapse → `"Đạt vàNgười"`. Plan order: strip controls then collapse remaining whitespace. Re-ran with spaces-only collapse; added explicit newline case.
2. `html:hero-after-names-not-inside` regex `[\s\S]*?` was greedy across later `</div>`. Manual sibling check: `.hero-guest` is after `.hero-names`, not inside.

## Node case results (51/51)

Sanitize: null/undefined/empty/spaces/tabs → `""`. Collapse multiple spaces. Strip `\u0000\u0007\u007F`. Keep `<script>…` as text. Keep Vietnamese. 80 keep / 81 slice+trim. `"a"*79+" b"` → 79 `a` (slice then trim). `123` → `"123"`. Newline C0 → concat without space.

Query: missing / `to=` / `%20%20` empty. Encoded `Đạt và Người Thương` OK. `open=1&to=Lan` and reverse OK.

Apply: empty leaves hidden. `Lan` → overlay `Lan`, hero `Kính mời Lan`, unhide. Guestbook `#wish-name` = `Lan`. `#rsvp-name` stays `""`. XSS via `textContent`. Existing wish value not overwritten. Missing `#wish-name` does not throw.

URL sim: `?to=Lan` + set open → `?to=Lan&open=1`. Existing `open=1&to=…` keeps `to`.

## Requirement detail

### 1. Markup hidden by default

```html
<p class="overlay-guest" id="overlay-guest" hidden></p>  <!-- after Thân Mời -->
<p class="hero-guest" id="hero-guest" hidden></p>        <!-- after .hero-names -->
```

Empty. `hidden` attribute. Overlay sibling between invite copy and `#open-invite`.

### 2. Sanitize / apply vs plan

Matches `phase-02` snippet:

- `raw == null` → `""`
- strip `[\u0000-\u001F\u007F]`
- `\s+` → single space, then `trim`
- empty after trim → `""` (nodes stay hidden)
- else cap `MAX_GUEST_NAME = 80` + trim
- apply: `textContent` only; hero prefix `"Kính mời "`
- guestbook: `if (wishName && !wishName.value) wishName.value = name`

**Plan also prefill guestbook** (`#wish-name`). User check was **No RSVP prefill** — distinct. RSVP untouched. Guestbook prefill **present and intended**.

### 3. Order vs `alreadyOpen`

`applyGuestName(sanitizeGuestName(params.get("to")))` at L56, immediately after fn defs. Overlay hide at L439–443. So `?open=1&to=X` still fills overlay node + hero (overlay then hidden). Matches “open=1&to= still personalizes”.

### 4. `openInvite`

```js
const url = new URL(location.href);
url.searchParams.set("open", "1");
history.replaceState({}, "", url);
```

`set` does not drop other params. No `delete("to")` in file.

### 5. CSS / hero placement

- `.overlay-invite { margin-bottom: 24px }` default gap
- `:has(+ .overlay-guest:not([hidden])) { margin-bottom: 0 }`
- `.overlay-guest { margin: 8px 0 24px; font 16px; burgundy 0.88; word-break }`
- `.hero-guest` wrap + overlay font; sibling of `.hero-names` (amp overlay stays)

`:has()` as planned. Cache bust `?v=guest1` on CSS+JS.

### 6. No RSVP prefill

`applyGuestName` IDs: overlay-guest, hero-guest, wish-name only. RSVP submit still reads `#rsvp-name` independently. HTML `rsvp-name` has no `value=`.

## Performance Metrics

- `node --check js/invitation.js`: OK
- Logic script: <1s
- Slow tests: none

## Build Status

- **Build**: N/A (static HTML/CSS/JS)
- **package.json tests**: none
- **Syntax**: PASS (`node --check`)
- **Product files**: unmodified

## Critical Issues

None blocking.

## Gaps (non-blocking)

1. **Newline in `to`**: `\n` stripped, not turned into space (`A\nB` → `AB`). Spec-accurate; odd if a messenger injects `%0A`.
2. **80-char mid-grapheme**: plan accepted.
3. **No browser proof**: overlay `:has()` gap, wrap, `open=1` skip animation not visually run.
4. **Guestbook vs RSVP**: cook/plan fill `#wish-name`; RSVP empty. Confirm product intent if later copy said “no prefill” for both.
5. **No unit tests in repo**: verification is this one-off Node extract.

## Recommendations

1. **Low** — optional: map remaining controls to space (`\n`/`\t` → space) before collapse, if share links may contain newlines.
2. **Low** — keep guestbook prefill; do not add `#rsvp-name`.
3. **Med if shipping QA** — one manual pass: `?to=Đạt%20và%20Người%20Thương`, empty `to`, script string, `?open=1&to=Lan`, click Mở thiệp (address bar keeps `to`).

## Next Steps

1. Done for file/logic gate — **PASS**.
2. Optional visual on live `index.html` query combos.
3. Do not add RSVP wiring.

## Unresolved Questions

- Should encoded newline in `to` become a space (UX) or stay stripped (current spec)?
- User “No RSVP prefill” vs plan guestbook prefill: treated as RSVP-only. Confirm if guestbook should also stay empty.
