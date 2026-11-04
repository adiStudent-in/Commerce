/* Retail unit pages — dependency-free interactions for Easy Notes + Quick Revision. */
(function () {
  'use strict';

  var root = document.documentElement;
  var body = document.body;
  var themeToggle = document.getElementById('themeToggle');
  var themeIcon = themeToggle ? themeToggle.querySelector('.theme-icon') : null;
  var themeMeta = document.querySelector('meta[name="theme-color"]');
  var toc = document.getElementById('toc');
  var tocToggle = document.getElementById('tocToggle');
  var progressFill = document.getElementById('progressFill');
  var modeBar = document.getElementById('study-modes');
  var modeHint = document.getElementById('modeHint');
  var tocModeLabel = document.getElementById('tocModeLabel');
  var printToggle = document.querySelector('.print-toggle');

  var MODE_KEY = 'study-os-retail-mode';
  var currentMode = root.dataset.retailMode === 'quick' ? 'quick' : 'notes';

  var MODE_META = {
    notes: {
      label: 'Easy Notes',
      hint: 'You are reading the full notes. Switch to Quick Revision for a 25-minute recall session.',
      print: 'Print Easy Notes'
    },
    quick: {
      label: 'Quick Revision',
      hint: 'You are in Quick Revision. Answers stay hidden until you reveal them — switch to Easy Notes for the full explanations.',
      print: 'Print Quick Revision'
    }
  };

  function qsa(selector, scope) {
    return Array.prototype.slice.call((scope || document).querySelectorAll(selector));
  }

  function on(element, type, handler, options) {
    if (element) element.addEventListener(type, handler, options);
  }

  function prefersReducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  /* ---------- theme ---------- */

  function storedTheme() {
    try {
      var raw = localStorage.getItem('study-os-theme');
      if (!raw) return null;
      try { return JSON.parse(raw); } catch (e) { return raw; }
    } catch (e) {
      return null;
    }
  }

  function applyTheme(theme) {
    var dark = theme === 'dark';
    if (dark) root.dataset.theme = 'dark';
    else delete root.dataset.theme;
    if (themeIcon) themeIcon.textContent = dark ? '☀' : '☾';
    if (themeToggle) {
      themeToggle.setAttribute('aria-pressed', dark ? 'true' : 'false');
      themeToggle.setAttribute('title', dark ? 'Switch to light mode' : 'Switch to dark mode');
      themeToggle.setAttribute('aria-label', themeToggle.getAttribute('title'));
    }
    if (themeMeta) themeMeta.setAttribute('content', dark ? '#121613' : '#1a5e4a');
  }

  applyTheme(root.dataset.theme === 'dark' ? 'dark' : (storedTheme() === 'dark' ? 'dark' : 'light'));

  on(themeToggle, 'click', function () {
    var next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem('study-os-theme', JSON.stringify(next)); } catch (e) { /* private mode */ }
  });

  /* ---------- reading progress ---------- */

  function updateProgress() {
    if (!progressFill) return;
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    var pct = max > 0 ? (window.scrollY / max) * 100 : 0;
    progressFill.style.width = Math.min(100, Math.max(0, pct)) + '%';
  }

  var progressQueued = false;
  on(window, 'scroll', function () {
    if (progressQueued) return;
    progressQueued = true;
    window.requestAnimationFrame(function () {
      progressQueued = false;
      updateProgress();
    });
  }, { passive: true });
  on(window, 'resize', updateProgress, { passive: true });
  updateProgress();

  /* ---------- mobile contents drawer ---------- */

  function keepActiveVisible(link) {
    if (!link || !toc) return;
    /* Desktop keeps the active link in view. The mobile drawer always opens
       at the top — auto-following during its height transition used to scroll
       the header out of the drawer before it had even expanded. */
    if (window.innerWidth <= 980) return;
    if (toc.scrollHeight <= toc.clientHeight + 4) return;
    var tocRect = toc.getBoundingClientRect();
    var linkRect = link.getBoundingClientRect();
    if (linkRect.top < tocRect.top + 4) {
      toc.scrollTop -= (tocRect.top + 4 - linkRect.top);
    } else if (linkRect.bottom > tocRect.bottom - 4) {
      toc.scrollTop += (linkRect.bottom - (tocRect.bottom - 4));
    }
  }

  function setDrawer(open) {
    if (!toc || !tocToggle) return;
    toc.classList.toggle('open', open);
    tocToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    tocToggle.innerHTML = open
      ? '<span aria-hidden="true">✕</span> Close'
      : '<span aria-hidden="true">☰</span> Contents';
    if (open) toc.scrollTop = 0;
  }

  on(tocToggle, 'click', function (event) {
    event.stopPropagation();
    setDrawer(!toc.classList.contains('open'));
  });

  on(toc, 'click', function (event) {
    if (event.target.closest('a')) setDrawer(false);
  });

  on(document, 'click', function (event) {
    if (!toc || !toc.classList.contains('open')) return;
    if (toc.contains(event.target) || (tocToggle && tocToggle.contains(event.target))) return;
    setDrawer(false);
  });

  on(document, 'keydown', function (event) {
    if (event.key === 'Escape') setDrawer(false);
  });

  on(window, 'resize', function () {
    if (window.innerWidth > 980) setDrawer(false);
  }, { passive: true });

  /* ---------- table of contents scrollspy ---------- */

  var spyTargets = [];
  var spyLinks = [];
  var spyActive = null;

  function setSpy(target) {
    if (spyActive === target) return;
    spyActive = target;
    var activeLink = null;
    spyTargets.forEach(function (item) {
      item.links.forEach(function (link) {
        var isActive = item === target;
        link.classList.toggle('active', isActive);
        if (isActive) {
          link.setAttribute('aria-current', 'location');
          if (!activeLink) activeLink = link;
        } else {
          link.removeAttribute('aria-current');
        }
      });
    });
    keepActiveVisible(activeLink);
  }

  function updateSpy() {
    if (!spyTargets.length) return;
    /* Keep this just under the 96px scroll-padding so a heading that was
       just scrolled to is the one that lights up, not the one before it. */
    var y = window.scrollY + 100;
    var current = spyTargets[0];
    spyTargets.forEach(function (target) {
      var top = target.el.getBoundingClientRect().top + window.scrollY;
      if (top <= y) current = target;
    });
    if ((window.innerHeight + window.scrollY) >= document.documentElement.scrollHeight - 4) {
      current = spyTargets[spyTargets.length - 1];
    }
    setSpy(current);
  }

  function rebuildSpy() {
    if (!toc) return;
    var nav = toc.querySelector('.toc-nav[data-mode-nav="' + currentMode + '"]');
    spyLinks = nav ? qsa('a[href^="#"]', nav) : [];
    spyTargets = [];
    spyActive = null;

    qsa('.toc-link', toc).forEach(function (link) {
      link.classList.remove('active');
      link.removeAttribute('aria-current');
    });

    spyLinks.forEach(function (link) {
      var id = decodeURIComponent(link.getAttribute('href').slice(1));
      var element = document.getElementById(id);
      if (!element) return;
      var existing = spyTargets.filter(function (target) { return target.el === element; })[0];
      if (existing) {
        existing.links.push(link);
      } else {
        spyTargets.push({ el: element, links: [link] });
      }
    });

    spyTargets.sort(function (a, b) {
      return a.el.compareDocumentPosition(b.el) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
    });

    spyLinks.forEach(function (link) {
      on(link, 'click', function () {
        var target = spyTargets.filter(function (item) { return item.links.indexOf(link) !== -1; })[0];
        if (target) setSpy(target);
      });
    });

    updateSpy();
  }

  var spyQueued = false;
  on(window, 'scroll', function () {
    if (spyQueued) return;
    spyQueued = true;
    window.requestAnimationFrame(function () {
      spyQueued = false;
      updateSpy();
    });
  }, { passive: true });
  on(window, 'resize', updateSpy, { passive: true });

  /* ---------- mode switching ---------- */

  function normalizeMode(value) {
    return value === 'quick' ? 'quick' : 'notes';
  }

  function modeFromHash(hash) {
    var value = String(hash || '').replace(/^#/, '');
    if (value.indexOf('q-') === 0 || value === 'quick') return 'quick';
    if (value.indexOf('n-') === 0 || value === 'notes') return 'notes';
    return null;
  }

  function clearHash() {
    try {
      if (location.hash) {
        history.replaceState(null, '', location.pathname + location.search);
      }
    } catch (e) { /* file:// history can be restricted */ }
  }

  function scrollToModeBar() {
    /* The old mode console was removed from these pages; fall back to the top
       of the content so switching modes from the header still lands cleanly. */
    var target = modeBar || document.getElementById('main');
    if (!target) return;
    try {
      target.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'start' });
    } catch (e) {
      target.scrollIntoView();
    }
  }

  var modeAnimationTimer = null;

  function animatePanel(panel) {
    if (!panel) return;
    panel.classList.remove('is-entering');
    /* Force a reflow so switching modes repeatedly replays the entrance. */
    void panel.offsetWidth;
    panel.classList.add('is-entering');
    window.clearTimeout(modeAnimationTimer);
    modeAnimationTimer = window.setTimeout(function () {
      panel.classList.remove('is-entering');
    }, 340);
  }

  function applyMode(mode, options) {
    options = options || {};
    mode = normalizeMode(mode);
    var changed = mode !== currentMode;
    currentMode = mode;
    root.dataset.retailMode = mode;

    qsa('.mode-panel').forEach(function (panel) {
      panel.hidden = panel.getAttribute('data-mode') !== mode;
    });

    qsa('[data-mode-nav]').forEach(function (nav) {
      nav.hidden = nav.getAttribute('data-mode-nav') !== mode;
    });

    qsa('[data-set-mode]').forEach(function (button) {
      var active = button.getAttribute('data-set-mode') === mode;
      if (button.getAttribute('role') === 'tab') {
        button.setAttribute('aria-selected', active ? 'true' : 'false');
        button.tabIndex = active ? 0 : -1;
      } else {
        button.setAttribute('aria-pressed', active ? 'true' : 'false');
      }
    });

    var meta = MODE_META[mode];
    if (modeHint) modeHint.textContent = meta.hint;
    if (tocModeLabel) tocModeLabel.textContent = meta.label;
    if (printToggle) {
      printToggle.setAttribute('title', meta.print);
      printToggle.setAttribute('aria-label', meta.print);
    }

    var baseTitle = body.getAttribute('data-base-title') || document.title.split(' | ')[0];
    var subjectLabel = body.getAttribute('data-subject') || 'Retail';
    document.title = baseTitle + ' | ' + subjectLabel + ' ' + meta.label;

    if (options.persist) {
      try { localStorage.setItem(MODE_KEY, mode); } catch (e) { /* private mode */ }
    }

    if (changed) {
      rebuildSpy();
      if (options.animate !== false) {
        animatePanel(document.getElementById('panel-' + mode));
      }
    }

    window.requestAnimationFrame(function () {
      updateProgress();
      updateSpy();
    });
    window.setTimeout(function () {
      updateProgress();
      updateSpy();
    }, 320);

    if (options.scroll) {
      window.requestAnimationFrame(scrollToModeBar);
    }
  }

  qsa('[data-set-mode]').forEach(function (button) {
    on(button, 'click', function () {
      var mode = normalizeMode(button.getAttribute('data-set-mode'));
      if (mode === currentMode) {
        scrollToModeBar();
        return;
      }
      clearHash();
      applyMode(mode, { persist: true, scroll: true, animate: true });
    });
  });

  qsa('[data-mode-jump]').forEach(function (button) {
    on(button, 'click', function () {
      clearHash();
      applyMode(button.getAttribute('data-mode-jump'), { persist: true, scroll: true, animate: true });
    });
  });

  var modeTabs = document.querySelector('.mode-tabs');
  on(modeTabs, 'keydown', function (event) {
    var tabs = qsa('[role="tab"]', modeTabs);
    var index = tabs.indexOf(document.activeElement);
    if (index === -1) return;
    var next = null;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
    else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + tabs.length) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    if (next === null) return;
    event.preventDefault();
    tabs[next].focus();
    tabs[next].click();
  });

  function scrollToHashTarget(behavior) {
    var id = decodeURIComponent(String(location.hash || '').replace(/^#/, ''));
    if (!id) return;
    var target = document.getElementById(id);
    if (!target) return;
    if (behavior === 'instant') {
      /* A deep link must not inherit `scroll-behavior: smooth`; a webfont swap
         mid-animation would land the target tens of pixels off. */
      try {
        target.scrollIntoView({ behavior: 'instant', block: 'start' });
      } catch (e) {
        var html = document.documentElement;
        var previous = html.style.scrollBehavior;
        html.style.scrollBehavior = 'auto';
        target.scrollIntoView();
        html.style.scrollBehavior = previous;
      }
      return;
    }
    try {
      target.scrollIntoView({ behavior: behavior, block: 'start' });
    } catch (e) {
      target.scrollIntoView();
    }
  }

  on(window, 'hashchange', function () {
    var mode = modeFromHash(location.hash);
    if (mode && mode !== currentMode) {
      applyMode(mode, { persist: false, animate: true });
    }
    window.requestAnimationFrame(function () {
      scrollToHashTarget(prefersReducedMotion() ? 'auto' : 'smooth');
    });
  });

  /* Initial paint: the inline head script already picked storage/hash. */
  applyMode(currentMode, { persist: false, animate: false });
  rebuildSpy();

  if (location.hash) {
    var initialMode = modeFromHash(location.hash);
    if (initialMode && initialMode !== currentMode) {
      applyMode(initialMode, { persist: false, animate: false });
    }

    /* Deep links can land before the webfonts finish swapping, which changes
       section heights. Align instantly, then again once fonts and the load
       event have settled. Any real user input cancels the correction. */
    var hashUserMoved = false;
    ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(function (type) {
      on(window, type, function () { hashUserMoved = true; }, { passive: true });
    });

    function realignHash() {
      if (hashUserMoved) return;
      scrollToHashTarget('instant');
    }

    window.requestAnimationFrame(realignHash);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () {
        window.requestAnimationFrame(realignHash);
        window.setTimeout(realignHash, 80);
      });
    }
    if (document.readyState === 'complete') {
      window.setTimeout(realignHash, 0);
    } else {
      on(window, 'load', function () {
        window.setTimeout(realignHash, 0);
        window.setTimeout(realignHash, 260);
      });
    }
  }

  /* ---------- exam answer controls ---------- */

  var qaItems = qsa('#panel-notes .qa');
  var openAll = document.getElementById('openAllQa');
  var closeAll = document.getElementById('closeAllQa');

  function setAllQa(open) {
    qaItems.forEach(function (item) { item.open = open; });
  }

  on(openAll, 'click', function () { setAllQa(true); });
  on(closeAll, 'click', function () { setAllQa(false); });

  /* ---------- recall drills ---------- */

  qsa('.drill').forEach(function (drill) {
    var button = drill.querySelector('[data-drill-toggle]');
    var answers = qsa('.drill-answer', drill);
    if (!button || !answers.length) return;

    function syncDrillButton() {
      var allOpen = answers.every(function (item) { return item.open; });
      button.setAttribute('aria-expanded', allOpen ? 'true' : 'false');
      button.textContent = allOpen ? 'Close all answers' : 'Open all answers';
    }

    function setDrill(open) {
      answers.forEach(function (item) { item.open = open; });
      syncDrillButton();
    }

    on(button, 'click', function () {
      var allOpen = answers.every(function (item) { return item.open; });
      setDrill(!allOpen);
    });

    answers.forEach(function (item) {
      on(item, 'toggle', syncDrillButton);
    });

    syncDrillButton();
  });

  /* ---------- rapid fire: cover / reveal ---------- */

  qsa('[data-cover-answers]').forEach(function (button) {
    var block = button.closest('.rapid-block');
    var table = block ? block.querySelector('.rapid-table') : null;
    if (!table) return;
    var cells = qsa('tbody td:last-child', table);
    var covered = false;

    function revealCell(cell) {
      if (!covered) return;
      cell.classList.add('is-revealed');
      cell.removeAttribute('title');
    }

    function setCovered(next) {
      covered = next;
      table.classList.toggle('is-covered', covered);
      button.setAttribute('aria-pressed', covered ? 'true' : 'false');
      button.textContent = covered ? 'Reveal all' : 'Cover answers';
      cells.forEach(function (cell) {
        cell.classList.remove('is-revealed');
        if (covered) {
          cell.tabIndex = 0;
          cell.setAttribute('title', 'Tap or press Enter to reveal this answer');
        } else {
          cell.removeAttribute('tabindex');
          cell.removeAttribute('title');
        }
      });
    }

    on(button, 'click', function () { setCovered(!covered); });

    cells.forEach(function (cell) {
      on(cell, 'click', function () { revealCell(cell); });
      on(cell, 'keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ' || event.key === 'Spacebar') {
          event.preventDefault();
          revealCell(cell);
        }
      });
    });

    setCovered(false);
  });

  /* ---------- blank page test ---------- */

  var blankBlock = document.querySelector('.blank-block');
  if (blankBlock) {
    var blankBoxes = qsa('[data-blank]', blankBlock);
    var blankCount = blankBlock.querySelector('[data-blank-count]');
    var blankBar = blankBlock.querySelector('[data-blank-bar]');
    var blankReset = blankBlock.querySelector('[data-blank-reset]');
    var blankMeter = blankBlock.querySelector('.blank-meter');
    var blankKey = 'study-os-retail-blank-' + (body.getAttribute('data-unit') || 'unit');

    function readBlankState() {
      try {
        var raw = localStorage.getItem(blankKey);
        if (!raw) return {};
        var parsed = JSON.parse(raw);
        return parsed && typeof parsed === 'object' ? parsed : {};
      } catch (e) {
        return {};
      }
    }

    function saveBlankState() {
      var state = {};
      blankBoxes.forEach(function (box) {
        if (box.checked) state[box.id] = true;
      });
      try { localStorage.setItem(blankKey, JSON.stringify(state)); } catch (e) { /* private mode */ }
    }

    function updateBlankMeter() {
      var total = blankBoxes.length;
      var done = blankBoxes.filter(function (box) { return box.checked; }).length;
      var pct = total ? Math.round((done / total) * 100) : 0;
      if (blankCount) {
        blankCount.textContent = done + ' / ' + total + ' complete';
        blankCount.setAttribute('aria-live', 'polite');
      }
      if (blankBar) blankBar.style.width = pct + '%';
      if (blankMeter) blankMeter.classList.toggle('is-complete', total > 0 && done === total);
      blankBoxes.forEach(function (box) {
        var label = box.closest('.blank-item');
        if (label) label.classList.toggle('is-done', box.checked);
      });
    }

    var savedBlank = readBlankState();
    blankBoxes.forEach(function (box) {
      box.checked = !!(savedBlank[box.id] || savedBlank[box.getAttribute('data-blank')]);
      on(box, 'change', function () {
        updateBlankMeter();
        saveBlankState();
      });
    });
    updateBlankMeter();

    on(blankReset, 'click', function () {
      blankBoxes.forEach(function (box) { box.checked = false; });
      updateBlankMeter();
      try { localStorage.removeItem(blankKey); } catch (e) { /* private mode */ }
    });
  }

  /* ---------- print ---------- */

  on(printToggle, 'click', function () { window.print(); });

  var printState = null;

  function printableDetails() {
    return qsa('details').filter(function (item) {
      return !item.closest('[hidden]');
    });
  }

  on(window, 'beforeprint', function () {
    var items = printableDetails();
    printState = items.map(function (item) { return item.open; });
    items.forEach(function (item) { item.open = true; });
  });

  on(window, 'afterprint', function () {
    if (!printState) return;
    var items = printableDetails();
    items.forEach(function (item, index) {
      if (typeof printState[index] === 'boolean') item.open = printState[index];
    });
    printState = null;
  });
})();
