document.addEventListener('DOMContentLoaded', function () {
  const STORAGE_PREFIX = 'customizer_';
  const THEME_KEY = 'customizer_darkMode';

  function getStoredDarkMode() {
    return localStorage.getItem(THEME_KEY) === 'true';
  }

  function applyDarkMode(isDark) {
    document.body.classList.toggle('dark-mode', isDark);
    document.querySelectorAll('.theme-mode-option').forEach(el => {
      const optionIsDark = el.dataset.mode === 'dark';
      el.classList.toggle('active', optionIsDark === isDark);
    });
  }

  function setDarkMode(isDark) {
    localStorage.setItem(THEME_KEY, isDark ? 'true' : 'false');
    applyDarkMode(isDark);
  }

  applyDarkMode(getStoredDarkMode());

  document.querySelectorAll('.theme-mode-option').forEach(el => {
    el.addEventListener('click', function () {
      setDarkMode(this.dataset.mode === 'dark');
    });
  });

  const customizeToggleBtn = document.getElementById('customizeToggleBtn');
  const customizerPanel = document.getElementById('customizerPanel');
  const customizerCloseBtn = document.getElementById('customizerCloseBtn');

  if (customizeToggleBtn && customizerPanel) {
    customizeToggleBtn.addEventListener('click', () => {
      customizerPanel.classList.add('open');
    });
  }
  if (customizerCloseBtn && customizerPanel) {
    customizerCloseBtn.addEventListener('click', () => {
      customizerPanel.classList.remove('open');
    });
  }

  const layoutToggles = [
    { id: 'fixedNavbar', bodyClass: 'fixed-navbar' },
    { id: 'fixedSidebar', bodyClass: 'fixed-sidebar' },
    { id: 'sidebarMini', bodyClass: 'sidebar-mini' },
    { id: 'sidebarCompact', bodyClass: 'sidebar-compact' },
    { id: 'noNavbarBorder', bodyClass: 'no-navbar-border' },
    { id: 'navbarSmallText', bodyClass: 'navbar-small-text' },
    { id: 'footerSmallText', bodyClass: 'footer-small-text' },
  ];

  layoutToggles.forEach(({ id, bodyClass }) => {
    const checkbox = document.getElementById(id);
    if (!checkbox) return;

    const storageKey = STORAGE_PREFIX + id;
    const stored = localStorage.getItem(storageKey) === 'true';
    checkbox.checked = stored;
    document.body.classList.toggle(bodyClass, stored);

    checkbox.addEventListener('change', function () {
      localStorage.setItem(storageKey, this.checked);
      document.body.classList.toggle(bodyClass, this.checked);
    });
  });

  document.querySelectorAll('.swatch-navbar').forEach(swatch => {
    swatch.addEventListener('click', function () {
      const bg = this.dataset.bg;
      const text = this.dataset.text;
      document.documentElement.style.setProperty('--navbar-bg', bg);
      document.documentElement.style.setProperty('--navbar-text', text);
      localStorage.setItem(STORAGE_PREFIX + 'navbarBg', bg);
      localStorage.setItem(STORAGE_PREFIX + 'navbarText', text);
      document.querySelectorAll('.swatch-navbar').forEach(s => s.classList.remove('active-swatch'));
      this.classList.add('active-swatch');
    });
  });

  document.querySelectorAll('.swatch-sidebar').forEach(swatch => {
    swatch.addEventListener('click', function () {
      const color = this.dataset.color;
      document.documentElement.style.setProperty('--sidebar-bg', color);
      localStorage.setItem(STORAGE_PREFIX + 'sidebarBg', color);
      document.querySelectorAll('.swatch-sidebar').forEach(s => s.classList.remove('active-swatch'));
      this.classList.add('active-swatch');
    });
  });

  document.querySelectorAll('.swatch-theme').forEach(swatch => {
    swatch.addEventListener('click', function () {
      const color = this.dataset.color;
      document.documentElement.style.setProperty('--accent-color', color);
      localStorage.setItem(STORAGE_PREFIX + 'accentColor', color);
      document.querySelectorAll('.swatch-theme').forEach(s => s.classList.remove('active-swatch'));
      this.classList.add('active-swatch');
    });
  });

  const savedNavbarBg = localStorage.getItem(STORAGE_PREFIX + 'navbarBg');
  const savedNavbarText = localStorage.getItem(STORAGE_PREFIX + 'navbarText');
  if (savedNavbarBg) document.documentElement.style.setProperty('--navbar-bg', savedNavbarBg);
  if (savedNavbarText) document.documentElement.style.setProperty('--navbar-text', savedNavbarText);

  const savedSidebarBg = localStorage.getItem(STORAGE_PREFIX + 'sidebarBg');
  if (savedSidebarBg) document.documentElement.style.setProperty('--sidebar-bg', savedSidebarBg);

  const savedAccentColor = localStorage.getItem(STORAGE_PREFIX + 'accentColor');
  if (savedAccentColor) document.documentElement.style.setProperty('--accent-color', savedAccentColor);

  const resetThemeBtn = document.getElementById('resetThemeBtn');
  if (resetThemeBtn) {
    resetThemeBtn.addEventListener('click', function () {
      Object.keys(localStorage).forEach(key => {
        if (key.startsWith(STORAGE_PREFIX)) {
          localStorage.removeItem(key);
        }
      });
      location.reload();
    });
  }
});