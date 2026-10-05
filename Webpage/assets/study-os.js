/**
 * study-os.js — Study OS for Class 11 Commerce
 * Shared interactive features for all chapter pages and dashboard.
 * Initializes automatically on DOMContentLoaded.
 */
(function () {
  'use strict';

  /* ───────── HELPERS ───────── */

  function log(msg) {
    console.warn('[Study OS]', msg);
  }

  function getChapterId() {
    // Try meta tag
    var meta = document.querySelector('meta[name="chapter-id"]');
    if (meta) return meta.getAttribute('content');
    // Try script data attribute
    var script = document.getElementById('chapter-data');
    if (script && script.dataset.chapter) return script.dataset.chapter;
    // Infer from URL path
    var path = window.location.pathname;
    var m = path.match(/(?:BST|Economics|Statistics)\/(?:Chapter-(\d+)|[^/]+)/i);
    if (m && m[1]) {
      var prefix = 'bst';
      if (path.indexOf('/Economics/') !== -1) prefix = 'econ';
      else if (path.indexOf('/Statistics/') !== -1) prefix = 'stat';
      return prefix + '-' + m[1];
    }
    // Fallback to page title
    var title = document.title;
    var t = title.match(/Chapter\s*(\d+)/i);
    if (t) {
      var p = 'bst';
      if (/economics/i.test(title)) p = 'econ';
      else if (/statistics/i.test(title)) p = 'stat';
      return p + '-' + t[1];
    }
    return null;
  }

  function saveProgress(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      log('localStorage unavailable for ' + key);
    }
  }

  function loadProgress(key, defaultValue) {
    try {
      var raw = localStorage.getItem(key);
      return raw !== null ? JSON.parse(raw) : defaultValue;
    } catch (e) {
      return defaultValue;
    }
  }

  function debounce(fn, ms) {
    var timer = null;
    return function () {
      var ctx = this, args = arguments;
      if (timer) clearTimeout(timer);
      timer = setTimeout(function () { fn.apply(ctx, args); }, ms);
    };
  }

  function qs(sel, ctx) { return (ctx || document).querySelector(sel); }

  function qsa(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ───────── 1. DARK MODE ───────── */

  function initDarkMode() {
    try {
      var saved = loadProgress('study-os-theme', null);
      if (saved === 'dark') {
        document.documentElement.dataset.theme = 'dark';
      }
      var toggles = qsa('.dark-toggle');
      if (!toggles.length) return;

      function updateToggles() {
        var isDark = document.documentElement.dataset.theme === 'dark';
        toggles.forEach(function (btn) {
          btn.textContent = isDark ? '☀️' : '🌙';
          btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
        });
      }

      toggles.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var isDark = document.documentElement.dataset.theme === 'dark';
          var next = isDark ? 'light' : 'dark';
          if (next === 'dark') {
            document.documentElement.dataset.theme = 'dark';
          } else {
            delete document.documentElement.dataset.theme;
          }
          saveProgress('study-os-theme', next === 'dark' ? 'dark' : null);
          updateToggles();
        });
      });

      updateToggles();
    } catch (e) { log('Dark mode init error: ' + e.message); }
  }

  /* ───────── 2. REVISION MODE ───────── */

  function initRevisionMode() {
    try {
      var saved = loadProgress('study-os-revision', false);
      if (saved === true || saved === 'true') {
        document.body.classList.add('revision-mode');
      }
      var toggles = qsa('.revision-toggle');
      if (!toggles.length) return;

      function updateToggles() {
        var active = document.body.classList.contains('revision-mode');
        toggles.forEach(function (btn) {
          btn.textContent = active ? '📚 Read' : '📖 Revise';
          btn.classList.toggle('active', active);
        });
      }

      toggles.forEach(function (btn) {
        btn.addEventListener('click', function () {
          document.body.classList.toggle('revision-mode');
          var active = document.body.classList.contains('revision-mode');
          saveProgress('study-os-revision', active);
          updateToggles();
        });
      });

      updateToggles();
    } catch (e) { log('Revision mode init error: ' + e.message); }
  }

  /* ───────── 6. SEARCH ───────── */

  function initSearch() {
    try {
      // Build index from current page
      var index = buildSearchIndex();
      var overlay = qs('.search-overlay');
      var modal = qs('.search-modal');
      if (!overlay || !modal) return;

      var toggles = qsa('.search-toggle');
      var input = qs('.search-input-wrap input', modal);
      var closeBtn = qs('.search-close', modal);
      var resultsContainer = qs('.search-results', modal);

      if (!input || !resultsContainer) return;

      function openSearch() {
        overlay.classList.add('active');
        setTimeout(function () { input.focus(); }, 100);
        document.body.style.overflow = 'hidden';
      }

      function closeSearch() {
        overlay.classList.remove('active');
        input.value = '';
        resultsContainer.innerHTML = '';
        document.body.style.overflow = '';
      }

      toggles.forEach(function (btn) {
        btn.addEventListener('click', openSearch);
      });

      if (closeBtn) closeBtn.addEventListener('click', closeSearch);
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeSearch();
      });

      function performSearch(query) {
        if (!query.trim()) {
          resultsContainer.innerHTML = '';
          return;
        }
        var q = query.toLowerCase().trim();
        var results = [];

        index.forEach(function (item) {
          var titleMatch = item.title && item.title.toLowerCase().indexOf(q) !== -1;
          var headingMatch = item.headings && item.headings.some(function (h) { return h.toLowerCase().indexOf(q) !== -1; });
          var contentMatch = item.content && item.content.toLowerCase().indexOf(q) !== -1;
          if (titleMatch || headingMatch || contentMatch) {
            results.push(item);
          }
        });

        if (!results.length) {
          resultsContainer.innerHTML = '<div class="search-empty">No results found for "' + escapeHtml(query.trim()) + '"</div>';
          return;
        }

        var html = '';
        results.forEach(function (r) {
          // Highlight match in context
          var ctx = r.content ? r.content.substring(0, 150) : '';
          var idx2 = ctx.toLowerCase().indexOf(q);
          var displayCtx = '';
          if (idx2 !== -1) {
            var start = Math.max(0, idx2 - 40);
            var end = Math.min(ctx.length, idx2 + 80);
            var before = ctx.substring(start, idx2);
            var match = ctx.substring(idx2, idx2 + q.length);
            var after = ctx.substring(idx2 + q.length, end);
            displayCtx = (start > 0 ? '...' : '') + escapeHtml(before) + '<em>' + escapeHtml(match) + '</em>' + escapeHtml(after) + (end < ctx.length ? '...' : '');
          } else {
            displayCtx = escapeHtml(ctx.substring(0, 150)) + (ctx.length > 150 ? '...' : '');
          }

          var headingLabel = r.section || 'Page content';
          var href = r.url || (r.id ? '#' + r.id : '#');

          html += '<a href="' + href + '" class="search-result-item" data-section-id="' + (r.id || '') + '" data-url="' + (r.url || '') + '">';
          html += '  <div class="sr-title">' + escapeHtml(r.title || headingLabel) + '</div>';
          html += '  <div class="sr-context">' + displayCtx + '</div>';
          html += '  <div class="sr-meta">' + escapeHtml(headingLabel) + '</div>';
          html += '</a>';
        });
        resultsContainer.innerHTML = html;

        // Click handler for navigation or smooth scroll
        qsa('.search-result-item', resultsContainer).forEach(function (item) {
          item.addEventListener('click', function (e) {
            e.preventDefault();
            var url = item.getAttribute('data-url');
            var id = item.getAttribute('data-section-id');
            if (url) {
              window.location.href = url;
              return;
            }
            if (id) {
              var target = document.getElementById(id);
              if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            }
            closeSearch();
          });
        });
      }

      input.addEventListener('keyup', debounce(function () {
        performSearch(input.value);
      }, 200));

      // Keyboard close/open
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && overlay.classList.contains('active')) {
          closeSearch();
        }
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
          e.preventDefault();
          if (overlay.classList.contains('active')) closeSearch();
          else openSearch();
        }
      });
    } catch (e) { log('Search init error: ' + e.message); }
  }

  function buildSearchIndex() {
    var index = [];
    try {
      var title = document.title || '';
      var metaDesc = '';
      var metaTag = document.querySelector('meta[name="description"]');
      if (metaTag) metaDesc = metaTag.getAttribute('content') || '';

      var mainContent = qs('main.content') || document.body;

      // Page-level entry
      index.push({
        id: '',
        title: title,
        headings: [],
        content: metaDesc || title,
        section: 'Page',
        url: ''
      });

      // Section-level entries (chapter pages — sections have IDs)
      qsa('section[id]', mainContent).forEach(function (section) {
        var h2 = qs('h2', section);
        var h3 = qs('h3', section);
        var headingText = (h2 ? h2.textContent : (h3 ? h3.textContent : '')).trim();
        var text = section.textContent.replace(/\s+/g, ' ').trim().substring(0, 300);

        index.push({
          id: section.getAttribute('id'),
          title: headingText || section.getAttribute('id'),
          headings: [headingText],
          content: text,
          section: headingText || 'Section',
          url: ''
        });
      });

      // Index h2/h3 elements outside sections
      qsa('h2[id], h3[id]', mainContent).forEach(function (el) {
        var parentSec = el.closest('section');
        if (parentSec) return;
        index.push({
          id: el.getAttribute('id'),
          title: el.textContent.trim(),
          headings: [el.textContent.trim()],
          content: (el.nextElementSibling ? el.nextElementSibling.textContent : '').replace(/\s+/g, ' ').trim().substring(0, 150),
          section: 'Sub-section',
          url: ''
        });
      });

      // Hub page fallback: index accordion content (chapter links, subject names)
      qsa('.chapter-item', document).forEach(function (item) {
        var titleEl = qs('.ch-title', item);
        var metaEl = qs('.ch-meta', item);
        var numEl = qs('.ch-num', item);
        var subjectPanel = item.closest('.subject-wrap');
        var subjectName = subjectPanel ? (qs('.name', subjectPanel) || {}).textContent || '' : '';
        var href = item.getAttribute('href') || '';
        index.push({
          id: '',
          title: (titleEl ? titleEl.textContent : '').trim(),
          headings: [subjectName, (titleEl ? titleEl.textContent : '').trim()],
          content: (metaEl ? metaEl.textContent : '') + ' ' + subjectName + ' ' + (numEl ? numEl.textContent : ''),
          section: subjectName || 'Chapter',
          url: href
        });
      });
    } catch (e) { log('Search index build error: ' + e.message); }
    return index;
  }

  function escapeHtml(str) {
    if (!str) return '';
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  /* ───────── 7. KEY TERMS OVERLAY ───────── */

  function initKeyTerms() {
    try {
      var toggles = qsa('.terms-toggle');
      if (!toggles.length) return;

      var overlay = qs('.terms-overlay');
      var modal = qs('.terms-modal');
      if (!overlay || !modal) {
        log('terms-overlay or terms-modal not found in DOM');
        return;
      }

      var closeBtn = qs('.close-btn', modal);
      var termsContainer = qs('.terms-grid-overlay', modal);

      function loadTerms() {
        var terms = null;
        // Try inline script tag
        var dataScript = document.getElementById('chapter-terms-data');
        if (dataScript) {
          try {
            terms = JSON.parse(dataScript.textContent);
          } catch (e) { log('Failed to parse chapter-terms-data JSON'); }
        }
        // Try window var
        if (!terms && typeof window.CHAPTER_TERMS !== 'undefined') {
          terms = window.CHAPTER_TERMS;
        }
        return terms;
      }

      function renderTerms(terms) {
        if (!termsContainer) return;
        if (!terms || !terms.length) {
          termsContainer.innerHTML = '<p style="color:var(--text-muted);text-align:center;">No key terms available for this chapter.</p>';
          return;
        }
        var html = '';
        terms.forEach(function (t) {
          var name = t.name || t.term || '';
          var def = t.definition || t.def || t.description || '';
          html += '<div class="term-card"><strong>' + escapeHtml(name) + '</strong><span>' + escapeHtml(def) + '</span></div>';
        });
        termsContainer.innerHTML = html;
      }

      toggles.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var terms = loadTerms();
          renderTerms(terms);
          overlay.classList.add('active');
          document.body.style.overflow = 'hidden';
        });
      });

      function closeTerms() {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      }

      if (closeBtn) closeBtn.addEventListener('click', closeTerms);
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeTerms();
      });

      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && overlay.classList.contains('active')) closeTerms();
      });
    } catch (e) { log('Key terms init error: ' + e.message); }
  }

  /* ───────── 15. PWA ───────── */

  function initPWA() {
    try {
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./service-worker.js')
          .then(function (reg) { log('SW registered: ' + reg.scope); })
          .catch(function (err) { log('SW registration failed: ' + err); });
      }

      window.addEventListener('appinstalled', function () {
        log('App installed');
      });
    } catch (e) { log('PWA init error: ' + e.message); }
  }

  /* ───────── 10. PRINT ───────── */

  function initPrint() {
    try {
      var toggles = qsa('.print-toggle');
      toggles.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
          e.preventDefault();
          window.print();
        });
      });
    } catch (e) { log('Print init error: ' + e.message); }
  }

  /* ───────── 10.5 MIND MAP OVERLAY ───────── */

  var mmOverlayBuilt = false;

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error('Failed to load ' + src)); };
      document.head.appendChild(s);
    });
  }

  // Lazy-load markmap deps once and cache the promise. markmap-lib and
  // markmap-view share the `window.markmap` global (view clobbers lib), so we
  // capture Transformer right after markmap-lib loads.
  var mmLibPromise = null;
  function loadMarkmapLib() {
    if (!mmLibPromise) {
      mmLibPromise = loadScript('https://cdn.jsdelivr.net/npm/d3@7')
        .then(function () { return loadScript('https://cdn.jsdelivr.net/npm/markmap-lib@0.18.12'); })
        .then(function () {
          var wm = window.markmap || {};
          return wm.Transformer ? wm.Transformer : null;
        });
    }
    return mmLibPromise;
  }

  var mmViewPromise = null;
  function loadMarkmapView() {
    if (!mmViewPromise) {
      mmViewPromise = loadMarkmapLib()
        .then(function () {
          return loadScript('https://cdn.jsdelivr.net/npm/markmap-view@0.18.12');
        })
        .then(function () {
          var wm = window.markmap || {};
          return wm.Markmap ? wm.Markmap : null;
        });
    }
    return mmViewPromise;
  }

  function buildMindmapOverlay() {
    if (!mmOverlayBuilt) {
      mmOverlayBuilt = true;
      var overlay = document.createElement('div');
      overlay.className = 'mindmap-overlay';
      overlay.id = 'mindmapOverlay';
      overlay.innerHTML =
        '<div class="mindmap-modal">' +
          '<div class="mindmap-modal-header">' +
            '<span class="mm-title">🗺️ Concept Map</span>' +
            '<span class="mm-hint">Scroll to zoom &middot; Drag to pan &middot; Click a node to collapse / expand</span>' +
            '<div class="mindmap-actions">' +
              '<button type="button" class="mm-fit">Fit</button>' +
              '<button type="button" class="mm-expand">Expand all</button>' +
              '<button type="button" class="mm-collapse">Collapse all</button>' +
            '</div>' +
            '<button type="button" class="mindmap-close" aria-label="Close mind map" title="Close (Esc)">&times;</button>' +
          '</div>' +
          '<svg id="mindmap-svg"></svg>' +
        '</div>';
      document.body.appendChild(overlay);

      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeMindmapOverlay();
      });
      qs('.mindmap-close', overlay).addEventListener('click', closeMindmapOverlay);
      qs('.mm-fit', overlay).addEventListener('click', function () {
        if (window.mmInstance) window.mmInstance.fit();
      });
      qs('.mm-expand', overlay).addEventListener('click', function () {
        if (window.mmInstance) window.mmInstance.setData(window.mmRoot, { initialExpandLevel: -1 });
      });
      qs('.mm-collapse', overlay).addEventListener('click', function () {
        if (window.mmInstance) window.mmInstance.setData(window.mmRoot, { initialExpandLevel: 0 });
      });
    }
  }

  function closeMindmapOverlay() {
    var overlay = qs('#mindmapOverlay');
    if (overlay) {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  function openMindmapOverlay() {
    buildMindmapOverlay();
    var overlay = qs('#mindmapOverlay');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function initMindmap() {
    try {
      var toggle = qs('.mindmap-toggle');
      var dataEl = qs('#chapter-mindmap-data');
      if (!toggle || !dataEl) return;

      // Live re-theme of the SVG when dark mode flips (Ch 1-5 pages).
      var svgObserver = new MutationObserver(function () {
        if (window.mmInstance) {
          window.mmInstance.fit();
        }
      });
      svgObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

      toggle.addEventListener('click', function () {
        openMindmapOverlay();
        var overlay = qs('#mindmapOverlay');
        var svg = qs('#mindmap-svg', overlay);
        svg.style.background = 'var(--surface)';
        svg.classList.add('no-print');

        var markdown;
        try {
          markdown = JSON.parse(dataEl.textContent.trim());
        } catch (err) {
          markdown = dataEl.textContent;
        }

        loadMarkmapView()
          .then(function (Markmap) {
            if (Markmap === null) { log('markmap-view not found'); return; }
            return loadMarkmapLib().then(function (Transformer) {
              return { Markmap: Markmap, Transformer: Transformer };
            });
          })
          .then(function (mm) {
            if (!mm.Transformer) { log('markmap transformer not found'); return; }
            // Clear any prior render so reopening doesn't stack SVGs.
            if (window.mmInstance && typeof window.mmInstance.destroy === 'function') {
              window.mmInstance.destroy();
            }
            var transformer = new mm.Transformer();
            var data = transformer.transform(markdown);
            window.mmRoot = data.root;
            window.mmInstance = mm.Markmap.create(svg, {
              colorFreezeLevel: 2,
              initialExpandLevel: 2,
              spacingVertical: 6,
              spacingHorizontal: 80
            }, data.root);
            window.mmInstance.fit();
          })
          .catch(function (err) { log('Mind map error: ' + err.message); });
      });
    } catch (e) { log('Mindmap init error: ' + e.message); }
  }

  /* ───────── 12. KEYBOARD SHORTCUTS ───────── */

  function initKeyboardShortcuts() {
    try {
      document.addEventListener('keydown', function (e) {
        // Don't fire shortcuts when typing in inputs/textarea
        var tag = e.target.tagName;
        if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

        if (e.key === 'd' && !e.ctrlKey && !e.metaKey && !e.altKey) {
          e.preventDefault();
          // Toggle dark mode
          var toggles = qsa('.dark-toggle');
          if (toggles.length) toggles[0].click();
          return;
        }

        if (e.key === 'r' && !e.ctrlKey && !e.metaKey && !e.altKey) {
          e.preventDefault();
          var revToggles = qsa('.revision-toggle');
          if (revToggles.length) revToggles[0].click();
          return;
        }

        if ((e.key === 's' || e.key === '/') && !e.ctrlKey && !e.metaKey && !e.altKey) {
          e.preventDefault();
          var searchToggles = qsa('.search-toggle');
          if (searchToggles.length) searchToggles[0].click();
          return;
        }

        if (e.key === 'p' && !e.ctrlKey && !e.metaKey && !e.altKey) {
          e.preventDefault();
          var printToggles = qsa('.print-toggle');
          if (printToggles.length) printToggles[0].click();
          else window.print();
          return;
        }

        if (e.key === 'Escape') {
          // Close the active overlay by finding its close button
          var mindmapOverlay = qs('#mindmapOverlay.active');
          var searchOverlay = qs('.search-overlay.active');
          var termsOverlay = qs('.terms-overlay.active');
          if (mindmapOverlay) {
            closeMindmapOverlay();
          } else if (searchOverlay) {
            var closeBtn = qs('.search-close', searchOverlay);
            if (closeBtn) closeBtn.click();
          } else if (termsOverlay) {
            var closeBtn = qs('.close-btn', termsOverlay);
            if (closeBtn) closeBtn.click();
          }
          return;
        }
      });
    } catch (e) { log('Keyboard shortcuts init error: ' + e.message); }
  }

  /* ───────── 12. CHAPTER TRACKING + STUDY LOG ───────── */

  // --- Study Log Helpers ---

  function getStudyLog() {
    return loadProgress('study-os-study-log', []);
  }

  function saveStudyLog(log) {
    saveProgress('study-os-study-log', log);
  }

  function getTodayLog() {
    var log = getStudyLog();
    var today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
    for (var i = 0; i < log.length; i++) {
      if (log[i].date === today) return log[i];
    }
    var newEntry = { date: today, totalMinutes: 0, chaptersVisited: [],  };
    log.push(newEntry);
    saveStudyLog(log);
    return newEntry;
  }

  function updateTodayLog(chapterId) {
    var log = getStudyLog();
    var today = new Date().toISOString().slice(0, 10);
    var entry = null;
    for (var i = 0; i < log.length; i++) {
      if (log[i].date === today) { entry = log[i]; break; }
    }
    if (!entry) {
      entry = { date: today, totalMinutes: 0, chaptersVisited: [],  };
      log.push(entry);
    }
    if (entry.chaptersVisited.indexOf(chapterId) === -1) {
      entry.chaptersVisited.push(chapterId);
    }
    entry.totalMinutes += 10; // estimate per visit
    saveStudyLog(log);
  }

  function calculateWeeklyActivity() {
    var log = getStudyLog();
    var days = [];
    var now = new Date();
    for (var i = 6; i >= 0; i--) {
      var d = new Date(now);
      d.setDate(d.getDate() - i);
      var dateStr = d.toISOString().slice(0, 10);
      var dayName = d.toLocaleDateString('en-US', { weekday: 'short' });
      var entry = null;
      for (var j = 0; j < log.length; j++) {
        if (log[j].date === dateStr) { entry = log[j]; break; }
      }
      days.push({ day: dayName, date: dateStr, minutes: entry ? entry.totalMinutes : 0, chapters: entry ? entry.chaptersVisited.length : 0 });
    }
    return days;
  }

  function initChapterTracking() {
    try {
      var chapterId = getChapterId();
      if (!chapterId) {
        log('No chapter ID detected, skipping chapter tracking');
        return;
      }

      var progress = loadProgress('study-os-progress', {});
      if (!progress[chapterId]) {
        progress[chapterId] = {};
      }
      progress[chapterId].visited = true;
      progress[chapterId].lastVisited = new Date().toISOString();
      progress[chapterId].visitCount = (progress[chapterId].visitCount || 0) + 1;
      progress[chapterId].totalTimeSpent = (progress[chapterId].totalTimeSpent || 0) + 10;
      saveProgress('study-os-progress', progress);

      // Also update today's study log
      updateTodayLog(chapterId);
    } catch (e) { log('Chapter tracking init error: ' + e.message); }
  }

  /* ───────── INIT ───────── */

  document.addEventListener('DOMContentLoaded', function () {
    initChapterTracking();
    initDarkMode();
    initRevisionMode();
    initSearch();
    initKeyTerms();
    initPWA();
    initPrint();
    initMindmap();
    initKeyboardShortcuts();

    log('Study OS initialized');
  });
})();
