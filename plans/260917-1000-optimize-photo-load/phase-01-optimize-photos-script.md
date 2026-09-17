---
phase: 1
title: Optimize photos script
status: completed
priority: P1
dependencies: []
effort: S
---

# Phase 1: Optimize photos script

## Overview

Move camera JPEGs vào `originals/`, gitignore dumps, viết `scripts/optimize-photos.py` (Pillow) sinh `hero.webp` + `card/` + `full/` đạt KB target.

## Requirements

- Functional: script idempotent; process `hero.jpg` + `01.jpg`…`07.jpg`; skip `NTD*` (không output webp)
- Non-functional: Windows PowerShell; Pillow only; print before/after KB; fail non-zero nếu thiếu source hoặc output vượt target

## Architecture

```
assets/photos/*.jpg  --move-->  assets/photos/originals/
scripts/optimize-photos.py
  originals/hero.jpg  -> assets/photos/hero.webp     max edge 1600, webp q80, <200KB
  originals/0N.jpg    -> assets/photos/card/0N.webp  max edge 800,  q80, <150KB
  originals/0N.jpg    -> assets/photos/full/0N.webp  max edge 1600, q80, <400KB
```

Resize: fit **inside** box, keep aspect, LANCZOS. Convert RGB (drop EXIF). `method=6` nếu Pillow hỗ trợ.

Nếu file vẫn > target: hạ q 80→70 rồi 60; **không** tăng q. Nếu vẫn fail, hạ max edge 1600→1400 (full/hero) hoặc 800→720 (card) — ghi log.

Skip write nếu dest exists và mtime >= source mtime **và** size trong target (vẫn print row).

## Related Code Files

- Create: `scripts/optimize-photos.py`
- Create: `assets/photos/originals/` (move existing jpgs)
- Create: `assets/photos/card/`, `assets/photos/full/`
- Create: `.gitignore` (repo chưa có) — ignore `assets/photos/originals/`
- Modify: none of HTML/JS this phase
- Do not delete NTD jpgs; only move

## Implementation Steps

1. Tạo `.gitignore` với:

   ```
   assets/photos/originals/
   ```

   Không ignore `card/`, `full/`, `hero.webp`.

2. Tạo thư mục `assets/photos/originals`, `card`, `full`.

3. Move mọi `assets/photos/*.jpg` (hero, 01–07, NTD*) vào `originals/`. Không để JPG còn ở `assets/photos/` root.

4. Viết `scripts/optimize-photos.py`:
   - `SRC = Path("assets/photos/originals")`
   - Names: `hero.jpg`; `f"{i:02d}.jpg"` for 1..7
   - Helper `resize_max_edge(im, edge)`
   - `save_webp(im, dest, quality)`
   - CLI: `python scripts/optimize-photos.py` từ repo root
   - Exit 1 nếu thiếu hero/01–07 hoặc bất kỳ output vượt target sau retry

5. Chạy script. In bảng KB. `03.jpg` 36MB decode chậm — chấp nhận.

6. Confirm git status: originals untracked/ignored; webp untracked mới.

## Success Criteria

- [x] `python scripts/optimize-photos.py` exits 0
- [x] `hero.webp` <200KB
- [x] 7 card WebP each <150KB
- [x] 7 full WebP each <400KB
- [x] `originals/` gitignored; no `assets/photos/*.jpg` at root
- [x] NTD* remain in originals only (no webp)

## Risk Assessment

- Pillow decode 36MB OOM unlikely on this machine; if crash, process 03 alone first
- EXIF orientation: `ImageOps.exif_transpose` trước resize
- Git: người khác clone không có originals — script phải error rõ “put JPEGs in originals/”
