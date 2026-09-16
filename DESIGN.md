# Minimalism Đỏ Đậm — Design System

Source: live `getComputedStyle` on [chungdoi.com Minimalism Đỏ Đậm demo](https://chungdoi.com/vi/mau-thiep/minimalism-do-dam/demo?open=1), Chrome DevTools page 2, viewport 929×861, invitation scrollHeight 6251. Tokens live in `reports/extract.json`. Do not use site `:root` `--font-primary: Pattaya` / `--font-secondary: Roboto` for invitation type. No live countdown. Do not ship Maps API keys. Download theme/photo/audio locally; do not hotlink.

## 1. Atmosphere & Identity

A closed-then-opened paper invitation on warm cream, not a SaaS landing page. The page feels like a physical thiệp: a pale ivory sheet (`#FFF7EB`) sitting on dark document chrome (`oklch(0.21 0.006 56.043)`), then burgundy boards that read as inked cardstock because a `paper.webp` texture is multiplied at 0.4 over a solid `#511419` fill. Type is a Vietnamese wedding stack — light Viaoda Libre names, a ghost Nautigal ampersand, Times for titles, Baskerville for body — never display-script Pattaya. The signature is **burgundy paper with multiply texture**: cream ink on a 13px-radius board, offset shadow `4px 4px 10px rgba(0,0,0,0.25)`, centered column max 900px. The moment a guest remembers is the envelope lift (cover over background, hint pulse) then the hero names with the 15% burgundy `&` sitting between Hoàng Long and Bảo Ngọc.

Taste / anti-patterns:
- Do not flatten paper into a solid hex card. Fill + multiply texture + radius + offset shadow is the material.
- Do not substitute Inter, Roboto, Pattaya, or generic script for the seven invitation faces.
- Do not add a countdown clock; `03` is the ceremony/banquet day numeral.
- Do not use emoji, glassmorphism, purple gradients, or rounded-2xl-on-everything.
- Do not invent extra gold besides sparkles (`#B58B2F`) and the dress-code gold swatch (`#C9A24A`).
- Animate transform/opacity only. Envelope hint pulse is the only looping decorative motion besides the playing music disc.

## 2. Color

Invitation is light-only. Document chrome behind the card is dark. There is no product dark theme for the invitation itself.

### Palette

| Role | Token | Light | Dark (chrome only) | Usage |
|------|-------|-------|--------------------|-------|
| Chrome | `--html-bg` | — | `oklch(0.21 0.006 56.043)` | `html` background behind invitation |
| Surface/primary | `--surface-page` | `#FFF7EB` | — | Invitation root |
| Surface/paper | `--surface-paper` | `#511419` | — | Ceremony / banquet / timeline board fill |
| Surface/cream-ink | `--ink-cream` | `#ECE4D8` | — | Type on burgundy paper; dress swatch 4 |
| Text/primary (cream field) | `--ink-burgundy` | `#511419` | — | Hero names, cream-field titles, heart, CTAs, borders |
| Text/overline | `--ink-burgundy-deep` | `#590310` | — | SAVE THE DATE |
| Text/secondary on paper | `--ink-cream-muted` | `#ECE4D8B3` | — | Ông bà, district, roles, tư gia, Đón khách |
| Text/secondary on cream | `--ink-burgundy-80` | `#511419CC` | — | Venue address |
| Text/amp-hero | `--ink-amp-hero` | `#51141926` | — | Hero `&` |
| Text/cta | `--ink-cta` | `#DED9D7` | — | Submit label on burgundy pill |
| Accent/gold | `--gold-sparkle` | `#B58B2F` | — | Sparkles only |
| Dress/mid | `--dress-mid` | `#8C3A3F` | — | Dress-code swatch 2 |
| Dress/gold | `--dress-gold` | `#C9A24A` | — | Dress-code swatch 3 |
| Border/invitation | `--border-invitation` | `#51141922` | — | `md` 1px invitation outline |
| Shadow/paper | `--shadow-paper` | `4px 4px 10px rgba(0,0,0,0.25)` | — | Paper boards |
| Shadow/fab | `--shadow-fab` | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)` | — | Music disc |

RGB sources (authoritative): burgundy `rgb(81, 20, 25)`; deep `rgb(89, 3, 16)`; mid `rgb(140, 58, 63)`; cream `rgb(236, 228, 216)`; cream muted `rgba(236, 228, 216, 0.7)`; page `rgb(255, 247, 235)`; gold `rgb(181, 139, 47)`; dress gold `rgb(201, 162, 74)`; CTA text `rgb(222, 217, 215)`; amp `rgba(81, 20, 25, 0.15)`; venue `rgba(81, 20, 25, 0.8)`; border `rgba(81, 20, 25, 0.133)`.

### Rules

- Never introduce a color not in this table. Extend the table first.
- Burgundy is both ink and paper fill. Cream is both page-adjacent ink and dress swatch — do not swap page cream (`#FFF7EB`) with type cream (`#ECE4D8`).
- Gold is not a second brand color for headings. Sparkles + one dress swatch only.
- Accent for interaction is burgundy (pills, caret, 3px outline). Gold is decorative.

