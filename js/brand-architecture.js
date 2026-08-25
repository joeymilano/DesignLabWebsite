(function () {
  const html = document.documentElement;
  const body = document.body;
  const navLinks = document.querySelector('.nav-links');
  const menuButton = document.querySelector('.nav-menu-button');
  const languageButtons = document.querySelectorAll('[data-language]');

  function track(eventName, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, params || {});
    }
  }

  function applyLanguage(language) {
    const lang = language === 'en' ? 'en' : 'zh';
    html.lang = lang === 'en' ? 'en' : 'zh-CN';
    html.dataset.language = lang;

    document.querySelectorAll('[data-zh][data-en]').forEach((element) => {
      const value = lang === 'en' ? element.dataset.en : element.dataset.zh;
      if (value !== undefined) element.textContent = value;
    });

    document.querySelectorAll('[data-zh-aria][data-en-aria]').forEach((element) => {
      element.setAttribute('aria-label', lang === 'en' ? element.dataset.enAria : element.dataset.zhAria);
    });

    document.querySelectorAll('meta[data-zh-content][data-en-content]').forEach((element) => {
      element.setAttribute('content', lang === 'en' ? element.dataset.enContent : element.dataset.zhContent);
    });

    if (body.dataset.titleZh && body.dataset.titleEn) {
      document.title = lang === 'en' ? body.dataset.titleEn : body.dataset.titleZh;
    }

    languageButtons.forEach((button) => {
      const active = button.dataset.language === lang;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
    });

    try { localStorage.setItem('designlab-language', lang); } catch (_) {}
  }

  let initialLanguage = 'zh';
  try {
    const savedLanguage = localStorage.getItem('designlab-language');
    if (savedLanguage === 'en' || savedLanguage === 'zh') initialLanguage = savedLanguage;
  } catch (_) {}
  applyLanguage(initialLanguage);

  languageButtons.forEach((button) => {
    button.addEventListener('click', () => {
      applyLanguage(button.dataset.language);
      track('language_change', { language: button.dataset.language, page: body.dataset.page || 'unknown' });
    });
  });

  if (menuButton && navLinks) {
    menuButton.addEventListener('click', () => {
      const open = navLinks.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('is-open');
        menuButton.setAttribute('aria-expanded', 'false');
      });
    });
  }

  document.querySelectorAll('[data-track]').forEach((element) => {
    element.addEventListener('click', () => {
      track(element.dataset.track, {
        hub: element.dataset.hub || body.dataset.hub || 'root',
        placement: element.dataset.placement || 'unknown',
        item: element.dataset.item || ''
      });
    });
  });

  function openContactDialog(hub, source) {
    const dialog = document.getElementById('contact-' + hub);
    if (!dialog) return;
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
    track('contact_open', { hub: hub, source: source || 'unknown' });
  }

  document.querySelectorAll('[data-contact-hub]').forEach((button) => {
    button.addEventListener('click', () => openContactDialog(button.dataset.contactHub, button.dataset.placement));
  });

  document.querySelectorAll('dialog').forEach((dialog) => {
    dialog.querySelectorAll('[data-dialog-close]').forEach((button) => {
      button.addEventListener('click', () => dialog.close());
    });
    dialog.addEventListener('click', (event) => {
      if (event.target === dialog) dialog.close();
    });
  });

  const observer = 'IntersectionObserver' in window
    ? new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        });
      }, { threshold: 0.14 })
    : null;

  document.querySelectorAll('.reveal').forEach((element) => {
    if (observer) observer.observe(element);
    else element.classList.add('is-visible');
  });
})();
