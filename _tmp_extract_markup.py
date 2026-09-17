# -*- coding: utf-8 -*-
import json, re, pathlib

root = pathlib.Path(r"C:\Users\Admin\hieuvm\wendding_page\assets\research\_extracted\sections")
out = pathlib.Path(r"C:\Users\Admin\hieuvm\wendding_page\_tmp_markup.json")

def styles(html):
    found = re.findall(r'style="([^"]{0,800})"', html)
    uniq = []
    for s in found:
        if s not in uniq:
            uniq.append(s)
    return uniq[:80]

def attrs(html, name):
    return re.findall(r'\b' + name + r'="([^"]{0,400})"', html)[:40]

data = {}
for p in sorted(root.glob("*.html")):
    t = p.read_text(encoding="utf-8")
    data[p.name] = {
        "len": len(t),
        "styles": styles(t),
        "aria": attrs(t, "aria-label"),
        "alt": attrs(t, "alt"),
        "data": re.findall(r'data-[a-z0-9-]+="[^"]*"', t)[:30],
        "keyframes_hint": bool("keyframes" in t.lower() or "animation" in t.lower()),
        "animation": re.findall(r'animation:[^;"\']+', t)[:20],
        "transform": re.findall(r'transform:[^;"\']+', t)[:20],
    }
out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("ok", len(data))
