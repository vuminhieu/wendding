# -*- coding: utf-8 -*-
"""Assemble vanilla index.html / styles.css / app.js from remapped fragments."""
from __future__ import annotations

import html as htmlmod
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
FRAG = ROOT / "_build_fragments"

OSM_EMBED = (
    "https://www.openstreetmap.org/export/embed.html"
    "?bbox=106.6680%2C10.7940%2C106.6780%2C10.8020&layer=mapnik"
    "&marker=10.7980%2C106.6730"
)

QR_GROOM = (
    "/api/qr-png?d=00020101021238540010A0000007270124000697043601101023456789"
    "0208QRIBFTTA53037045802VN63049B81&amp;ec=M"
)
QR_BRIDE = (
    "/api/qr-png?d=00020101021238540010A0000007270124000697040701109988776655"
    "0208QRIBFTTA53037045802VN63043DEB&amp;ec=M"
)

ORDER = [
    "header.html",
    "ceremony.html",
    "album.html",
    "banquet.html",
    "venue.html",
    "dress.html",
    "timeline.html",
    "guestbook.html",
    "gift.html",
    "footer.html",
    "brand.html",
]


def patch(html: str) -> str:
    html = html.replace(QR_GROOM, "assets/qr/groom.png")
    html = html.replace(QR_BRIDE, "assets/qr/bride.png")
    html = html.replace('src=""', f'src="{OSM_EMBED}"', 1)
    html = html.replace(
        '<iframe class="mt-3 h-[268px]',
        '<iframe title="Ban do White Palace" class="mt-3 h-[268px]',
        1,
    )
    return html


def load(name: str) -> str:
    return patch((FRAG / name).read_text(encoding="utf-8"))


