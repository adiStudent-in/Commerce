/**
 * toc-scrollspy.js — one authoritative sidebar scrollspy for every Study OS chapter page.
 * Fixes: sub-section links never highlighting (legacy code watched section[id] only),
 * wrong highlight from offsetTop math, headings hiding under the fixed nav,
 * sidebars listing sub-topics before their parent, and the highlight scrolling
 * out of view. Loads after the legacy per-page handlers, so its highlight wins.
 */
(function () {
  'use strict';

  try {
    var TOC_SELECTORS = ['#toc', '.toc', '#sidebarToc', '.sidebar-toc', '#sidebar', '.sidebar', '#tocDrawer', '.toc-drawer', 'aside', 'nav'];

    function all(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
    function decode(id) { try { return decodeURIComponent(id); } catch (e) { return id; } }

    /* 1. Sidebar containers that actually hold anchor links. */
    var containers = [];
    TOC_SELECTORS.forEach(function (sel) {
      all(sel).forEach(function (el) {
        if (containers.indexOf(el) === -1 && el.querySelector('a[href^="#"]')) containers.push(el);
      });
    });
    if (!containers.length) return;

    /* 2. Every linked heading, sorted in document order (sidebar order is not trusted). */
    var seen = {};
    var targets = [];
    containers.forEach(function (ct) {
      all('a[href^="#"]', ct).forEach(function (a) {
        var href = a.getAttribute('href');
        if (!href || href.length < 2) return;
        var id = decode(href.slice(1));
        if (!id || seen[id]) return;
        var el = document.getElementById(id);
        if (!el) return;
        seen[id] = true;
        targets.push({ id: id, el: el });
      });
    });
    if (!targets.length) return;
    targets.sort(function (a, b) {
      if (a.el === b.el) return 0;
      return (a.el.compareDocumentPosition(b.el) & 4) ? -1 : 1;
    });
    var lastId = targets[targets.length - 1].id;

    /* All sidebar links grouped by target, so desktop sidebar + mobile drawer stay in sync. */
    var linksById = {};
    containers.forEach(function (ct) {
      all('a[href^="#"]', ct).forEach(function (a) {
        var id = decode(a.getAttribute('href').slice(1));
        if (!id || !seen[id]) return;
        var group = (linksById[id] = linksById[id] || []);
        if (group.indexOf(a) === -1) group.push(a);
      });
    });

    /* 3. Keep anchored headings clear of the fixed 60px nav. */
    document.documentElement.style.scrollPaddingTop = '84px';
    targets.forEach(function (t) { t.el.style.scrollMarginTop = '90px'; });

    /* 4. Highlight the current topic and keep it visible inside the sidebar. */
    var currentId = null;
    function setActive(id) {
      if (id === currentId) return;
      currentId = id;
      Object.keys(linksById).forEach(function (key) {
        var on = (id !== null && key === id);
        linksById[key].forEach(function (a) {
          if (on) a.classList.add('active');
          else a.classList.remove('active');
        });
      });
      if (id === null) return;
      containers.forEach(function (ct) {
        if (ct.scrollHeight <= ct.clientHeight + 4) return;
        var active = ct.querySelector('a.active');
        if (!active) return;
        var cRect = ct.getBoundingClientRect();
        var aRect = active.getBoundingClientRect();
        if (aRect.top < cRect.top + 4) ct.scrollTop -= (cRect.top + 4 - aRect.top);
        else if (aRect.bottom > cRect.bottom - 4) ct.scrollTop += (aRect.bottom - (cRect.bottom - 4));
      });
    }

    /* 5. Which topic owns the current scroll position. */
    var OFFSET = 110;
    function pickByPosition() {
      var y = window.scrollY || window.pageYOffset || 0;
      if (y < 40) return null;
      var cur = null;
      for (var i = 0; i < targets.length; i++) {
        var top = targets[i].el.getBoundingClientRect().top + y;
        if (top - OFFSET <= y) cur = targets[i].id;
        else break;
      }
      return cur;
    }

    function atBottom() {
      var h = document.documentElement;
      return (window.innerHeight + (window.scrollY || 0)) >= (h.scrollHeight - 4);
    }

    /* Tapping a link highlights it at once; scroll tracking takes over from there. */
    Object.keys(linksById).forEach(function (key) {
      linksById[key].forEach(function (a) {
        a.addEventListener('click', function () { setActive(key); });
      });
    });

    if ('IntersectionObserver' in window) {
      var visible = {};
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
        var best = null;
        for (var i = 0; i < targets.length; i++) {
          if (visible[targets[i].id]) best = targets[i].id;
        }
        if (best) setActive(best);
        else if (atBottom()) setActive(lastId);
        else {
          var near = pickByPosition();
          if (near) setActive(near);
        }
      }, { rootMargin: '-100px 0px -65% 0px', threshold: 0 });
      targets.forEach(function (t) { io.observe(t.el); });
      var ticking = false;
      window.addEventListener('scroll', function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
          ticking = false;
          if (atBottom()) setActive(lastId);
        });
      }, { passive: true });
    } else {
      var tickingFallback = false;
      window.addEventListener('scroll', function () {
        if (tickingFallback) return;
        tickingFallback = true;
        requestAnimationFrame(function () {
          tickingFallback = false;
          setActive(atBottom() ? lastId : pickByPosition());
        });
      }, { passive: true });
    }

    /* 6. Deep links: honour #hash on load and when it changes. */
    function applyHash() {
      var raw = window.location.hash;
      if (!raw || raw.length < 2) return;
      var id = decode(raw.slice(1));
      if (!seen[id]) return;
      setActive(id);
      var el = document.getElementById(id);
      if (el) el.scrollIntoView({ block: 'start' });
    }
    window.addEventListener('hashchange', applyHash);
    function initPosition() {
      if (window.location.hash) applyHash();
      else {
        var near = pickByPosition();
        if (near) setActive(near);
      }
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initPosition);
    } else {
      initPosition();
    }
  } catch (e) { /* Never break the page: the sidebar simply stays unhighlighted. */ }
})();