## 3. Typography

Seven families are required. Site marketing fonts (Pattaya, Roboto) are forbidden on the invitation.

### Font stack

| Token | Family | Role |
|-------|--------|------|
| `--font-overline` | `"Cormorant Garamond", serif` | SAVE THE DATE |
| `--font-display` | `"Viaoda Libre", serif` | Hero names; ceremony H3 names |
| `--font-script-hero` | `"The Nautigal", cursive` | Hero `&`; calendar month |
| `--font-script-inner` | `"Ms Madi", cursive` | Inner paper `&` |
| `--font-title` | `"Times New Roman", Times, serif` | H2 / cream-field titles, day numerals, submit, timeline hours |
| `--font-body` | `Baskerville, "Times New Roman", serif` | Families, báo tin, tư gia, venue, weekdays, labels |
| `--font-role` | `Uchen, serif` | Trưởng Nam / Út Nữ |

### Scale (desktop live values; mobile noted)

| Level | Size | Weight | Line height | Tracking | Family | Usage |
|-------|------|--------|-------------|----------|--------|-------|
| Amp/hero | 120px | 300 | 120px | 0 | The Nautigal | Hero `&` |
| Display/hero | 58px (`clamp(38px, 11vw, 46px)` → 58px md) | 300 | 1 (leading-none) | 0 | Viaoda Libre | Hoàng Long / Bảo Ngọc |
| Display/paper | 46px (md leading 60px, min-h 80px, w 80%) | 400 | ~60px md | 0 | Viaoda Libre | Đặng Hoàng Long / Vũ Bảo Ngọc |
| Day numeral | 46px (40px mobile) | 300 | 1 | 0 | Times | `03` — date, not a timer |
| Banquet lead | 26px | 400 | 39px | 0 | Baskerville | “Tiệc cưới sẽ diễn ra vào lúc:” |
| Month | 25px | 400 | — | 0.625px | The Nautigal | Tháng 1 / 2026 |
| Title/cream-field | 20px | 700 | 30px | 0.6px | Times | Sổ lưu bút, Hộp Quà Mừng, Dress code |
| Title/on-paper (span) | 20px | 700 | 30px | 0.48px | Times | THÔNG TIN LỄ/TIỆC CƯỚI inner SPAN |
| Title/on-paper (h2) | 16px | 700 | — | 0.48px | Times | H2 wrapper; paint the SPAN at 20px |
| Amp/inner | 35px | 300 | — | 0 | Ms Madi | Paper `&` |
| Overline | 18px (15px mobile) | 600 | 27px | 2.88px | Cormorant Garamond | SAVE THE DATE uppercase |
| Body/lg paper | 18px | 400 | 27px | 0 | Baskerville | LỄ THÀNH HÔN… TƯ GIA (`--ink-cream-muted`) |
| Venue title | 16px | 700 | 24px | 0.48px | Times | Tiệc cưới sẽ tổ chức tại (`--ink-burgundy`) |
| Time secondary | 15px | 300 | 22.5px | 0 | Baskerville | 18:00 muted on paper |
| Family | 14px | 600 | — | 0 | Baskerville | Parent names on paper |
| Venue addr | 14px | 300 | 22.75px | 0 | Baskerville | Address on cream |
| Submit | 14px | 600 | — | 0 | Times | GỬI LỜI CHÚC |
| Báo tin | 13px | 300 | 19.5px | 0 | Baskerville | TRÂN TRỌNG BÁO TIN… |
| Ông bà / Đón khách | 12px | 300 | 16–18px | 0 / 0.6px | Baskerville | Muted labels |
| Weekday | 11px | 500 | — | 0 | Baskerville | T2–CN |
| Role | 10px | 300 | 15px | 1.4px | Uchen | Trưởng Nam / Út Nữ |
| District | 10px | 300 | 12.5px | 0 | Baskerville | Quận… |
| Timeline hour | 17px (16px mobile) | 300 | 23.375px | 0.425px | Times | tabular-nums tracking-wide |