STATIC = {
    "block": "display:block",
    "inline": "display:inline",
    "inline-block": "display:inline-block",
    "inline-flex": "display:inline-flex",
    "flex": "display:flex",
    "hidden": "display:none",
    "grid": "display:grid",
    "contents": "display:contents",
    "fixed": "position:fixed",
    "absolute": "position:absolute",
    "relative": "position:relative",
    "sticky": "position:sticky",
    "inset-0": "inset:0",
    "inset-x-0": "left:0;right:0",
    "top-0": "top:0",
    "right-0": "right:0",
    "bottom-0": "bottom:0",
    "left-0": "left:0",
    "top-1/2": "top:50%",
    "left-1/2": "left:50%",
    "overflow-hidden": "overflow:hidden",
    "overflow-x-clip": "overflow-x:clip",
    "overflow-y-auto": "overflow-y:auto",
    "overflow-x-hidden": "overflow-x:hidden",
    "pointer-events-none": "pointer-events:none",
    "pointer-events-auto": "pointer-events:auto",
    "cursor-pointer": "cursor:pointer",
    "isolate": "isolation:isolate",
    "z-0": "z-index:0",
    "z-10": "z-index:10",
    "z-20": "z-index:20",
    "z-30": "z-index:30",
    "z-40": "z-index:40",
    "z-50": "z-index:50",
    "z-[25]": "z-index:25",
    "z-[200]": "z-index:200",
    "-z-10": "z-index:-10",
    "flex-col": "flex-direction:column",
    "flex-row": "flex-direction:row",
    "flex-wrap": "flex-wrap:wrap",
    "flex-1": "flex:1 1 0%",
    "items-center": "align-items:center",
    "items-start": "align-items:flex-start",
    "items-end": "align-items:flex-end",
    "justify-center": "justify-content:center",
    "justify-between": "justify-content:space-between",
    "justify-end": "justify-content:flex-end",
    "text-center": "text-align:center",
    "text-left": "text-align:left",
    "text-right": "text-align:right",
    "uppercase": "text-transform:uppercase",
    "lowercase": "text-transform:lowercase",
    "italic": "font-style:italic",
    "font-bold": "font-weight:700",
    "font-semibold": "font-weight:600",
    "font-medium": "font-weight:500",
    "font-light": "font-weight:300",
    "font-mono": "font-family:ui-monospace,SFMono-Regular,Menlo,monospace",
    "leading-none": "line-height:1",
    "leading-relaxed": "line-height:1.625",
    "whitespace-pre-line": "white-space:pre-line",
    "whitespace-nowrap": "white-space:nowrap",
    "truncate": "overflow:hidden;text-overflow:ellipsis;white-space:nowrap",
    "line-clamp-2": "display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden",
    "w-full": "width:100%",
    "h-full": "height:100%",
    "w-fit": "width:fit-content",
    "max-w-none": "max-width:none",
    "max-w-full": "max-width:100%",
    "min-h-full": "min-height:100%",
    "mx-auto": "margin-left:auto;margin-right:auto",
    "object-contain": "object-fit:contain",
    "object-cover": "object-fit:cover",
    "object-fill": "object-fit:fill",
    "border": "border-width:1px;border-style:solid",
    "border-none": "border:none",
    "border-white": "border-color:#fff",
    "rounded-full": "border-radius:9999px",
    "rounded-lg": "border-radius:0.5rem",
    "rounded-xl": "border-radius:0.75rem",
    "rounded-2xl": "border-radius:1rem",
    "shadow-lg": "box-shadow:0 10px 15px -3px rgba(0,0,0,.1),0 4px 6px -4px rgba(0,0,0,.1)",
    "shadow-xl": "box-shadow:0 20px 25px -5px rgba(0,0,0,.1),0 8px 10px -6px rgba(0,0,0,.1)",
    "no-underline": "text-decoration:none",
    "outline-none": "outline:none",
    "bg-transparent": "background-color:transparent",
    "bg-white": "background-color:#fff",
    "bg-current": "background-color:currentColor",
    "text-white": "color:#fff",
    "text-sm": "font-size:0.875rem;line-height:1.25rem",
    "text-xs": "font-size:0.75rem;line-height:1rem",
    "text-lg": "font-size:1.125rem;line-height:1.75rem",
    "text-base": "font-size:1rem;line-height:1.5rem",
    "text-xl": "font-size:1.25rem;line-height:1.75rem",
    "shrink-0": "flex-shrink:0",
    "grow": "flex-grow:1",
    "space-y-3": "",
    "space-y-0.5": "",
    "space-x-1": "",
    "touch-pan-y": "touch-action:pan-y",
    "select-none": "user-select:none",
    "transition-all": "transition-property:all;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:150ms",
    "transition-colors": "transition-property:color,background-color,border-color;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:150ms",
    "transition-transform": "transition-property:transform;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:150ms",
    "duration-300": "transition-duration:300ms",
    "ease-in-out": "transition-timing-function:ease-in-out",
    "group": "",
    "@container": "container-type:inline-size",
    "tabular-nums": "font-variant-numeric:tabular-nums",
    "tracking-wide": "letter-spacing:0.025em",
    "ring-2": "box-shadow:0 0 0 2px rgba(255,255,255,.3)",
    "ring-white/30": "",
}

SPACING = {
    "0": "0",
    "0.5": "0.125rem",
    "1": "0.25rem",
    "1.5": "0.375rem",
    "2": "0.5rem",
    "2.5": "0.625rem",
    "3": "0.75rem",
    "3.5": "0.875rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "7": "1.75rem",
    "8": "2rem",
    "9": "2.25rem",
    "10": "2.5rem",
    "11": "2.75rem",
    "12": "3rem",
    "14": "3.5rem",
    "15": "3.75rem",
    "16": "4rem",
    "20": "5rem",
    "24": "6rem",
    "28": "7rem",
    "32": "8rem",
    "36": "9rem",
    "40": "10rem",
    "44": "11rem",
    "48": "12rem",
    "52": "13rem",
    "56": "14rem",
    "60": "15rem",
    "64": "16rem",
    "72": "18rem",
    "80": "20rem",
    "96": "24rem",
}

