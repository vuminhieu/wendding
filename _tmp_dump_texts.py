# -*- coding: utf-8 -*-
import json, re, pathlib
from html.parser import HTMLParser

root = pathlib.Path(r"C:\Users\Admin\hieuvm\wendding_page\assets\research\_extracted")
sec = root / "sections"
out = pathlib.Path(r"C:\Users\Admin\hieuvm\wendding_page\_tmp_texts.json")

class TextCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        d = dict(attrs)
        if tag == "img":
            src = d.get("src", "")
            alt = d.get("alt", "")
            self.parts.append(f"[img {alt} | {src.split('/')[-1]}]")
        if tag == "a":
            href = d.get("href", "")
            self.parts.append(f"[a {href[:180]}]")
        if tag == "iframe":
            self.parts.append("[iframe omitted]")
    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if self.skip:
            return
        t = data.strip()
        if t and t not in ("<!-- -->",):
            self.parts.append(t)

data = {}
for p in sorted(sec.glob("*.html")):
    html = p.read_text(encoding="utf-8")
    c = TextCollector()
    try:
        c.feed(html)
    except Exception as e:
        c.parts.append(f"PARSE_ERR {e}")
    # unique consecutive
    texts = []
    for t in c.parts:
        if not texts or texts[-1] != t:
            texts.append(t)
    data[p.name] = texts

# also pull overlay CTA/card class names
ov = (sec / "overlay.html").read_text(encoding="utf-8")
# extract class strings containing ienv
ienv = sorted(set(re.findall(r'class="([^"]*ienv[^"]*)"', ov)))
data["_overlay_ienv_classes"] = ienv
data["_overlay_len"] = len(ov)

# gift srcs
gift = (sec / "gift.html").read_text(encoding="utf-8")
data["_gift_srcs"] = re.findall(r'src="([^"]+)"', gift)
data["_gift_classes"] = sorted(set(re.findall(r'class="([^"]{10,200})"', gift)))[:40]

# guestbook placeholders
gb = (sec / "guestbook.html").read_text(encoding="utf-8")
data["_gb_placeholders"] = re.findall(r'placeholder="([^"]*)"', gb)
data["_gb_classes"] = sorted(set(re.findall(r'class="([^"]{20,240})"', gb)))[:30]

# album classes
al = (sec / "album.html").read_text(encoding="utf-8")
data["_album_classes"] = sorted(set(re.findall(r'class="([^"]{20,240})"', al)))[:30]
data["_album_srcs"] = re.findall(r'src="([^"]+)"', al)

# banquet calendar days
bn = (sec / "banquet.html").read_text(encoding="utf-8")
data["_banquet_hrefs"] = re.findall(r'href="([^"]+)"', bn)
data["_banquet_classes"] = sorted(set(re.findall(r'class="([^"]{30,240})"', bn)))[:40]

# timeline
tl = (sec / "timeline.html").read_text(encoding="utf-8")
data["_timeline_srcs"] = re.findall(r'src="([^"]+)"', tl)

# header remainder after truncation
hd = (sec / "header.html").read_text(encoding="utf-8")
# names block
m = re.search(r'mt-16 flex flex-col[\s\S]+$', hd)
data["_header_tail"] = hd[-1200:]

# venue remainder
vn = (sec / "venue.html").read_text(encoding="utf-8")
data["_venue_tail"] = vn[-800:]
data["_venue_hrefs"] = re.findall(r'href="([^"]+)"', vn)

out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", out, "keys", len(data))
