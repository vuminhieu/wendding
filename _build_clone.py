# -*- coding: utf-8 -*-
"""Remap extracted section HTML to local assets and print ASCII-safe URL inventory."""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SEC = ROOT / "assets" / "research" / "_extracted" / "sections"
OUT = ROOT / "_build_fragments"
OUT.mkdir(exist_ok=True)

REPLACEMENTS = [
    ("https://cdn.chungdoi.com/uploads/d9528f99-0c36-447b-8640-23a9451d2cae.jpg", "assets/photos/hero.jpg"),
    ("https://cdn.chungdoi.com/uploads/5863b29b-7c13-4a6b-ab93-c0d2d13b37b6.jpg", "assets/photos/01.jpg"),
    ("https://cdn.chungdoi.com/uploads/8882811d-2424-4027-8b38-9660d97475ca.jpg", "assets/photos/02.jpg"),
    ("https://cdn.chungdoi.com/uploads/991f6e03-a840-44bf-b3c4-821cea3b0422.jpg", "assets/photos/03.jpg"),
    ("https://cdn.chungdoi.com/uploads/48e0d0dd-9ef4-4c86-8a64-3be567fcd1ea.jpg", "assets/photos/04.jpg"),
    ("https://cdn.chungdoi.com/uploads/8794e534-1367-4d26-b21b-52ca4175dea5.jpg", "assets/photos/05.jpg"),
    ("https://cdn.chungdoi.com/uploads/5b983a42-ff25-4abe-9326-5a9cf50707da.jpg", "assets/photos/06.jpg"),
    ("https://cdn.chungdoi.com/uploads/49c14506-8332-4718-a4f6-ba327af5104e.jpg", "assets/photos/07.jpg"),
    ("/images/themes/minimalism-dark-red/castle-background.webp", "assets/theme/castle-background.webp"),
    ("/images/themes/minimalism-dark-red/envelope-background.webp", "assets/theme/envelope-background.webp"),
    ("/images/themes/minimalism-dark-red/envelope-cover.webp", "assets/theme/envelope-cover.webp"),
    ("/images/themes/minimalism-dark-red/flower2-decoration.webp", "assets/theme/flower2-decoration.webp"),
    ("/images/themes/minimalism-dark-red/paper.webp", "assets/theme/paper.webp"),
    ("/images/themes/minimalism-dark-red/camera.webp", "assets/theme/camera.webp"),
    ("/images/themes/minimalism-dark-red/cake.webp", "assets/theme/cake.webp"),
    ("/images/themes/minimalism-dark-red/cook.webp", "assets/theme/cook.webp"),
    ("/images/themes/minimalism-dark-red/papernote-background.webp", "assets/theme/papernote-background.webp"),
    ("/images/envelope/minimalism_darkred.webp", "assets/envelope/minimalism_darkred.webp"),
    ("https://cdn.chungdoi.com/music/em-dong-y-i-do.mp3", "assets/audio/em-dong-y-i-do.mp3"),
]

# Maps iframe / API key must never ship.
MAPS_PATTERNS = [
    re.compile(r"https://www\.google\.com/maps/embed[^\s\"']+", re.I),
    re.compile(r"https://maps\.googleapis\.com[^\s\"']+", re.I),
    re.compile(r"AIzaSy[A-Za-z0-9_-]+"),
]

VENUE_DIR = (
    "https://www.google.com/maps/dir/?api=1&destination="
    "Trung%20T%C3%A2m%20H%E1%BB%99i%20Ngh%E1%BB%8B%20White%20Palace%2C%20"
    "194%20Ho%C3%A0ng%20V%C4%83n%20Th%E1%BB%A5%2C%20Ph%C6%B0%E1%BB%9Dng%209%2C%20"
    "Qu%E1%BA%ADn%20Ph%C3%BA%20Nhu%E1%BA%ADn%2C%20TP.%20H%E1%BB%93%20Ch%C3%AD%20Minh"
)

OSM_EMBED = (
    "https://www.openstreetmap.org/export/embed.html"
    "?bbox=106.6680%2C10.7940%2C106.6780%2C10.8020&layer=mapnik"
    "&marker=10.7980%2C106.6730"
)


def remap(html: str) -> str:
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)
    for pat in MAPS_PATTERNS:
        html = pat.sub("", html)
    # Replace leftover iframe maps with OSM if present
    html = re.sub(
        r"<iframe[^>]*(?:google\.com/maps|maps\.googleapis)[^>]*>.*?</iframe>",
        f'<iframe title="Ban do White Palace" src="{OSM_EMBED}" class="invite-map" loading="lazy" referrerpolicy="no-referrer"></iframe>',
        html,
        flags=re.I | re.S,
    )
    return html


def urls_in(html: str) -> list[str]:
    found = re.findall(r"""(?:src|href)=["']([^"']+)["']""", html)
    return found


def main() -> None:
    inventory = {}
    for f in sorted(SEC.glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        mapped = remap(raw)
        (OUT / f.name).write_text(mapped, encoding="utf-8")
        inventory[f.name] = {
            "len": len(mapped),
            "urls": [u.encode("unicode_escape").decode("ascii") for u in urls_in(mapped)],
            "has_maps_key": "AIza" in mapped,
            "has_cdn": "cdn.chungdoi.com" in mapped,
            "has_theme_abs": "/images/" in mapped,
        }
        print(f.name, len(mapped), "key=" + str(inventory[f.name]["has_maps_key"]), "cdn=" + str(inventory[f.name]["has_cdn"]))
        for u in inventory[f.name]["urls"]:
            print("  ", u)
    (OUT / "_inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    print("VENUE_DIR_LEN", len(VENUE_DIR))
    print("DONE")


if __name__ == "__main__":
    main()