PROP_PREFIX = {
    "p": "padding",
    "px": ("padding-left", "padding-right"),
    "py": ("padding-top", "padding-bottom"),
    "pt": "padding-top",
    "pr": "padding-right",
    "pb": "padding-bottom",
    "pl": "padding-left",
    "m": "margin",
    "mx": ("margin-left", "margin-right"),
    "my": ("margin-top", "margin-bottom"),
    "mt": "margin-top",
    "mr": "margin-right",
    "mb": "margin-bottom",
    "ml": "margin-left",
    "gap": "gap",
    "gap-x": "column-gap",
    "gap-y": "row-gap",
    "w": "width",
    "h": "height",
    "min-w": "min-width",
    "min-h": "min-height",
    "max-w": "max-width",
    "max-h": "max-height",
    "top": "top",
    "right": "right",
    "bottom": "bottom",
    "left": "left",
    "inset": "inset",
    "text": "font-size",
    "leading": "line-height",
    "tracking": "letter-spacing",
    "opacity": "opacity",
    "z": "z-index",
    "rounded": "border-radius",
    "border": "border-width",
    "indent": "text-indent",
}

FRAC = {
    "1/2": "50%",
    "1/3": "33.333333%",
    "2/3": "66.666667%",
    "1/4": "25%",
    "3/4": "75%",
    "full": "100%",
    "screen": "100vh",
    "fit": "fit-content",
    "min": "min-content",
    "max": "max-content",
    "auto": "auto",
    "px": "1px",
}


def arb_value(raw: str) -> str:
    raw = htmlmod.unescape(raw)
    raw = raw.replace("_", " ")
    return raw


def decl_for(cls: str) -> str | None:
    if cls in STATIC:
        return STATIC[cls] or None
    if cls.startswith("aspect-["):
        v = cls[8:-1].replace("/", " / ")
        return f"aspect-ratio:{v}"
    if cls.startswith("aspect-"):
        rest = cls[7:]
        if "/" in rest:
            a, b = rest.split("/", 1)
            return f"aspect-ratio:{a} / {b}"
    if cls.startswith("grid-cols-"):
        n = cls.split("-")[-1]
        if n.isdigit():
            return f"display:grid;grid-template-columns:repeat({n},minmax(0,1fr))"
    if cls.startswith("col-span-"):
        n = cls.split("-")[-1]
        if n.isdigit():
            return f"grid-column:span {n} / span {n}"
    if cls.startswith("translate-"):
        return None  # handled as extra
    if cls.startswith("-translate-"):
        return None
    if cls.startswith("rotate-["):
        return f"transform:rotate({cls[8:-1]})"
    if cls.startswith("rotate-"):
        ang = cls[7:]
        if ang.lstrip("-").isdigit():
            return f"transform:rotate({ang}deg)"
    if cls.startswith("-rotate-["):
        return f"transform:rotate(-{cls[9:-1]})" if False else f"transform:rotate(-{cls[9:-1]})"
    if cls.startswith("-rotate-"):
        ang = cls[8:]
        if ang.isdigit():
            return f"transform:rotate(-{ang}deg)"
    if cls.startswith("scale-["):
        return f"transform:scale({cls[7:-1]})"
    if cls.startswith("drop-shadow-["):
        return f"filter:drop-shadow({arb_value(cls[13:-1])})"
    if cls.startswith("shadow-["):
        return f"box-shadow:{arb_value(cls[8:-1])}"
    if cls.startswith("border-["):
        return f"border-width:{cls[8:-1]}"
    if cls.startswith("bg-base-200/60"):
        return "background-color:rgba(229,231,235,.6)"
    if cls.startswith("bg-base-200"):
        return "background-color:#e5e7eb"
    if cls == "hover:bg-base-200":
        return "background-color:#e5e7eb"
    if cls.startswith("from-") or cls.startswith("to-") or cls.startswith("via-"):
        return None
    m = re.fullmatch(
        r"(-)?(p|px|py|pt|pr|pb|pl|m|mx|my|mt|mr|mb|ml|gap|gap-x|gap-y|w|h|min-w|min-h|max-w|max-h|top|right|bottom|left|inset|text|leading|tracking|opacity|z|rounded|indent)-(.+)",
        cls,
    )
    if not m:
        return None
    neg, prefix, rest = m.group(1), m.group(2), m.group(3)
    prop = PROP_PREFIX.get(prefix)
    if not prop:
        return None
    if rest.startswith("[") and rest.endswith("]"):
        val = arb_value(rest[1:-1])
    elif rest in SPACING:
        val = SPACING[rest]
    elif rest in FRAC:
        val = FRAC[rest]
    elif rest.replace(".", "", 1).isdigit():
        val = SPACING.get(rest, rest)
    else:
        return None
    if neg:
        if val.startswith("var") or val.endswith("%") or val.endswith("px") or val.endswith("rem"):
            val = f"-{val}"
        elif val.replace(".", "", 1).lstrip("-").isdigit():
            val = f"-{val}"
    if isinstance(prop, tuple):
        return ";".join(f"{p}:{val}" for p in prop)
    if prefix == "text" and rest in ("center", "left", "right", "white", "sm", "xs", "lg", "base", "xl"):
        return None
    if prefix == "border" and rest in ("none", "white"):
        return None
    return f"{prop}:{val}"


