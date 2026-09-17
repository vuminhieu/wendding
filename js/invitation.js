(() => {
  const PHOTO_IDS = ["01", "02", "03", "04", "05", "06", "07"];
  const PHOTOS_CARD = PHOTO_IDS.map((id) => `assets/photos/card/${id}.webp`);
  const PHOTOS_FULL = PHOTO_IDS.map((id) => `assets/photos/full/${id}.webp`);

  const WISH_SEED = [
    ["Duy Khang", "Chúc mừng ngày vui của hai bạn, trăm năm hạnh phúc bền lâu!"],
    ["Lan Chi", "Đẹp đôi quá! Chúc hai bạn sống bên nhau đầu bạc răng long."],
    ["Tuấn Anh", "Mừng hạnh phúc hai bạn! Chúc gia đình nhỏ luôn đầy ắp tiếng cười."],
    ["Khánh Vy", "Chúc cô dâu chú rể luôn giữ được nụ cười này mãi mãi nhé!"],
    ["Gia Bảo", "Nhìn thiệp là thấy tình yêu rồi. Chúc hai bạn trăm năm viên mãn!"],
    ["Hải Yến", "Chúc đám cưới thật trọn vẹn và ấm áp. Hạnh phúc nhé hai bạn!"],
    ["Minh Đức", "Cuối cùng cũng tới ngày trọng đại, chúc mừng cặp đôi xứng lứa vừa đôi!"],
    ["Thu Hà", "Chúc hai bạn mãi mãi yêu thương và bên nhau trọn đời!"],
    ["Thuỳ Linh", "Mẫu thiệp đẹp quá, tông đỏ đô sang trọng ghê. Chúc mừng hai bạn!"],
    ["Ngọc Trâm", "Chúc hai bạn trăm năm hạnh phúc, sớm sinh quý tử nhé!"]
  ];

  const AI_WISHES = [
    "Chúc hai bạn trăm năm hạnh phúc, sớm sum vầy bên nhau.",
    "Chúc cô dâu chú rể một đời bình an, yêu thương bền chặt.",
    "Mừng ngày vui, chúc gia đình mới luôn đầy ắp tiếng cười."
  ];

  const overlay = document.getElementById("overlay");
  const openBtn = document.getElementById("open-invite");
  const musicBtn = document.getElementById("music-btn");
  const bgm = document.getElementById("bgm");
  const toast = document.getElementById("toast");
  const params = new URLSearchParams(location.search);
  const alreadyOpen = params.get("open") === "1";

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("is-on");
    setTimeout(() => toast.classList.remove("is-on"), 2200);
  }

  function spawnHearts() {
    const root = document.getElementById("hearts");
    const colors = ["#a8323b", "#ece4d8", "#c9a24a", "#7a1f26"];
    const n = 12;
    for (let i = 0; i < n; i++) {
      const el = document.createElement("div");
      el.className = "heart";
      const size = 12 + Math.random() * 12;
      const sway = (Math.random() * 60 - 30).toFixed(2);
      el.style.left = `${Math.random() * 92}%`;
      el.style.color = colors[i % colors.length];
      el.style.fontSize = `${size}px`;
      el.style.setProperty("--sway", `${sway}px`);
      el.style.setProperty("--dur", `${18 + Math.random() * 8}s`);
      el.style.setProperty("--delay", `${-Math.random() * 24}s`);
      el.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path></svg>';
      root.appendChild(el);
    }
  }

  function playMusic() {
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

  function openInvite() {
    if (overlay.hidden || overlay.classList.contains("is-leaving")) return;
    overlay.classList.add("is-leaving");
    playMusic();
    let closed = false;
    const done = () => {
      if (closed) return;
      closed = true;
      overlay.hidden = true;
      overlay.classList.remove("is-leaving");
    };
    overlay.addEventListener("transitionend", done, { once: true });
    setTimeout(done, 800);
    const url = new URL(location.href);
    url.searchParams.set("open", "1");
    history.replaceState({}, "", url);
  }

  function buildCalendar() {
    const grid = document.getElementById("calendar-grid");
    const firstWeekday = new Date(2026, 9, 1).getDay();
    const offset = firstWeekday === 0 ? 6 : firstWeekday - 1;
    for (let i = 0; i < offset; i++) {
      grid.appendChild(document.createElement("div")).className = "cal-cell";
    }
    for (let d = 1; d <= 31; d++) {
      const cell = document.createElement("div");
      cell.className = "cal-cell";
      if (d === 24) {
        cell.innerHTML = '<div class="cal-heart" aria-label="24"><svg viewBox="0 0 24 22" fill="#511419"><path d="M12 21C12 21 1.5 13.5 1.5 7.5C1.5 4.46 3.96 2 7 2C8.76 2 10.35 2.81 11.4 4.09L12 4.8L12.6 4.09C13.65 2.81 15.24 2 17 2C20.04 2 22.5 4.46 22.5 7.5C22.5 13.5 12 21 12 21Z"></path></svg><span>24</span></div>';
      } else {
        cell.innerHTML = `<span>${d}</span>`;
      }
      grid.appendChild(cell);
    }
  }

  let albumIndex = 0;

  function fanTransform(offset, n) {
    const half = Math.floor(n / 2);
    let o = offset;
    if (o > half) o -= n;
    if (o < -half) o += n;
    const abs = Math.abs(o);
    if (abs > 3) {
      return { transform: "translateX(0) translateZ(-600px) scale(0.5)", opacity: 0, z: 90 - abs };
    }
    const x = o * 60;
    const z = -Math.abs(o) * 150;
    const rot = o * 45;
    const scale = o === 0 ? 1 : abs === 1 ? 0.85 : 0.7;
    const opacity = o === 0 ? 1 : abs === 1 ? 0.75 : abs === 2 ? 0.5 : 0.3;
    const zIndex = 100 - abs;
    return {
      transform: `translateX(${x}%) translateZ(${z}px) rotateY(${rot}deg) scale(${scale})`,
      opacity,
      z: zIndex
    };
  }

  function applyAlbumTransforms() {
    const fan = document.getElementById("album-fan");
    const dots = document.getElementById("album-dots");
    const n = PHOTO_IDS.length;
    [...fan.children].forEach((btn, i) => {
      const t = fanTransform(i - albumIndex, n);
      btn.style.transform = t.transform;
      btn.style.opacity = String(t.opacity);
      btn.style.zIndex = String(t.z);
      btn.style.boxShadow = i === albumIndex ? "0 20px 25px -5px rgba(0,0,0,0.15)" : "";
    });
    [...dots.children].forEach((dot, i) => {
      dot.classList.toggle("is-active", i === albumIndex);
    });
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
        img.loading = i === 0 ? "eager" : "lazy";
        btn.appendChild(img);
        btn.addEventListener("click", () => {
          if (i === albumIndex) openLightbox(i);
          else {
            albumIndex = i;
            applyAlbumTransforms();
          }
        });
        fan.appendChild(btn);

        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "album-dot";
        dot.setAttribute("aria-label", `Go to photo ${i + 1}`);
        dot.addEventListener("click", () => {
          albumIndex = i;
          applyAlbumTransforms();
        });
        dots.appendChild(dot);
      });
    }
    applyAlbumTransforms();
  }

  function stepAlbum(dir) {
    albumIndex = (albumIndex + dir + PHOTO_IDS.length) % PHOTO_IDS.length;
    applyAlbumTransforms();
  }

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

  const WISH_KEY = "invitation-wishes";

  function loadWishes() {
    try {
      const raw = localStorage.getItem(WISH_KEY);
      if (raw) return JSON.parse(raw);
    } catch {}
    return WISH_SEED.map(([name, text]) => ({
      name,
      text,
      time: "12:30:49 26/7/2026"
    }));
  }

  function saveWishes(list) {
    localStorage.setItem(WISH_KEY, JSON.stringify(list));
  }

  function formatNow() {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())} ${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
  }

  function renderWishes() {
    const root = document.getElementById("wishes");
    const list = loadWishes();
    root.innerHTML = list.map((w) => `
      <article class="wish">
        <div class="wish-head">
          <span class="wish-name">${escapeHtml(w.name)}</span>
          <span class="wish-time">${escapeHtml(w.time)}</span>
        </div>
        <p>${escapeHtml(w.text)}</p>
      </article>
    `).join("");
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  spawnHearts();
  buildCalendar();
  renderAlbum();
  buildThumbs();
  renderWishes();

  if (alreadyOpen) {
    overlay.hidden = true;
    playMusic();
  }

  openBtn.addEventListener("click", openInvite);
  musicBtn.addEventListener("click", () => {
    if (bgm.paused) playMusic();
    else pauseMusic();
  });

  document.getElementById("album-prev").addEventListener("click", () => stepAlbum(-1));
  document.getElementById("album-next").addEventListener("click", () => stepAlbum(1));
  document.getElementById("lb-close").addEventListener("click", () => lightbox.close());
  document.getElementById("lightbox").addEventListener("click", (e) => {
    if (e.target.id === "lightbox") e.target.close();
  });

  {
    const stage = document.querySelector(".album-stage");
    let x0 = null;
    stage.addEventListener("pointerdown", (e) => { x0 = e.clientX; });
    stage.addEventListener("pointerup", (e) => {
      if (x0 == null) return;
      const dx = e.clientX - x0;
      x0 = null;
      if (dx > 40) stepAlbum(-1);
      else if (dx < -40) stepAlbum(1);
    });
  }
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

  document.getElementById("wish-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const name = document.getElementById("wish-name").value.trim();
    const text = document.getElementById("wish-msg").value.trim();
    if (!name || !text) return;
    const list = loadWishes();
    list.unshift({ name, text, time: formatNow() });
    saveWishes(list);
    renderWishes();
    e.target.reset();
    showToast("Đã gửi lời chúc");
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
