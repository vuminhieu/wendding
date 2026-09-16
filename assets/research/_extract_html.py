import json
from pathlib import Path

base = Path(r"C:\Users\Admin\hieuvm\wendding_page\assets\research")
out = base / "_extracted"
out.mkdir(exist_ok=True)

files = [
    "live-header-full.json",
    "live-ceremony-full.json",
    "live-album-full.json",
    "live-banquet-full.json",
    "live-timeline-full.json",
    "live-overlay-card.json",
    "dump-guestbook.json",
    "dump-gift.json",
    "dump-venue.json",
    "dump-dress.json",
    "dump-footer.json",
]

for name in files:
    p = base / name
    if not p.exists():
        print("MISSING", name)
        continue
    raw = p.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
        html = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
    except Exception:
        html = raw.strip().strip('"')
        html = html.encode("utf-8").decode("unicode_escape") if "\\n" in html[:200] else html
    dest = out / (p.stem + ".html")
    dest.write_text(html, encoding="utf-8")
    print(name, "->", dest.name, "len", dest.stat().st_size)