TRANSFORMS = {
    "-translate-x-1/2": "transform:translateX(-50%)",
    "-translate-y-1/2": "transform:translateY(-50%)",
    "translate-x-[0px]": "transform:translateX(0)",
    "-translate-y-[-16px]": "transform:translateY(16px)",
}


def media_wrap(variant: str, body: str) -> str:
    if variant == "sm":
        return f"@media (min-width:640px){{{body}}}"
    if variant == "md":
        return f"@media (min-width:768px){{{body}}}"
    if variant == "lg":
        return f"@media (min-width:1024px){{{body}}}"
    return body


def escape_cls(cls: str) -> str:
    return re.sub(r"([^a-zA-Z0-9_-])", r"\\\1", cls)


def collect_classes(html: str) -> set[str]:
    found: set[str] = set()
    for m in re.finditer(r'class="([^"]*)"', html):
        raw = htmlmod.unescape(m.group(1))
        for tok in raw.split():
            if tok.startswith("jsx-"):
                continue
            found.add(tok)
    return found


def css_for_classes(classes: set[str]) -> str:
    chunks: list[str] = []
    extra_hover: list[str] = []
    extra_disabled: list[str] = []
    for cls in sorted(classes):
        variants = cls.split(":")
        core = variants[-1]
        prefix_vars = variants[:-1]
        decl = decl_for(core)
        if core in TRANSFORMS:
            decl = TRANSFORMS[core]
        if not decl:
            # arbitrary leftover like hover:scale-[1.03]
            if core.startswith("scale-["):
                decl = f"transform:scale({core[7:-1]})"
            elif core.startswith("opacity-"):
                rest = core[8:]
                if rest.isdigit():
                    decl = f"opacity:{int(rest)/100}"
            elif core.startswith("w-") and core[2:] in SPACING:
                decl = f"width:{SPACING[core[2:]]}"
            elif core.startswith("h-") and core[2:] in SPACING:
                decl = f"height:{SPACING[core[2:]]}"
            else:
                continue
        sel = "." + escape_cls(cls)
        rule = f"{sel}{{{decl}}}"
        hover = "hover" in prefix_vars
        disabled = "disabled" in prefix_vars
        md = "md" in prefix_vars
        sm = "sm" in prefix_vars
        lg = "lg" in prefix_vars
        if hover:
            sel = "." + escape_cls(cls.split("hover:", 1)[-1] if False else cls)
            # class in HTML is the full token including hover:
            sel = "." + escape_cls(cls)
            rule = f"{sel}:hover{{{decl}}}" if "hover:" not in cls else f".{escape_cls(cls)}{{{decl}}}"
            # HTML contains class="hover:scale-105" so selector is .hover\:scale-105:hover
            rule = f".{escape_cls(cls)}:hover{{{decl}}}"
        if disabled:
            rule = f".{escape_cls(cls)}:disabled{{{decl}}}"
        if md:
            rule = media_wrap("md", rule)
        elif sm:
            rule = media_wrap("sm", rule)
        elif lg:
            rule = media_wrap("lg", rule)
        chunks.append(rule)
    # space-y / space-x
    chunks.append(".space-y-3>*+*{margin-top:0.75rem}")
    chunks.append(".space-y-0\\.5>*+*{margin-top:0.125rem}")
    chunks.append(".space-x-1>*+*{margin-left:0.25rem}")
    chunks.append(".hidden.md\\:flex{display:none}")
    chunks.append("@media (min-width:768px){.hidden.md\\:flex{display:flex}}")
    chunks.append(".md\\:flex{display:none}")
    chunks.append("@media (min-width:768px){.md\\:flex{display:flex}}")
    return "\n".join(chunks)