### Rules

- Load the seven faces. Silent fallback to Inter/system is a defect.
- Body on paper may be 10–13px (roles, districts, báo tin) — this invitation is denser than the architecture’s 14px floor; keep live sizes.
- H2 vs inner SPAN: wrapper computes 16px/700; visible title is the SPAN at 20px/700 Times cream, uppercase, tracking 0.48px.
- Earlier closed-page dump of tư gia as 16px/300 burgundy is stale. Opened live is 18px/400 cream 0.7.

## 4. Spacing & Layout

Base unit 4px. Live padding that is not on the 4px grid is documented as exception.

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Tight |
| `--space-2` | 8px | Submit vertical padding |
| `--space-3` | 12px | Compact |
| `--space-4` | 16px | Default |
| `--space-5` | 20px | Paper horizontal padding (`px-5`) |
| `--space-6` | 24px | Paper content gap (`gap-6`); submit horizontal padding |
| `--space-8` | 32px | |
| `--space-9` | 36px | Hero horizontal padding; exception (9×4) |
| `--space-10` | 40px | Paper top (`pt-9` = 36px live — use 36) |
| `--space-12` | 48px | Music FAB `bottom-14` (56px) nearby |
| `--space-14` | 56px | Hero bottom padding; FAB offset |
| `--space-15` | 60px | Hero top padding; exception |
| `--space-paper-bottom` | 40px | Paper `pb-10` |

### Grid

- Invitation max: `480px` default, `900px` from `md`, centered (`md:mx-auto`).
- Invitation height ~6250px at 900px wide. `overflow: hidden`, `isolate`.
- Paper boards: width 560px, centered (~x 177 at 900px canvas). Ceremony 560×848 y=958 r=13; banquet 560×875 y=2476 r=10; timeline 560×405 y=4198 r=10.
- Paper content column: 520px, `flex-col items-center gap-6`, `relative z-10`.
- Calendar: 280px mobile, 330×283 md, r=8, y=2899.
- Map: 560×380 r=15 y=3488.
- Breakpoints that matter: mobile invitation 480; md 768 (names 58px, paper 560, calendar 330, border on). Extracted desktop vw 929.

### Vertical rhythm (section y on 900×6250)

SAVE THE DATE 61 → hero names 764 → ceremony paper 958 → day 1674 → banquet paper 2476 → calendar 2899 → venue 3401 → map 3488 → dress 4012 → timeline 4198 → guestbook 4759 → submit 4993 → gift 5719.

### Rules

- Hero wrap padding is `60px 36px 56px` (exceptions). Paper is `pt-9 px-5 pb-10` (36 / 20 / 40).
- Asymmetric hero padding (60 top / 56 bottom) is intentional — matches live.
- Do not stretch paper to full 900px; boards stay ~560 with side cream.

## 5. Components

Vanilla HTML/CSS/JS primitives. No React.

### InvitationFrame

