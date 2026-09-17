# -*- coding: utf-8 -*-
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
FRAG = ROOT / "_build_fragments"


def ascii(s: str) -> str:
    return s.encode("unicode_escape").decode("ascii")


def dump(name: str, max_chars: int = 4000) -> None:
    p = FRAG / name
    t = p.read_text(encoding="utf-8")
    print("===", name, "len", len(t))
    # tags of interest
    tags = re.findall(r"<(iframe|dialog|a |button|form|audio|style)[^>]{0,400}", t, re.I)
    print("TAGS", [ascii(x[:120]) for x in tags][:20])
    print("HAS_IFRAME", "<iframe" in t.lower())
    print("HAS_DIALOG", "<dialog" in t.lower())
    print("HAS_QR", "qr-png" in t or "qr/" in t)
    print("HAS_AIza", "AIza" in t)
    print("HEAD", ascii(t[:max_chars]))
    print("---TAIL---")
    print(ascii(t[-min(2000, len(t)) :]))
    print()


for n in [
    "overlay.html",
    "venue.html",
    "gift.html",
    "album.html",
    "guestbook.html",
    "header.html",
]:
    dump(n, 2500)