BASE_CSS = r"""
:root{
  --html-bg: oklch(0.21 0.006 56.043);
  --surface-page:#FFF7EB;
  --surface-paper:#511419;
  --ink-cream:#ECE4D8;
  --ink-burgundy:#511419;
  --ink-burgundy-deep:#590310;
  --ink-cream-muted:#ECE4D8B3;
  --ink-burgundy-80:#511419CC;
  --ink-amp-hero:#51141926;
  --ink-cta:#DED9D7;
  --gold-sparkle:#B58B2F;
  --dress-mid:#8C3A3F;
  --dress-gold:#C9A24A;
  --border-invitation:#51141922;
  --shadow-paper:4px 4px 10px rgba(0,0,0,0.25);
  --shadow-fab:0 10px 15px -3px rgba(0,0,0,0.1),0 4px 6px -4px rgba(0,0,0,0.1);
  --font-overline:"Cormorant Garamond",serif;
  --font-display:"Viaoda Libre",serif;
  --font-script-hero:"The Nautigal",cursive;
  --font-script-inner:"Ms Madi",cursive;
  --font-title:"Times New Roman",Times,serif;
  --font-body:Baskerville,"Times New Roman",serif;
  --font-role:Uchen,serif;
  --font-cta:"Lora","Times New Roman",serif;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--html-bg);color:var(--ink-burgundy)}
body{min-height:100vh}
img{max-width:100%;display:block}
button,input,textarea{font:inherit}
.invite-root{
  position:relative;
  width:100%;
  max-width:480px;
  margin:0 auto;
  background:var(--surface-page);
  overflow:hidden;
  isolation:isolate;
}
@media (min-width:768px){
  .invite-root{
    max-width:900px;
    border:1px solid var(--border-invitation);
  }
}
.invite-paper-bg{
  position:absolute;inset:0;z-index:0;pointer-events:none;
  background:url("assets/theme/paper.webp") center/cover;
  opacity:.5;mix-blend-mode:multiply;
}
@keyframes drFloat{
  0%,100%{transform:translateY(0)}
  50%{transform:translateY(-10px)}
}
@keyframes ambient-fall{
  0%{transform:translate3d(0,-30px,0);opacity:0}
  8%{opacity:.9}
  92%{opacity:.9}
  100%{transform:translate3d(var(--sway,0px),110vh,0);opacity:0}
}
@keyframes shine{
  0%{transform:translateX(-4rem)}
  100%{transform:translateX(16rem)}
}
@keyframes seal-pulse{
  0%,100%{transform:scale(1)}
  50%{transform:scale(1.08)}
}
@keyframes ienvHintPulse{
  0%,100%{transform:scale(1);opacity:1}
  50%{transform:scale(1.03);opacity:.92}
}
@keyframes spin-cd{
  to{transform:rotate(360deg)}
}
@keyframes sparkle{
  0%,100%{opacity:.35;transform:scale(.85)}
  50%{opacity:1;transform:scale(1)}
}
.jsx-353cb38c53e4a74a.fixed{z-index:50}
.seal-pulse,.jsx-353cb38c53e4a74a [style*="seal-pulse"]{animation:seal-pulse 2s ease-in-out infinite}
.ienv-sparkle,.ienv-sparkle-2,.ienv-sparkle-3,.ienv-sparkle-4{animation:sparkle 2.4s ease-in-out infinite}
.ienv-sparkle-2{animation-delay:.4s}
.ienv-sparkle-3{animation-delay:.8s}
.ienv-sparkle-4{animation-delay:1.2s}
.music-fab{
  position:fixed;bottom:3.5rem;right:1rem;z-index:40;
  width:3rem;height:3rem;border-radius:9999px;border:0;cursor:pointer;
  background:var(--ink-burgundy);color:var(--ink-cream);
  box-shadow:var(--shadow-fab);
  display:flex;align-items:center;justify-content:center;
  transition:transform .15s cubic-bezier(.4,0,.2,1);
}
.music-fab:hover{transform:scale(1.1)}
.music-fab.is-playing .music-fab__disc{animation:spin-cd 4s linear infinite}
.music-fab__disc{
  width:2.25rem;height:2.25rem;border-radius:9999px;
  background:
    radial-gradient(circle at 50% 50%, #ece4d8 0 7px, transparent 8px),
    repeating-radial-gradient(circle at 50% 50%, #2a0c0e 0 1px, #511419 2px, #6e1a20 3px);
  box-shadow:inset 0 0 0 2px #c9a24a55;
}
.lightbox{
  position:fixed;inset:0;z-index:60;background:rgba(20,4,6,.88);
  display:none;align-items:center;justify-content:center;padding:1.5rem;
}
.lightbox.is-open{display:flex}
.lightbox img{max-width:min(92vw,900px);max-height:88vh;object-fit:contain;border:8px solid #fff}
.lightbox__close{
  position:absolute;top:1rem;right:1rem;width:2.5rem;height:2.5rem;border:0;border-radius:9999px;
  background:#ece4d8;color:#511419;cursor:pointer;font-size:1.4rem;
}
dialog.modal,dialog{
  border:none;padding:0;background:transparent;max-width:min(92vw,640px);
}
dialog::backdrop{background:rgba(20,4,6,.55)}
.modal-backdrop{display:none}
.invite-overlay.is-hidden{display:none !important}
.album-slide{will-change:transform,opacity}
iframe.mt-3,iframe[title="Ban do White Palace"]{border:1px solid #511419}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{
    animation:none !important;
    transition:none !important;
  }
  .music-fab:hover,.music-fab.is-playing .music-fab__disc{transform:none;animation:none}
}
"""