- **Structure**: root `relative w-full max-w-[480px] md:max-w-[900px] md:mx-auto overflow-hidden md:border isolate` over dark `html`.
- **Variants**: closed (envelope overlay) / open (`?open=1` content).
- **Spacing**: full-bleed cream; md border `--border-invitation`.
- **States**: default only at frame level.
- **Accessibility**: `lang="vi"`; skip decorative castle bg (`opacity: 0.1`, `object-fit: contain`, `aria-hidden`).
- **Motion**: envelope exit on open (transform/opacity).

### Envelope

- **Structure**: stack `envelope-background.webp` 420×484 z-10 `object-fit: fill` + `envelope-cover.webp` 420×277 z-30 + hint pulse.
- **Variants**: closed / opening / opened (removed or translated off).
- **States**: default; hint looping; reduced-motion = static.
- **Motion**: `ienvHintPulse` `2s ease-in-out infinite`.
- **Accessibility**: open control must be a button; do not trap focus after open.

### PaperCard

- **Structure**: relative parent (`rounded-[13px]` ceremony / `10px` banquet & timeline) → absolute inset fill `--surface-paper` same radius → `paper.webp` cover, opacity 0.4, `mix-blend-mode: multiply`, same radius → content `relative z-10 flex flex-col items-center gap-6`.
- **Variants**: ceremony (848 / r13 / `px-5 pb-10 pt-9`), banquet (875 / r10), timeline (405 / r10).
- **Spacing**: parent 560 wide; content 520; shadow `--shadow-paper`.
- **States**: static.
- **Accessibility**: headings in source order; cream on burgundy must keep live sizes (do not lighten fill).

### HeroNames

- **Structure**: overline SAVE THE DATE → name / amp / name. Amp absolutely overlapping between names.
- **States**: static.
- **Typography**: tokens in §3. Amp color `--ink-amp-hero`.

### DateBlock

- **Structure**: weekday + 46px Times `03` + month/year + lunar line. Not a countdown.
- **States**: static.
- **Accessibility**: the numeral is text “03”, not `role="timer"`.

### Calendar

- **Structure**: month The Nautigal; weekdays Baskerville 11/500; grid; day 3 = heart SVG.
- **Heart**: viewBox `0 0 24 22`, 30×28, fill `--ink-burgundy`. Path starts `M12 21C12 21 1.5 13.5 1.5 7.5C1.5 4.46 3.96 2 7 2C8.76 2 10.35 2.81 11.4 4.09L12`.
- **States**: default; selected day is the heart, not a filled square.
- **Accessibility**: calendar semantics or labelled grid; heart has accessible “3”.

### MapEmbed

- **Structure**: 560×380 r=15. Static map or iframe **without** shipping a Google API key (proxy or snapshot).
- **States**: default; loading placeholder cream.
- **Accessibility**: title “Bản đồ White Palace”; address also in text above.

### DressSwatches

- **Structure**: four 48×48 squares: `--ink-burgundy`, `--dress-mid`, `--dress-gold`, `--ink-cream`.
- **States**: static (not pickers).
- **Accessibility**: list of color names, not empty divs.

### GuestbookForm

- **Structure**: title “Sổ lưu bút”; input 348×46 “Nhập tên*”; textarea 348×110 “Nhập lời chúc*”; submit pill.
- **Spacing**: input border `1px solid var(--ink-burgundy)`; caret burgundy; outline `3px` burgundy on focus.
- **States**: default; hover submit `scale(1.05)`; focus 3px burgundy outline; disabled (opacity + no scale); error (keep burgundy, do not introduce a new red); empty.
- **Motion**: submit `transform 0.15s cubic-bezier(0.4, 0, 0.2, 1)`.
- **Accessibility**: labels; `*` required; button type submit.

### SubmitPill

- **Structure**: `padding: 8px 24px`; radius 9999px; bg `--ink-burgundy`; color `--ink-cta`; Times 14/600; 149×36.
- **States**: default; hover scale 1.05; active scale ~1; focus visible ring; disabled.
- **Motion**: micro 150ms.

