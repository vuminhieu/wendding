from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = 300_000_000

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "photos" / "originals"
OUT_PHOTOS = ROOT / "assets" / "photos"
CARD_DIR = OUT_PHOTOS / "card"
FULL_DIR = OUT_PHOTOS / "full"

HERO_EDGE = 1600
FULL_EDGE = 1600
CARD_EDGE = 800
START_Q = 80
MIN_Q = 60

TARGETS = {
    "hero": 200 * 1024,
    "card": 150 * 1024,
    "full": 400 * 1024,
}


def kb(n: int) -> str:
    return f"{n / 1024:.1f}KB"


def resize_max_edge(im: Image.Image, edge: int) -> Image.Image:
    w, h = im.size
    longest = max(w, h)
    if longest <= edge:
        return im
    scale = edge / longest
    size = (max(1, round(w * scale)), max(1, round(h * scale)))
    return im.resize(size, Image.Resampling.LANCZOS)


def save_webp(im: Image.Image, dest: Path, quality: int) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    kwargs = {"quality": quality, "method": 6}
    im.save(dest, "WEBP", **kwargs)
    return dest.stat().st_size


def load_rgb(path: Path) -> Image.Image:
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode in ("RGBA", "LA"):
            return im.convert("RGB")
        if im.mode != "RGB":
            return im.convert("RGB")
        return im.copy()


def fresh(dest: Path, source: Path, target: int) -> bool:
    return (
        dest.is_file()
        and dest.stat().st_mtime >= source.stat().st_mtime
        and dest.stat().st_size <= target
    )


def encode(im: Image.Image, dest: Path, edge: int, target: int, label: str) -> tuple[int, int]:
    work = resize_max_edge(im, edge)
    quality = START_Q
    size = save_webp(work, dest, quality)
    while size > target and quality > MIN_Q:
        quality -= 10
        size = save_webp(work, dest, quality)
    if size > target and edge > 720:
        smaller = max(720, int(edge * 0.875))
        work = resize_max_edge(im, smaller)
        quality = MIN_Q
        size = save_webp(work, dest, quality)
        edge = smaller
    if size > target:
        print(f"FAIL {label} {dest.relative_to(ROOT)} {kb(size)} > {kb(target)}", file=sys.stderr)
        return size, quality
    print(f"OK   {label:4} {dest.relative_to(ROOT)} {kb(size)} q{quality} edge<={edge}")
    return size, quality


def require(path: Path) -> Path:
    if not path.is_file():
        print(f"missing source: {path}", file=sys.stderr)
        sys.exit(1)
    return path


def main() -> int:
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    FULL_DIR.mkdir(parents=True, exist_ok=True)
    if not SRC.is_dir():
        print(f"put JPEGs in {SRC}", file=sys.stderr)
        return 1

    failed = False
    hero_src = require(SRC / "hero.jpg")
    hero_dest = OUT_PHOTOS / "hero.webp"
    if fresh(hero_dest, hero_src, TARGETS["hero"]):
        print(f"SKIP hero {hero_dest.relative_to(ROOT)} {kb(hero_dest.stat().st_size)}")
    else:
        size, _ = encode(load_rgb(hero_src), hero_dest, HERO_EDGE, TARGETS["hero"], "hero")
        if size > TARGETS["hero"]:
            failed = True

    album_ids = sorted(
        p.stem
        for p in SRC.glob("[0-9][0-9].jpg")
        if p.stem.isdigit()
    )
    if not album_ids:
        print("no numbered album JPEGs in originals", file=sys.stderr)
        return 1

    for stem in album_ids:
        name = f"{stem}.jpg"
        src = require(SRC / name)
        card_dest = CARD_DIR / f"{stem}.webp"
        full_dest = FULL_DIR / f"{stem}.webp"
        if fresh(card_dest, src, TARGETS["card"]) and fresh(full_dest, src, TARGETS["full"]):
            print(f"SKIP {stem} card {kb(card_dest.stat().st_size)} full {kb(full_dest.stat().st_size)}")
            continue
        im = load_rgb(src)
        if fresh(card_dest, src, TARGETS["card"]):
            print(f"SKIP card {card_dest.relative_to(ROOT)} {kb(card_dest.stat().st_size)}")
            card_size = card_dest.stat().st_size
        else:
            card_size, _ = encode(im, card_dest, CARD_EDGE, TARGETS["card"], "card")
        if fresh(full_dest, src, TARGETS["full"]):
            print(f"SKIP full {full_dest.relative_to(ROOT)} {kb(full_dest.stat().st_size)}")
            full_size = full_dest.stat().st_size
        else:
            full_size, _ = encode(im, full_dest, FULL_EDGE, TARGETS["full"], "full")
        if card_size > TARGETS["card"] or full_size > TARGETS["full"]:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