APP_JS = r"""
(function () {
  "use strict";

  var overlay = document.getElementById("invite-envelope");
  var params = new URLSearchParams(location.search);
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function openInvite(push) {
    if (!overlay) return;
    if (reduce) {
      overlay.classList.add("is-hidden");
    } else {
      overlay.style.transition = "opacity .45s ease, transform .45s ease";
      overlay.style.opacity = "0";
      overlay.style.transform = "scale(.98)";
      window.setTimeout(function () {
        overlay.classList.add("is-hidden");
      }, 450);
    }
    document.body.style.overflow = "";
    if (push && !params.has("open")) {
      history.replaceState(null, "", "?open=1");
    }
    tryPlay();
  }

  if (params.get("open") === "1") {
    if (overlay) overlay.classList.add("is-hidden");
  } else {
    document.body.style.overflow = "hidden";
  }

  document.querySelectorAll('a[href="?open=1"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      openInvite(true);
    });
  });

  var audio = document.getElementById("invite-audio");
  var fab = document.getElementById("music-fab");
  function tryPlay() {
    if (!audio) return;
    audio.play().then(function () {
      if (fab) {
        fab.classList.add("is-playing");
        fab.setAttribute("aria-label", "Tam dung nhac");
      }
    }).catch(function () {});
  }
  if (params.get("open") === "1") tryPlay();
  if (fab && audio) {
    fab.addEventListener("click", function () {
      if (audio.paused) tryPlay();
      else {
        audio.pause();
        fab.classList.remove("is-playing");
        fab.setAttribute("aria-label", "Phat nhac");
      }
    });
  }

  var slides = Array.prototype.slice.call(document.querySelectorAll(".album-stage .album-slide"));
  if (!slides.length) {
    var stage = document.querySelector('[style*="perspective:1000px"]');
    if (stage) {
      slides = Array.prototype.slice.call(stage.children);
      slides.forEach(function (el) { el.classList.add("album-slide"); });
    }
  }
  var dots = Array.prototype.slice.call(document.querySelectorAll('[aria-label^="Go to photo"]'));
  var prevBtn = document.querySelector('[aria-label="Previous photo"]');
  var nextBtn = document.querySelector('[aria-label="Next photo"]');
  var albumIndex = 0;
  var POS = {
    0: "translateX(0%) translateZ(0px) rotateY(0deg) scale(1)|1|100",
    1: "translateX(60%) translateZ(-150px) rotateY(45deg) scale(0.85)|0.75|99",
    "-1": "translateX(-60%) translateZ(-150px) rotateY(-45deg) scale(0.85)|0.75|99",
    2: "translateX(120%) translateZ(-300px) rotateY(90deg) scale(0.7)|0.5|98",
    "-2": "translateX(-120%) translateZ(-300px) rotateY(-90deg) scale(0.7)|0.5|98",
    3: "translateX(160%) translateZ(-380px) rotateY(95deg) scale(0.6)|0|96",
    "-3": "translateX(-160%) translateZ(-380px) rotateY(-95deg) scale(0.6)|0|96"
  };
  function wrap(i, n) {
    return ((i % n) + n) % n;
  }
  function renderAlbum() {
    var n = slides.length;
    if (!n) return;
    slides.forEach(function (el, i) {
      var d = i - albumIndex;
      if (d > n / 2) d -= n;
      if (d < -n / 2) d += n;
      var key = String(d);
      var spec = POS[key] || POS[d > 0 ? "3" : "-3"];
      var parts = spec.split("|");
      el.style.transitionDuration = "1100ms";
      el.style.transform = parts[0];
      el.style.opacity = parts[1];
      el.style.zIndex = parts[2];
      el.classList.toggle("ring-2", d === 0);
    });
    dots.forEach(function (dot, i) {
      var on = i === albumIndex;
      dot.style.width = on ? "1.5rem" : "0.5rem";
      dot.style.opacity = on ? "0.7" : "0.25";
    });
  }
  if (slides.length) {
    renderAlbum();
    if (prevBtn) prevBtn.addEventListener("click", function () {
      albumIndex = wrap(albumIndex - 1, slides.length);
      renderAlbum();
    });
    if (nextBtn) nextBtn.addEventListener("click", function () {
      albumIndex = wrap(albumIndex + 1, slides.length);
      renderAlbum();
    });
    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () {
        albumIndex = i;
        renderAlbum();
      });
    });
    slides.forEach(function (el, i) {
      el.addEventListener("click", function () {
        if (i !== albumIndex) {
          albumIndex = i;
          renderAlbum();
          return;
        }
        var img = el.querySelector("img");
        if (img) openLightbox(img.src, img.alt);
      });
    });
  }

  var lightbox = document.getElementById("lightbox");
  var lightboxImg = document.getElementById("lightbox-img");
  function openLightbox(src, alt) {
    if (!lightbox || !lightboxImg) return;
    lightboxImg.src = src;
    lightboxImg.alt = alt || "";
    lightbox.classList.add("is-open");
  }
  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove("is-open");
  }
  if (lightbox) {
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) closeLightbox();
    });
    var closeBtn = lightbox.querySelector(".lightbox__close");
    if (closeBtn) closeBtn.addEventListener("click", closeLightbox);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeLightbox();
    });
  }

  var giftBtn = document.querySelector('button[aria-label="Mở hộp mừng cưới"]');
  var giftDialog = document.querySelector("dialog");
  if (giftBtn && giftDialog) {
    giftBtn.addEventListener("click", function () {
      if (typeof giftDialog.showModal === "function") giftDialog.showModal();
      else giftDialog.setAttribute("open", "");
    });
    giftDialog.addEventListener("click", function (e) {
      if (e.target === giftDialog) giftDialog.close();
    });
  }
  document.querySelectorAll("dialog img[src*='assets/qr/']").forEach(function (img) {
    var wrap = img.closest("div.flex-col, div.flex");
    var saveBtn = wrap ? wrap.querySelector("button") : null;
    if (!saveBtn) return;
    saveBtn.addEventListener("click", function () {
      var a = document.createElement("a");
      a.href = img.getAttribute("src");
      a.download = img.getAttribute("src").split("/").pop();
      a.click();
    });
  });

  var form = document.querySelector('[data-landing-screenshot-id="invite-guestbook"] form');
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var nameInput = form.querySelector('input[type="text"]');
      var ta = form.querySelector("textarea");
      var name = nameInput ? nameInput.value.trim() : "";
      var msg = ta ? ta.value.trim() : "";
      if (!name || !msg) return;
      var list = form.parentElement.querySelector(".overflow-y-auto");
      if (list) {
        var now = new Date();
        var stamp =
          String(now.getHours()).padStart(2, "0") + ":" +
          String(now.getMinutes()).padStart(2, "0") + ":" +
          String(now.getSeconds()).padStart(2, "0") + " " +
          now.getDate() + "/" + (now.getMonth() + 1) + "/" + now.getFullYear();
        var card = document.createElement("div");
        card.className = "rounded-[8px] border p-4 text-sm";
        card.style.borderColor = "rgba(81, 20, 25, 0.333)";
        card.style.backgroundColor = "rgba(255, 255, 255, 0.55)";
        card.innerHTML =
          '<div class="flex items-start justify-between"><span class="font-semibold" style="color: rgb(81, 20, 25);"></span><span class="text-xs opacity-70"></span></div><p class="mt-2 leading-relaxed"></p>';
        card.querySelector(".font-semibold").textContent = name;
        card.querySelector(".opacity-70").textContent = stamp;
        card.querySelector("p").textContent = msg;
        list.insertBefore(card, list.firstChild);
      }
      form.reset();
    });
  }
})();
"""


