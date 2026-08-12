(function () {
  const root = document.documentElement;

  const ACCENT_KEY = 'theme_accent';
  const NAVBAR_BG_KEY = 'theme_navbar_bg';
  const NAVBAR_TEXT_KEY = 'theme_navbar_text';
  const SIDEBAR_BG_KEY = 'theme_sidebar_bg';
  const DARK_MODE_KEY = 'darkMode';

  const TOGGLE_KEYS = [
    'fixedNavbar',
    'fixedSidebar',
    'sidebarMini',
    'sidebarCompact',
    'noNavbarBorder',
    'navbarSmallText',
    'footerSmallText'
  ];

  const CLASS_MAP = {
    fixedNavbar: 'fixed-navbar',
    fixedSidebar: 'fixed-sidebar',
    sidebarMini: 'sidebar-mini',
    sidebarCompact: 'sidebar-compact',
    noNavbarBorder: 'no-navbar-border',
    navbarSmallText: 'navbar-small-text',
    footerSmallText: 'footer-small-text'
  };

  const savedAccent = localStorage.getItem(ACCENT_KEY);
  const savedNavbarBg = localStorage.getItem(NAVBAR_BG_KEY);
  const savedNavbarText = localStorage.getItem(NAVBAR_TEXT_KEY);
  const savedSidebarBg = localStorage.getItem(SIDEBAR_BG_KEY);
  const savedDarkMode = localStorage.getItem(DARK_MODE_KEY) === 'true';

  if (savedAccent) root.style.setProperty('--accent-color', savedAccent);
  if (savedNavbarBg) root.style.setProperty('--navbar-bg', savedNavbarBg);
  if (savedNavbarText) root.style.setProperty('--navbar-text', savedNavbarText);
  if (savedSidebarBg) root.style.setProperty('--sidebar-bg', savedSidebarBg);

  // Apply dark mode as early as possible (before DOMContentLoaded) to avoid
  // a flash of light mode on page load.
  if (savedDarkMode) {
    document.documentElement.classList.add('dark-mode-pending');
  }

  document.addEventListener('DOMContentLoaded', function () {

    // ---- Dark mode ----
    if (savedDarkMode) {
      document.body.classList.add('dark-mode');
    }
    document.documentElement.classList.remove('dark-mode-pending');

    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
      darkModeToggle.checked = savedDarkMode;
      darkModeToggle.addEventListener('change', function () {
        document.body.classList.toggle('dark-mode', this.checked);
        localStorage.setItem(DARK_MODE_KEY, this.checked);
      });
    }

    // ---- Layout toggles ----
    TOGGLE_KEYS.forEach(function (key) {
      const saved = localStorage.getItem(key);
      const isOn = saved === 'true';
      const checkbox = document.getElementById(key);
      if (checkbox) checkbox.checked = isOn;
      document.body.classList.toggle(CLASS_MAP[key], isOn);
    });

    TOGGLE_KEYS.forEach(function (key) {
      const checkbox = document.getElementById(key);
      if (!checkbox) return;
      checkbox.addEventListener('change', function () {
        document.body.classList.toggle(CLASS_MAP[key], this.checked);
        localStorage.setItem(key, this.checked);
      });
    });

    // ---- Theme accent swatches ----
    document.querySelectorAll('.swatch-theme').forEach(function (el) {
      if (el.dataset.color === savedAccent) el.classList.add('active-swatch');
      el.addEventListener('click', function () {
        const color = this.dataset.color;
        root.style.setProperty('--accent-color', color);
        localStorage.setItem(ACCENT_KEY, color);
        document.querySelectorAll('.swatch-theme').forEach(s => s.classList.remove('active-swatch'));
        this.classList.add('active-swatch');
      });
    });

    // ---- Navbar color swatches ----
    document.querySelectorAll('.swatch-navbar').forEach(function (el) {
      if (el.dataset.bg === savedNavbarBg) el.classList.add('active-swatch');
      el.addEventListener('click', function () {
        const bg = this.dataset.bg;
        const text = this.dataset.text;
        root.style.setProperty('--navbar-bg', bg);
        root.style.setProperty('--navbar-text', text);
        localStorage.setItem(NAVBAR_BG_KEY, bg);
        localStorage.setItem(NAVBAR_TEXT_KEY, text);
        document.querySelectorAll('.swatch-navbar').forEach(s => s.classList.remove('active-swatch'));
        this.classList.add('active-swatch');
      });
    });

    // ---- Sidebar color swatches ----
    document.querySelectorAll('.swatch-sidebar').forEach(function (el) {
      if (el.dataset.color === savedSidebarBg) el.classList.add('active-swatch');
      el.addEventListener('click', function () {
        const color = this.dataset.color;
        root.style.setProperty('--sidebar-bg', color);
        localStorage.setItem(SIDEBAR_BG_KEY, color);
        document.querySelectorAll('.swatch-sidebar').forEach(s => s.classList.remove('active-swatch'));
        this.classList.add('active-swatch');
      });
    });

    // ---- Panel open/close ----
    const toggleBtn = document.getElementById('customizeToggleBtn');
    const panel = document.getElementById('customizerPanel');
    const closeBtn = document.getElementById('customizerCloseBtn');

    if (toggleBtn && panel) {
      toggleBtn.addEventListener('click', function () {
        panel.classList.toggle('open');
      });
    }
    if (closeBtn && panel) {
      closeBtn.addEventListener('click', function () {
        panel.classList.remove('open');
      });
    }

    // ---- Reset ----
    const resetBtn = document.getElementById('resetThemeBtn');
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        [ACCENT_KEY, NAVBAR_BG_KEY, NAVBAR_TEXT_KEY, SIDEBAR_BG_KEY, DARK_MODE_KEY].forEach(k => localStorage.removeItem(k));
        TOGGLE_KEYS.forEach(key => localStorage.removeItem(key));
        window.location.reload();
      });
    }
  });
})();