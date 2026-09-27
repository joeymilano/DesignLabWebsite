/* 1% Design Lab — site interactions. No dependencies. */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const track = (name, params) => { try { window.gtag && gtag('event', name, params); } catch (e) {} };

  /* Shanghai clock */
  const clocks = $$('[data-clock]');
  if (clocks.length) {
    const fmt = new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Shanghai', hour: '2-digit', minute: '2-digit', hour12: false });
    const tick = () => clocks.forEach(c => { c.textContent = `SHA ${fmt.format(new Date())} GMT+8`; });
    tick(); setInterval(tick, 15000);
  }

  /* Header: solid after hero edge, hide on scroll down */
  const hdr = $('.hdr');
  let lastY = scrollY;
  const onScroll = () => {
    const y = scrollY;
    if (hdr) {
      hdr.classList.toggle('is-solid', y > 24);
      hdr.classList.toggle('is-hidden', y > 480 && y > lastY + 2 && !root.classList.contains('menu-open'));
      if (y < lastY - 2) hdr.classList.remove('is-hidden');
    }
    lastY = y;
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const burger = $('.burger');
  burger && burger.addEventListener('click', () => {
    const open = root.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open);
  });
  $$('.mnav a').forEach(a => a.addEventListener('click', () => root.classList.remove('menu-open')));

  /* Reveal */
  const revealEls = $$('[data-reveal],[data-lines]');
  if (reduce || !('IntersectionObserver' in window)) revealEls.forEach(el => el.classList.add('is-in'));
  else {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(el => io.observe(el));
  }
  requestAnimationFrame(() => $$('[data-lines].hero-now').forEach(el => el.classList.add('is-in')));

  /* Count-up */
  const counters = $$('[data-count]');
  const render = (el, v) => {
    const dec = +(el.dataset.dec || 0);
    el.firstChild.nodeValue = v.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  };
  const run = el => {
    const to = parseFloat(el.dataset.count), t0 = performance.now(), dur = 1600;
    const step = t => {
      const p = Math.min(1, (t - t0) / dur);
      render(el, to * (1 - Math.pow(1 - p, 4)));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if (counters.length && !reduce && 'IntersectionObserver' in window) {
    counters.forEach(el => render(el, 0));
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
    }), { threshold: 0.5 });
    counters.forEach(el => io.observe(el));
  }

  /* Doors: crossfade carousels, faster on hover */
  $$('.door').forEach(door => {
    const imgs = $$('.door-media img', door);
    const count = $('.door-count', door);
    if (imgs.length < 2) return;
    let i = 0, timer;
    const show = n => {
      imgs[i].classList.remove('is-on');
      i = (n + imgs.length) % imgs.length;
      imgs[i].classList.add('is-on');
      if (count) count.textContent = `${String(i + 1).padStart(2, '0')} / ${String(imgs.length).padStart(2, '0')}`;
    };
    const loop = ms => { clearInterval(timer); if (!reduce) timer = setInterval(() => show(i + 1), ms); };
    loop(4200);
    door.addEventListener('mouseenter', () => { show(i + 1); loop(1500); });
    door.addEventListener('mouseleave', () => loop(4200));
  });

  /* Manifesto: light words with scroll */
  $$('[data-manifesto]').forEach(el => {
    const zh = /^zh/.test(root.lang);
    const split = (node, hl) => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const parts = zh ? [...n.nodeValue] : n.nodeValue.split(/(\s+)/);
          const frag = document.createDocumentFragment();
          parts.forEach(p => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            const s = document.createElement('span');
            s.className = hl ? 'w hl' : 'w';
            s.textContent = p;
            frag.appendChild(s);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) split(n, hl || n.classList.contains('hl'));
      });
    };
    split(el, false);
    const words = $$('.w', el);
    if (reduce) { words.forEach(w => w.classList.add('on')); return; }
    let ticking = false;
    const update = () => {
      ticking = false;
      const r = el.getBoundingClientRect(), vh = innerHeight;
      const p = Math.min(1, Math.max(0, (vh * 0.82 - r.top) / (r.height + vh * 0.3)));
      const n = Math.round(p * words.length);
      words.forEach((w, k) => w.classList.toggle('on', k < n));
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  });

  /* Filters: <div data-filter="#target"><button data-f="all|key"> ; items carry data-k="a b" */
  $$('[data-filter]').forEach(bar => {
    const target = $(bar.dataset.filter);
    if (!target) return;
    const btns = $$('button', bar);
    btns.forEach(b => b.addEventListener('click', () => {
      const f = b.dataset.f;
      btns.forEach(x => x.setAttribute('aria-pressed', x === b));
      $$('[data-k]', target).forEach(it => { it.hidden = f !== 'all' && !it.dataset.k.split(' ').includes(f); });
      track('work_filter', { filter: f });
    }));
  });

  /* Work index: cursor-follow preview */
  const peek = $('.peek');
  if (peek && fine && !reduce) {
    const img = $('img', peek);
    let x = 0, y = 0, px = 0, py = 0, raf = 0, on = false;
    const loop = () => {
      px += (x - px) * 0.16; py += (y - py) * 0.16;
      peek.style.transform = `translate3d(${px}px,${py}px,0) translate(-50%,-50%)`;
      raf = on || Math.abs(x - px) > 0.5 ? requestAnimationFrame(loop) : 0;
    };
    addEventListener('mousemove', e => { x = e.clientX + 40; y = e.clientY; if (!raf) raf = requestAnimationFrame(loop); }, { passive: true });
    $$('.index .row[data-img]').forEach(row => {
      row.addEventListener('mouseenter', e => {
        if (img.getAttribute('src') !== row.dataset.img) img.src = row.dataset.img;
        if (!on) { px = x = e.clientX + 40; py = y = e.clientY; }
        on = true; peek.classList.add('is-on');
        if (!raf) raf = requestAnimationFrame(loop);
      });
      row.addEventListener('mouseleave', () => { on = false; peek.classList.remove('is-on'); });
    });
  }

  /* Lightbox for gallery */
  const lb = $('.lb');
  if (lb) {
    const lbImg = $('img', lb), lbT = $('h3', lb), lbN = $('.lb-n', lb);
    let items = [], cur = 0, opener = null;
    const show = k => {
      cur = (k + items.length) % items.length;
      const it = items[cur];
      lbImg.src = it.dataset.src; lbImg.alt = it.dataset.title;
      lbT.textContent = it.dataset.title;
      lbN.textContent = `${String(cur + 1).padStart(2, '0')} / ${String(items.length).padStart(2, '0')} · ${it.dataset.cat}`;
    };
    const close = () => { lb.classList.remove('is-on'); document.body.style.overflow = ''; opener && opener.focus(); };
    $$('.g-item').forEach(b => b.addEventListener('click', () => {
      items = $$('.g-item').filter(x => !x.hidden);
      opener = b; show(items.indexOf(b));
      lb.classList.add('is-on'); document.body.style.overflow = 'hidden';
      $('.lb-x', lb).focus();
    }));
    $('.lb-x', lb).addEventListener('click', close);
    $('[data-prev]', lb).addEventListener('click', () => show(cur - 1));
    $('[data-next]', lb).addEventListener('click', () => show(cur + 1));
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    addEventListener('keydown', e => {
      if (!lb.classList.contains('is-on')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    });
  }

  /* Consult dialog */
  const dlg = $('#consult');
  if (dlg) {
    const panes = $$('[data-pane]', dlg);
    const go = pane => panes.forEach(p => { p.hidden = p.dataset.pane !== pane; });
    const pageBiz = document.body.dataset.biz;
    $$('[data-consult]').forEach(b => b.addEventListener('click', e => {
      e.preventDefault();
      const biz = b.dataset.consult || (pageBiz !== 'home' ? pageBiz : '');
      go(biz || 'choose');
      typeof dlg.showModal === 'function' ? dlg.showModal() : dlg.setAttribute('open', '');
      track('consult_open', { biz: biz || 'choose', from: b.dataset.from || 'cta' });
    }));
    $$('[data-go]', dlg).forEach(b => b.addEventListener('click', () => {
      go(b.dataset.go);
      if (b.dataset.go !== 'choose') track('consult_open', { biz: b.dataset.go, from: 'dialog' });
    }));
    $$('.c-x', dlg).forEach(b => b.addEventListener('click', () => dlg.close()));
    dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
  }

  /* Outbound + Taobao tracking */
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="http"]');
    if (!a || a.host === location.host) return;
    track(/taobao|tb\.cn/.test(a.host) ? 'taobao_click' : 'outbound_click', { url: a.href, label: a.dataset.label || a.textContent.trim().slice(0, 40) });
  });

  /* Drag-scroll strips */
  $$('.strip').forEach(s => {
    let down = false, sx = 0, sl = 0, moved = false;
    s.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = s.scrollLeft; });
    addEventListener('pointermove', e => {
      if (!down) return;
      const dx = e.clientX - sx;
      if (Math.abs(dx) > 4) { moved = true; s.classList.add('is-drag'); }
      s.scrollLeft = sl - dx;
    });
    addEventListener('pointerup', () => { down = false; s.classList.remove('is-drag'); });
    s.addEventListener('click', e => { if (moved) e.preventDefault(); }, true);
  });
})();