INDEX_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hoàng Long &amp; Bảo Ngọc</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Ms+Madi&family=The+Nautigal&family=Uchen&family=Viaoda+Libre&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
{overlay}
<main id="invitation" class="invite-root">
  <div class="invite-paper-bg" aria-hidden="true"></div>
  <style>@keyframes drFloat{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}</style>
{body}
</main>
<button type="button" id="music-fab" class="music-fab" aria-label="Phat nhac">
  <span class="music-fab__disc" aria-hidden="true"></span>
</button>
<audio id="invite-audio" src="assets/audio/em-dong-y-i-do.mp3" loop preload="auto"></audio>
<div id="lightbox" class="lightbox" role="dialog" aria-modal="true" aria-label="Album">
  <button type="button" class="lightbox__close" aria-label="Dong">&times;</button>
  <img id="lightbox-img" alt="">
</div>
<script src="app.js"></script>
</body>
</html>
"""


def main() -> None:
    overlay = load("overlay.html")
    overlay = overlay.replace(
        'data-landing-screenshot-id="invite-envelope"',
        'id="invite-envelope" data-landing-screenshot-id="invite-envelope"',
        1,
    )
    overlay = overlay.replace(
        'class="jsx-353cb38c53e4a74a fixed inset-0 z-50',
        'class="invite-overlay jsx-353cb38c53e4a74a fixed inset-0 z-50',
        1,
    )

    sections = [load(name) for name in ORDER]
    album = sections[2]
    album = album.replace(
        'class="relative w-full h-full flex items-center justify-center"',
        'class="album-stage relative w-full h-full flex items-center justify-center"',
        1,
    )
    album = album.replace(
        'class="absolute h-[92%] rounded-2xl overflow-hidden shadow-xl cursor-pointer transition-all ease-in-out',
        'class="album-slide absolute h-[92%] rounded-2xl overflow-hidden shadow-xl cursor-pointer transition-all ease-in-out',
    )
    sections[2] = album

    venue = sections[4]
    if "openstreetmap.org" not in venue:
        venue = re.sub(
            r"(<iframe[^>]*?)\ssrc=\"\"",
            rf'\1 src="{OSM_EMBED}"',
            venue,
            count=1,
        )
        if "openstreetmap.org" not in venue:
            venue = venue.replace(
                "<iframe ",
                f'<iframe src="{OSM_EMBED}" ',
                1,
            )
    sections[4] = venue

    body = "\n".join(sections)
    page = INDEX_TMPL.format(overlay=overlay, body=body)
    all_html = overlay + body
    util = css_for_classes(collect_classes(all_html))
    css = BASE_CSS + "\n" + util + "\n"

    (ROOT / "index.html").write_text(page, encoding="utf-8")
    (ROOT / "styles.css").write_text(css, encoding="utf-8")
    (ROOT / "app.js").write_text(APP_JS, encoding="utf-8")

    inv = {
        "index_len": len(page),
        "css_len": len(css),
        "js_len": len(APP_JS),
        "has_maps_key": "AIza" in page,
        "has_qr_api": "/api/qr-png" in page,
        "has_cdn": "cdn.chungdoi.com" in page,
        "has_osm": "openstreetmap.org" in page,
        "has_groom_qr": "assets/qr/groom.png" in page,
        "has_bride_qr": "assets/qr/bride.png" in page,
        "has_overlay_id": 'id="invite-envelope"' in page,
        "classes": len(collect_classes(all_html)),
    }
    (ROOT / "_assemble_report.json").write_text(
        __import__("json").dumps(inv, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