### GiftBox

- **Structure**: title “Hộp Quà Mừng”; CTA “Mở hộp mừng cưới” ~250×357; stacked envelopes `minimalism_darkred.webp` (204×252 z1 / 235×304 z2).
- **Variants**: closed stack / open modal with two VietQR (local assets).
- **States**: default; hover (micro scale if live); open dialog; empty N/A.
- **Accessibility**: dialog with close; do not copy bank secrets from demo if replacing with user data later.

### MusicFab

- **Structure**: `fixed bottom-14 right-4 z-40`; button `w-12 h-12 rounded-full shadow-lg` (~48×54 hit).
- **States**: playing (`aria-label="Tạm dừng nhạc"`, `animate-spin-cd`); paused (static, play label); hover `scale(1.10)`.
- **Motion**: spin while playing; hover 150ms.
- **Audio**: local copy of `em-dong-y-i-do.mp3`, loop. Playing on open matches source.
- **Accessibility**: toggle button; reduced-motion disables spin.

### TimelineRow

- **Structure**: hour Times 17/300 cream tabular-nums + icon 40×40 (camera/cake/cook) + label.
- **States**: static.
- **Content through**: 20:30 Kết thúc tiệc.

## 6. Motion & Interaction

### Timing

| Type | Duration | Easing | Usage |
|------|----------|--------|-------|
| Micro | 150ms | `cubic-bezier(0.4, 0, 0.2, 1)` | Submit hover scale 1.05; FAB hover 1.10; transform only |
| Hint | 2000ms | `ease-in-out` infinite | Envelope hint `ienvHintPulse` |
| Disc | continuous | linear spin (`animate-spin-cd`) | Music FAB while playing |
| Envelope open | match source (~transform/opacity, not layout) | — | Cover/background exit |

Source recorded 46 keyframes. Clone only the motions that are visible: hint pulse, disc spin, pill/FAB scale, envelope open. Do not port unused keyframes.

### Rules

- Only animate `transform` and `opacity`.
- Hover + focus + active on submit, FAB, gift CTA, envelope open.
- `prefers-reduced-motion: reduce` → no pulse, no spin, no hover scale; envelope jumps to open.
- No countdown tick.

## 7. Depth & Surface

**Strategy: mixed** — cream page + md hairline border + offset paper shadow + multiply paper texture. Not glass. Not tonal-shift-only.

| Layer | Treatment | Usage |
|-------|-----------|-------|
| Chrome | Dark `oklch(0.21 0.006 56.043)` | Outside the card |
| Page | Flat `#FFF7EB` + `1px solid #51141922` at md | Invitation sheet |
| Castle wash | `castle-background.webp` opacity 0.1, contain, absolute | Atmosphere behind hero, not a hero image |
| Paper | Solid `#511419` + `paper.webp` opacity 0.4 multiply + r 10–13 + `4px 4px 10px rgba(0,0,0,0.25)` | Ceremony / banquet / timeline |
| Envelope | Two bitmap layers, z 10 / 30, fill | Closed state |
| Gift | Two envelope bitmaps, z 1 / 2, slight offset | Gift CTA |
| FAB | Circle + Tailwind `shadow-lg` | Music |
| Map | r=15 clip, no extra glass | Venue |

No drop-shadow on hero names. Depth comes from the ghost ampersand, the paper board, and the envelope stack.

### Assets (download under `assets/`, never hotlink)

Theme `/images/themes/minimalism-dark-red/`: `castle-background.webp`, `envelope-background.webp`, `envelope-cover.webp`, `flower2-decoration.webp`, `paper.webp`, `camera.webp`, `cake.webp`, `cook.webp`, `papernote-background.webp`. Envelope `/images/envelope/minimalism_darkred.webp`. Audio `https://cdn.chungdoi.com/music/em-dong-y-i-do.mp3`. Couple photos: the 39 live `<img>` files. Fonts via `@font-face` for the seven families (97 faces on source — subset to used weights).
