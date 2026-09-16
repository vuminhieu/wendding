# -*- coding: utf-8 -*-
import json, re, pathlib

root = pathlib.Path(r"C:\Users\Admin\hieuvm\wendding_page\assets\research\_extracted\sections")
out = pathlib.Path(r"C:\Users\Admin\hieuvm\wendding_page\_tmp_section_classes.json")
data = {}
for p in sorted(root.glob("*.html")):
    t = p.read_text(encoding="utf-8")
    classes = re.findall(r'class="([^"]{0,500})"', t)
    uniq = []
    for c in classes:
        if c not in uniq:
            uniq.append(c)
    srcs = re.findall(r'(?:src|href)="([^"]+)"', t)
    texts = re.findall(r">([^<]{1,80})<", t)
    texts = [x.strip() for x in texts if x.strip()]
    data[p.name] = {
        "len": len(t),
        "uniq_classes": uniq[:80],
        "srcs": srcs[:40],
        "texts": texts[:60],
    }
out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", out, "keys", list(data.keys()))
