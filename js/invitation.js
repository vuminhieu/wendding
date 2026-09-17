(() => {
  const PHOTO_IDS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"];
  const PHOTOS_CARD = PHOTO_IDS.map((id) => `assets/photos/card/${id}.webp`);
  const PHOTOS_FULL = PHOTO_IDS.map((id) => `assets/photos/full/${id}.webp`);

  const WISH_DB_URL = "https://wedding-minhieu-phuonganh-default-rtdb.asia-southeast1.firebasedatabase.app";

  const AI_WISHES = [
    "Chúc hai bạn trăm năm hạnh phúc, sớm sum vầy bên nhau.",
    "Chúc cô dâu chú rể một đời bình an, yêu thương bền chặt.",
    "Mừng ngày vui, chúc gia đình mới luôn đầy ắp tiếng cười."
  ];

  const BGM_TRACKS = [
    "assets/audio/bai_nay_khong_de_di_dien.mp3",
    "assets/audio/em-dong-y-i-do.mp3"
  ];

  const overlay = document.getElementById("overlay");
  const openBtn = document.getElementById("open-invite");
  const invitation = document.getElementById("invitation");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const musicBtn = document.getElementById("music-btn");
  const bgm = document.getElementById("bgm");
  let bgmIndex = 0;
  const toast = document.getElementById("toast");
  const params = new URLSearchParams(location.search);
  const alreadyOpen = params.get("open") === "1";
  const MAX_GUEST_NAME = 80;

  function sanitizeGuestName(raw) {
    if (raw == null) return "";
    const name = String(raw)
      .replace(/[\u0000-\u001F\u007F]/g, "")
      .replace(/\s+/g, " ")
      .trim();
    if (!name) return "";
    return name.length > MAX_GUEST_NAME ? name.slice(0, MAX_GUEST_NAME).trim() : name;
  }

  function applyGuestName(name) {
    if (!name) return;
    const overlayGuest = document.getElementById("overlay-guest");
    const heroInvite = document.getElementById("hero-invite");
    const heroGuest = document.getElementById("hero-guest");
    const wishName = document.getElementById("wish-name");
    const rsvpName = document.getElementById("rsvp-name");
    overlayGuest.textContent = name;
    overlayGuest.hidden = false;
    heroGuest.textContent = name;
    heroInvite.hidden = false;
    if (wishName && !wishName.value) wishName.value = name;
    if (rsvpName && !rsvpName.value) rsvpName.value = name;
  }

  applyGuestName(sanitizeGuestName(params.get("to")));

  const WEDDING_DAY = Date.parse("2026-10-25T00:00:00+07:00");
  const THANKS_DAY = Date.parse("2026-10-26T00:00:00+07:00");

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function renderCountdown() {
    const cells = document.getElementById("countdown-cells");
    const done = document.getElementById("countdown-done");
    const live = document.getElementById("countdown-live");
    if (!cells || !done) return false;

    const now = Date.now();
    if (now >= WEDDING_DAY) {
      const label = document.querySelector("#countdown .countdown-label");
      if (label) label.hidden = true;
      cells.hidden = true;
      done.hidden = false;
      done.textContent = now >= THANKS_DAY
        ? "Trân trọng cảm ơn"
        : "Hôm nay là ngày cưới";
      if (live) live.textContent = done.textContent;
      return false;
    }

    let ms = WEDDING_DAY - now;
    const days = Math.floor(ms / 86400000);
    ms %= 86400000;
    const hours = Math.floor(ms / 3600000);
    ms %= 3600000;
    const mins = Math.floor(ms / 60000);
    ms %= 60000;
    const secs = Math.floor(ms / 1000);

    document.getElementById("cd-days").textContent = String(days);
    document.getElementById("cd-hours").textContent = pad2(hours);
    document.getElementById("cd-mins").textContent = pad2(mins);
    document.getElementById("cd-secs").textContent = pad2(secs);

    const summary = `Còn ${days} ngày ${hours} giờ`;
    if (live && live.dataset.summary !== summary) {
      live.dataset.summary = summary;
      live.textContent = summary;
    }
    return true;
  }

  function startCountdown() {
    if (!renderCountdown()) return;
    const id = setInterval(() => {
      if (document.hidden) return;
      if (!renderCountdown()) clearInterval(id);
    }, 1000);
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) return;
      if (!renderCountdown()) clearInterval(id);
    });
  }

  startCountdown();

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("is-on");
    setTimeout(() => toast.classList.remove("is-on"), 2200);
  }

  function spawnHearts(root, n, mode) {
    if (!root) return;
    const colors = ["#a8323b", "#ece4d8", "#c9a24a", "#7a1f26"];
    for (let i = 0; i < n; i++) {
      const el = document.createElement("div");
      const size = 12 + Math.random() * 14;
      el.style.color = colors[i % colors.length];
      el.style.fontSize = `${size}px`;
      el.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path></svg>';
      if (mode === "float") {
        el.className = "heart heart--float";
        el.style.left = `${4 + Math.random() * 90}%`;
        el.style.top = `${6 + Math.random() * 84}%`;
        el.style.setProperty("--bob-dur", `${4.6 + Math.random() * 1.6}s`);
        el.style.setProperty("--bob-delay", `${(-Math.random() * 4.8).toFixed(2)}s`);
      } else {
        el.className = "heart";
        el.style.left = `${Math.random() * 94}%`;
        el.style.setProperty("--sway", `${(Math.random() * 72 - 36).toFixed(2)}px`);
        el.style.setProperty("--dur", `${10 + Math.random() * 6}s`);
        el.style.setProperty("--delay", `${-Math.random() * 16}s`);
      }
      root.appendChild(el);
    }
  }

  function loadBgmTrack(index) {
    bgmIndex = ((index % BGM_TRACKS.length) + BGM_TRACKS.length) % BGM_TRACKS.length;
    const next = BGM_TRACKS[bgmIndex];
    if (bgm.getAttribute("src") !== next) {
      bgm.src = next;
    }
  }

  function playMusic() {
    loadBgmTrack(bgmIndex);
    bgm.play().then(() => {
      musicBtn.classList.add("is-playing");
      musicBtn.setAttribute("aria-label", "Tạm dừng nhạc");
    }).catch(() => {
      musicBtn.classList.remove("is-playing");
      musicBtn.setAttribute("aria-label", "Phát nhạc");
    });
  }

  function pauseMusic() {
    bgm.pause();
    musicBtn.classList.remove("is-playing");
    musicBtn.setAttribute("aria-label", "Phát nhạc");
  }

  function revealInvitation() {
    invitation?.removeAttribute("aria-hidden");
    invitation?.removeAttribute("inert");
  }

  function openInvite() {
    if (!document.body.classList.contains("await-open") || document.body.classList.contains("is-opening")) return;
    document.body.classList.remove("await-open");
    document.body.classList.add("is-opening");
    openBtn.disabled = true;
    openBtn.setAttribute("aria-busy", "true");
    overlay.classList.add("is-leaving");
    playMusic();

    let closed = false;
    const done = () => {
      if (closed) return;
      closed = true;
      overlay.hidden = true;
      overlay.classList.remove("is-leaving");
      document.body.classList.remove("is-opening");
      document.body.classList.add("is-opened");
      revealInvitation();
      openBtn.disabled = false;
      openBtn.removeAttribute("aria-busy");
      invitation?.focus({ preventScroll: true });
      startAlbumAutoplay(900);
    };

    if (reduceMotion.matches) {
      done();
    } else {
      overlay.addEventListener("transitionend", (e) => {
        if (e.target === overlay) done();
      }, { once: true });
      setTimeout(done, 1700);
    }

    const url = new URL(location.href);
    url.searchParams.set("open", "1");
    history.replaceState({}, "", url);
  }

  function buildCalendar(gridId, heartDay) {
    const grid = document.getElementById(gridId);
    if (!grid) return;
    const firstWeekday = new Date(2026, 9, 1).getDay();
    const offset = firstWeekday === 0 ? 6 : firstWeekday - 1;
    for (let i = 0; i < offset; i++) {
      grid.appendChild(document.createElement("div")).className = "cal-cell";
    }
    for (let d = 1; d <= 31; d++) {
      const cell = document.createElement("div");
      cell.className = "cal-cell";
      if (d === heartDay) {
        cell.innerHTML = `<div class="cal-heart" aria-label="${d}"><svg viewBox="0 0 24 22" fill="#511419"><path d="M12 21C12 21 1.5 13.5 1.5 7.5C1.5 4.46 3.96 2 7 2C8.76 2 10.35 2.81 11.4 4.09L12 4.8L12.6 4.09C13.65 2.81 15.24 2 17 2C20.04 2 22.5 4.46 22.5 7.5C22.5 13.5 12 21 12 21Z"></path></svg><span>${d}</span></div>`;
      } else {
        cell.innerHTML = `<span>${d}</span>`;
      }
      grid.appendChild(cell);
    }
  }

  let albumPos = 0;
  let albumTimer = null;
  let albumRaf = 0;
  let albumAnim = null;
  let albumDragging = false;
  let albumLock = null;
  const ALBUM_DURATION = 680;
  const ALBUM_INTERVAL = 3000;

  function albumCount() {
    return PHOTO_IDS.length;
  }

  function wrapDelta(offset, n) {
    let o = offset;
    const half = n / 2;
    while (o > half) o -= n;
    while (o < -half) o += n;
    return o;
  }

  function shortestTarget(from, to, n) {
    let d = ((to - from) % n + n) % n;
    if (d > n / 2) d -= n;
    return from + d;
  }

  function easeOutCubic(t) {
    return 1 - (1 - t) ** 3;
  }

  function applyAlbumTransforms(pos) {
    const fan = document.getElementById("album-fan");
    const dots = document.getElementById("album-dots");
    const n = albumCount();
    const idx = ((Math.round(pos) % n) + n) % n;
    [...fan.children].forEach((btn, i) => {
      const o = wrapDelta(i - pos, n);
      const abs = Math.abs(o);
      const x = o * 50;
      const z = -abs * 150;
      const rot = o * 22;
      const scale = 1 - Math.min(abs, 3) * 0.12;
      const opacity = abs >= 2.55 ? 0 : abs <= 1 ? 1 - abs * 0.16 : Math.max(0, 0.84 - (abs - 1) * 0.52);
      btn.style.transform = `translate3d(${x}%, 0, ${z}px) rotateY(${rot}deg) scale(${scale})`;
      btn.style.opacity = String(opacity);
      btn.style.zIndex = String(Math.round(120 - abs * 20));
      btn.style.boxShadow = abs < 0.35 ? "0 22px 28px -8px rgba(0,0,0,0.22)" : "";
    });
    [...dots.children].forEach((dot, i) => {
      dot.classList.toggle("is-active", i === idx);
    });
  }

  function albumIndex() {
    const n = albumCount();
    return ((Math.round(albumPos) % n) + n) % n;
  }

  function normalizeAlbumPos() {
    const n = albumCount();
    albumPos = ((albumPos % n) + n) % n;
  }

  function stopAlbumAnim() {
    if (albumRaf) {
      cancelAnimationFrame(albumRaf);
      albumRaf = 0;
    }
    albumAnim = null;
    albumAnimDone = null;
  }

  function tickAlbum(now) {
    if (!albumAnim) {
      albumRaf = 0;
      return;
    }
    const t = Math.min(1, (now - albumAnim.start) / albumAnim.dur);
    albumPos = albumAnim.from + (albumAnim.to - albumAnim.from) * easeOutCubic(t);
    applyAlbumTransforms(albumPos);
    if (t < 1) {
      albumRaf = requestAnimationFrame(tickAlbum);
      return;
    }
    albumPos = albumAnim.to;
    normalizeAlbumPos();
    albumAnim = null;
    albumRaf = 0;
    applyAlbumTransforms(albumPos);
    if (albumAnimDone) {
      const done = albumAnimDone;
      albumAnimDone = null;
      done();
    }
  }

  let albumAnimDone = null;

  function animateAlbumTo(target, dur, onDone) {
    stopAlbumAnim();
    albumAnimDone = onDone || null;
    const dist = Math.abs(target - albumPos);
    const ms = Math.max(280, Math.min(dur, 280 + dist * 420));
    albumAnim = { from: albumPos, to: target, start: performance.now(), dur: ms };
    albumRaf = requestAnimationFrame(tickAlbum);
  }

  function goToAlbum(next, { user = false } = {}) {
    const n = albumCount();
    const idx = ((next % n) + n) % n;
    const target = shortestTarget(albumPos, idx, n);
    if (Math.abs(target - albumPos) < 0.001) return;
    stopAlbumAutoplay();
    animateAlbumTo(target, ALBUM_DURATION, user ? startAlbumAutoplay : null);
  }

  function renderAlbum() {
    const fan = document.getElementById("album-fan");
    const dots = document.getElementById("album-dots");
    if (fan.childElementCount === 0) {
      PHOTO_IDS.forEach((_, i) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "album-card";
        const img = document.createElement("img");
        img.src = PHOTOS_CARD[i];
        img.alt = `Wedding photo ${i + 1}`;
        img.decoding = "async";
        img.draggable = false;
        img.loading = i <= 2 ? "eager" : "lazy";
        btn.appendChild(img);
        btn.addEventListener("click", (e) => {
          if (albumDidDrag) {
            e.preventDefault();
            return;
          }
          if (i === albumIndex()) openLightbox(i);
          else goToAlbum(i, { user: true });
        });
        fan.appendChild(btn);

        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "album-dot";
        dot.setAttribute("aria-label", `Go to photo ${i + 1}`);
        dot.addEventListener("click", () => goToAlbum(i, { user: true }));
        dots.appendChild(dot);
      });
    }
    applyAlbumTransforms(albumPos);
  }

  function stepAlbum(dir, user = false) {
    stopAlbumAutoplay();
    animateAlbumTo(albumPos + dir, ALBUM_DURATION, user ? startAlbumAutoplay : null);
  }

  function stopAlbumAutoplay() {
    if (albumTimer) {
      window.clearTimeout(albumTimer);
      albumTimer = null;
    }
  }

  function overlayOpen() {
    return !overlay.hidden && !overlay.classList.contains("is-leaving");
  }

  function lightboxOpen() {
    return Boolean(lightbox && lightbox.open);
  }

  function albumCanPlay() {
    return !albumDragging && !lightboxOpen() && !document.hidden && !overlayOpen();
  }

  function startAlbumAutoplay(delay) {
    stopAlbumAutoplay();
    if (!albumCanPlay()) return;
    albumTimer = window.setTimeout(() => {
      albumTimer = null;
      if (!albumCanPlay()) return;
      animateAlbumTo(albumPos + 1, ALBUM_DURATION, () => startAlbumAutoplay());
    }, delay == null ? ALBUM_INTERVAL : delay);
  }

  let albumDidDrag = false;

  let lbIndex = 0;
  const lightbox = document.getElementById("lightbox");
  const lbImg = document.getElementById("lb-img");
  const lbCount = document.getElementById("lb-count");
  const lbThumbs = document.getElementById("lb-thumbs");

  function prefetchFull(src) {
    const img = new Image();
    img.src = src;
  }

  function prefetchNeighbor(i) {
    const n = PHOTO_IDS.length;
    const run = () => {
      prefetchFull(PHOTOS_FULL[(i + 1) % n]);
      prefetchFull(PHOTOS_FULL[(i - 1 + n) % n]);
    };
    if ("requestIdleCallback" in window) requestIdleCallback(run, { timeout: 2000 });
    else setTimeout(run, 200);
  }

  function renderLb() {
    lbImg.src = PHOTOS_FULL[lbIndex];
    lbImg.alt = `Ảnh cưới ${lbIndex + 1}`;
    lbCount.textContent = `${lbIndex + 1} / ${PHOTO_IDS.length}`;
    [...lbThumbs.children].forEach((el, i) => {
      el.classList.toggle("is-active", i === lbIndex);
    });
  }

  function openLightbox(i) {
    lbIndex = i;
    renderLb();
    stopAlbumAutoplay();
    lightbox.showModal();
    prefetchNeighbor(lbIndex);
  }

  function buildThumbs() {
    PHOTOS_CARD.forEach((src, i) => {
      const b = document.createElement("button");
      b.type = "button";
      const img = document.createElement("img");
      img.src = src;
      img.alt = `Thumbnail ${i + 1}`;
      img.loading = "lazy";
      img.decoding = "async";
      b.appendChild(img);
      if (i === 0) b.classList.add("is-active");
      b.addEventListener("click", () => {
        lbIndex = i;
        renderLb();
        prefetchNeighbor(lbIndex);
      });
      lbThumbs.appendChild(b);
    });
  }

  function wishDbRoot() {
    return String(WISH_DB_URL || "").replace(/\/+$/, "");
  }

  function wishesFromSnapshot(data) {
    if (!data || typeof data !== "object") return [];
    return Object.keys(data)
      .map((id) => {
        const w = data[id];
        if (!w || typeof w !== "object") return null;
        const name = String(w.name || "").trim();
        const text = String(w.text || "").trim();
        if (!name || !text) return null;
        return {
          id,
          name,
          text,
          time: String(w.time || ""),
          at: Number(w.at) || 0
        };
      })
      .filter(Boolean)
      .sort((a, b) => b.at - a.at);
  }

  async function loadWishes() {
    const root = wishDbRoot();
    if (!root) return [];
    const res = await fetch(`${root}/wishes.json`);
    if (!res.ok) throw new Error("wish-load");
    return wishesFromSnapshot(await res.json());
  }

  async function postWish(wish) {
    const root = wishDbRoot();
    if (!root) throw new Error("wish-config");
    const res = await fetch(`${root}/wishes.json`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(wish)
    });
    if (!res.ok) throw new Error("wish-save");
  }

  function formatNow() {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())} ${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
  }

  async function renderWishes() {
    const root = document.getElementById("wishes");
    root.innerHTML = `<p class="wish-status">Đang tải lời chúc…</p>`;
    try {
      const list = await loadWishes();
      if (!list.length) {
        root.innerHTML = `<p class="wish-status">Chưa có lời chúc. Hãy là người đầu tiên.</p>`;
        return;
      }
      root.innerHTML = list.map((w) => `
      <article class="wish">
        <div class="wish-head">
          <span class="wish-name">${escapeHtml(w.name)}</span>
          <time class="wish-time">${escapeHtml(w.time)}</time>
        </div>
        <p>${escapeHtml(w.text)}</p>
      </article>
    `).join("");
    } catch {
      root.innerHTML = `<p class="wish-status wish-status--error">Không tải được sổ lưu bút.</p>`;
    }
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  spawnHearts(document.getElementById("hearts"), 18, "float");
  spawnHearts(document.getElementById("hearts"), 26);
  spawnHearts(document.getElementById("page-falls"), 28);
  buildCalendar("calendar-grid-groom", 24);
  buildCalendar("calendar-grid-bride", 25);
  renderAlbum();
  buildThumbs();
  renderWishes();

  if (alreadyOpen) {
    document.body.classList.remove("await-open", "is-opening");
    document.body.classList.add("is-opened");
    revealInvitation();
    overlay.hidden = true;
    playMusic();
    startAlbumAutoplay();
  }

  openBtn.addEventListener("click", openInvite);
  musicBtn.addEventListener("click", () => {
    if (bgm.paused) playMusic();
    else pauseMusic();
  });
  bgm.addEventListener("ended", () => {
    loadBgmTrack(bgmIndex + 1);
    playMusic();
  });

  document.getElementById("album-prev").addEventListener("click", () => stepAlbum(-1, true));
  document.getElementById("album-next").addEventListener("click", () => stepAlbum(1, true));
  document.getElementById("lb-close").addEventListener("click", () => lightbox.close());
  document.getElementById("lightbox").addEventListener("click", (e) => {
    if (e.target.id === "lightbox") e.target.close();
  });
  lightbox.addEventListener("close", startAlbumAutoplay);

  {
    const stage = document.querySelector(".album-stage");
    let startX = 0;
    let startY = 0;
    let startPos = 0;
    let lastX = 0;
    let lastT = 0;
    let vel = 0;
    let pid = null;

    function unitWidth() {
      return Math.max(160, stage.clientWidth * 0.42);
    }

    function onDown(e) {
      if (e.pointerType === "mouse" && e.button !== 0) return;
      stopAlbumAnim();
      stopAlbumAutoplay();
      albumLock = null;
      albumDragging = false;
      albumDidDrag = false;
      pid = e.pointerId;
      startX = lastX = e.clientX;
      startY = e.clientY;
      startPos = albumPos;
      lastT = performance.now();
      vel = 0;
    }

    function onMove(e) {
      if (pid == null || e.pointerId !== pid) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      if (!albumLock) {
        if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
        albumLock = Math.abs(dx) > Math.abs(dy) ? "x" : "y";
        if (albumLock === "x") {
          albumDragging = true;
          albumDidDrag = true;
          stage.classList.add("is-dragging");
          try { stage.setPointerCapture(pid); } catch {}
        }
      }
      if (albumLock !== "x") return;
      e.preventDefault();
      const now = performance.now();
      const dt = now - lastT;
      if (dt > 0) vel = (e.clientX - lastX) / dt;
      lastX = e.clientX;
      lastT = now;
      albumPos = startPos - dx / unitWidth();
      applyAlbumTransforms(albumPos);
    }

    function settle() {
      const n = albumCount();
      let target = albumPos - vel * 220 / unitWidth();
      const nearest = Math.round(albumPos);
      if (Math.abs(vel) > 0.35 && nearest === Math.round(target)) {
        target = nearest + (vel > 0 ? -1 : 1);
      } else {
        target = Math.round(target);
      }
      if (target > albumPos + n / 2) target -= n;
      if (target < albumPos - n / 2) target += n;
      albumDragging = false;
      pid = null;
      albumLock = null;
      stage.classList.remove("is-dragging");
      animateAlbumTo(target, ALBUM_DURATION, startAlbumAutoplay);
    }

    function onUp(e) {
      if (pid == null || e.pointerId !== pid) return;
      if (albumLock === "x") settle();
      else {
        pid = null;
        albumLock = null;
        albumDragging = false;
        stage.classList.remove("is-dragging");
        startAlbumAutoplay();
      }
    }

    stage.addEventListener("pointerdown", onDown);
    stage.addEventListener("pointermove", onMove, { passive: false });
    stage.addEventListener("pointerup", onUp);
    stage.addEventListener("pointercancel", onUp);
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopAlbumAutoplay();
    else startAlbumAutoplay();
  });

  startAlbumAutoplay();
  document.getElementById("lb-prev").addEventListener("click", () => {
    lbIndex = (lbIndex - 1 + PHOTO_IDS.length) % PHOTO_IDS.length;
    renderLb();
    prefetchNeighbor(lbIndex);
  });
  document.getElementById("lb-next").addEventListener("click", () => {
    lbIndex = (lbIndex + 1) % PHOTO_IDS.length;
    renderLb();
    prefetchNeighbor(lbIndex);
  });

  document.getElementById("gift-open").addEventListener("click", () => {
    document.getElementById("gift-dialog").showModal();
  });
  document.getElementById("gift-close").addEventListener("click", () => {
    document.getElementById("gift-dialog").close();
  });
  document.getElementById("gift-dialog").addEventListener("click", (e) => {
    if (e.target.id === "gift-dialog") e.target.close();
  });

  document.querySelectorAll(".save-qr").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const href = btn.getAttribute("data-qr");
      try {
        const res = await fetch(href);
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = href.split("/").pop();
        a.click();
        URL.revokeObjectURL(url);
      } catch {
        window.open(href, "_blank");
      }
    });
  });

  document.getElementById("ai-wish").addEventListener("click", () => {
    const ta = document.getElementById("wish-msg");
    ta.value = AI_WISHES[Math.floor(Math.random() * AI_WISHES.length)];
  });

  document.getElementById("wish-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("wish-name").value.trim();
    const text = document.getElementById("wish-msg").value.trim();
    if (!name || !text) return;
    const submitBtn = e.target.querySelector(".submit");
    if (submitBtn) submitBtn.disabled = true;
    try {
      await postWish({ name, text, time: formatNow(), at: Date.now() });
      e.target.reset();
      applyGuestName(sanitizeGuestName(params.get("to")));
      await renderWishes();
      showToast("Đã gửi lời chúc");
    } catch (err) {
      showToast(err && err.message === "wish-config"
        ? "Chưa cấu hình sổ lưu bút"
        : "Không gửi được, thử lại");
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });

  const rsvpDialog = document.getElementById("rsvp-dialog");
  document.getElementById("rsvp-open").addEventListener("click", () => rsvpDialog.showModal());
  document.getElementById("rsvp-cancel").addEventListener("click", () => rsvpDialog.close());
  document.getElementById("rsvp-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const name = document.getElementById("rsvp-name").value.trim();
    const status = document.getElementById("rsvp-status").value;
    localStorage.setItem("invitation-rsvp", JSON.stringify({ name, status, at: Date.now() }));
    rsvpDialog.close();
    showToast(status === "yes" ? "Cảm ơn bạn đã xác nhận tham dự" : "Đã ghi nhận phản hồi");
  });
})();
