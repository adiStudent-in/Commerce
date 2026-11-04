/* BST chapter pages — interactive concept map.
   Lazy-loads markmap only when a Mind Map button is pressed, then renders
   a full-screen, zoomable map built from bst-mindmap-data.js. */
(function () {
  'use strict';

  var CDN = {
    d3: 'https://cdn.jsdelivr.net/npm/d3@7',
    lib: 'https://cdn.jsdelivr.net/npm/markmap-lib@0.18.12',
    view: 'https://cdn.jsdelivr.net/npm/markmap-view@0.18.12'
  };

  var unit = document.body ? document.body.getAttribute('data-unit') : '';
  var config = window.BST_MINDMAPS && window.BST_MINDMAPS[unit];
  var toggles = Array.prototype.slice.call(document.querySelectorAll('.mindmap-toggle'));
  if (!config || !toggles.length) return;

  var chapter = unit.replace(/^bst-/, '') || '1';
  var overlay = null;
  var dialog = null;
  var svg = null;
  var loading = null;
  var errorBox = null;
  var meta = null;
  var lastFocus = null;
  var previousOverflow = '';
  var markmap = null;
  var root = null;
  var mapTheme = null;
  var creating = false;
  var viewPromise = null;
  var libPromise = null;
  var fitTimer = null;

  var reducedMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  function log(message) {
    if (window.console && console.warn) console.warn('[BST mind map] ' + message);
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var script = document.createElement('script');
      script.src = src;
      script.onload = resolve;
      script.onerror = function () { reject(new Error('Could not load ' + src)); };
      document.head.appendChild(script);
    });
  }

  function loadLib() {
    if (!libPromise) {
      libPromise = loadScript(CDN.d3)
        .then(function () { return loadScript(CDN.lib); })
        .then(function () {
          var wm = window.markmap || {};
          return wm.Transformer || null;
        });
    }
    return libPromise;
  }

  function loadView() {
    if (!viewPromise) {
      viewPromise = loadLib()
        .then(function () { return loadScript(CDN.view); })
        .then(function () {
          var wm = window.markmap || {};
          return { Markmap: wm.Markmap || null, deriveOptions: wm.deriveOptions || null };
        });
    }
    return viewPromise;
  }

  function themeColours() {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    return dark
      ? ['#74c6a8', '#e0a55f', '#82b5dc', '#b9a1e0', '#e59a83', '#8ecf9b']
      : ['#1a5e4a', '#b87324', '#2f6f8f', '#6d54a3', '#a24d3b', '#527b3f'];
  }

  function countMap(markdown) {
    var branches = 0;
    var points = 0;
    markdown.split('\n').forEach(function (line) {
      if (/^##\s/.test(line)) branches += 1;
      else if (/^\s*[-*]\s+/.test(line)) points += 1;
    });
    return { branches: branches, points: points };
  }

  function build() {
    if (overlay) return;

    overlay = document.createElement('div');
    overlay.className = 'mindmap-overlay';
    overlay.id = 'mindmapOverlay';
    overlay.innerHTML =
      '<div class="mindmap-modal" role="dialog" aria-modal="true" aria-labelledby="mindmapTitle" tabindex="-1">' +
        '<div class="mindmap-head">' +
          '<div class="mm-copy">' +
            '<span class="mm-kicker">Chapter ' + chapter + ' · Concept map</span>' +
            '<h2 class="mm-title" id="mindmapTitle"></h2>' +
            '<p class="mm-hint">Scroll or pinch to zoom · Drag to pan · Click a circle to fold a branch</p>' +
          '</div>' +
          '<div class="mm-tools" role="toolbar" aria-label="Mind map controls">' +
            '<button type="button" data-mm="zoom-out" title="Zoom out" aria-label="Zoom out">−</button>' +
            '<button type="button" data-mm="zoom-in" title="Zoom in" aria-label="Zoom in">+</button>' +
            '<button type="button" data-mm="fit">Fit</button>' +
            '<button type="button" data-mm="expand">Expand all</button>' +
            '<button type="button" data-mm="collapse">Collapse all</button>' +
            '<button type="button" data-mm="download" title="Download this map as an SVG">SVG</button>' +
          '</div>' +
          '<button type="button" class="mindmap-close" aria-label="Close mind map" title="Close (Esc)">&times;</button>' +
        '</div>' +
        '<div class="mindmap-canvas">' +
          '<div class="mm-loading" role="status"><span class="mm-spinner" aria-hidden="true"></span><span>Building your concept map…</span></div>' +
          '<div class="mm-error" role="alert" hidden><strong>The map could not load.</strong><span>Check your connection and try again.</span><button type="button" class="mm-retry">Try again</button></div>' +
          '<svg id="mindmap-svg" role="img" aria-label="Concept map for Chapter ' + chapter + '"></svg>' +
        '</div>' +
        '<div class="mindmap-foot">' +
          '<span class="mm-tip">Tip: use <strong>Expand all</strong> to revise every point, then fold branches to test yourself.</span>' +
          '<span class="mm-meta"></span>' +
        '</div>' +
      '</div>';

    document.body.appendChild(overlay);
    dialog = overlay.querySelector('.mindmap-modal');
    svg = overlay.querySelector('#mindmap-svg');
    loading = overlay.querySelector('.mm-loading');
    errorBox = overlay.querySelector('.mm-error');
    meta = overlay.querySelector('.mm-meta');

    var title = overlay.querySelector('#mindmapTitle');
    title.textContent = config.title;

    var counts = countMap(config.markdown);
    meta.textContent = counts.branches + ' branches · ' + counts.points + ' mapped points';

    overlay.querySelector('.mindmap-close').addEventListener('click', close);
    overlay.addEventListener('click', function (event) {
      if (event.target === overlay) close();
    });

    overlay.querySelector('[data-mm="zoom-out"]').addEventListener('click', function () {
      if (markmap && typeof markmap.rescale === 'function') markmap.rescale(0.8);
    });
    overlay.querySelector('[data-mm="zoom-in"]').addEventListener('click', function () {
      if (markmap && typeof markmap.rescale === 'function') markmap.rescale(1.2);
    });
    overlay.querySelector('[data-mm="fit"]').addEventListener('click', function () {
      if (markmap) markmap.fit();
    });
    overlay.querySelector('[data-mm="expand"]').addEventListener('click', function () {
      setFold(-1);
    });
    overlay.querySelector('[data-mm="collapse"]').addEventListener('click', function () {
      setFold(0);
    });
    overlay.querySelector('[data-mm="download"]').addEventListener('click', downloadSvg);
    overlay.querySelector('.mm-retry').addEventListener('click', retry);

    /* Markmap folds a branch on circle click but does not re-fit the view,
       so an expanded branch can run off the canvas. Capture the click before
       markmap handles it, then fit once the fold animation has finished. */
    svg.addEventListener('click', function (event) {
      if (!event.target || event.target.tagName !== 'circle') return;
      window.clearTimeout(fitTimer);
      fitTimer = window.setTimeout(function () {
        if (markmap) markmap.fit();
      }, 420);
    }, true);

    document.addEventListener('keydown', onKeydown);
  }

  function setFold(level) {
    /* markmap clones the tree passed to setData(), so fold flags must be set
       on the rendered state tree, not on the transform() result. */
    var data = markmap && markmap.state && markmap.state.data;
    if (!data) return;

    function walk(node, depth) {
      node.payload = Object.assign({}, node.payload, {
        fold: depth === 0 ? 0 : (level < 0 ? 0 : 1)
      });
      (node.children || []).forEach(function (child) { walk(child, depth + 1); });
    }

    try {
      walk(data, 0);
      Promise.resolve(markmap.renderData())
        .then(function () { return markmap.fit(); })
        .catch(function (error) { log(error.message); });
    } catch (error) {
      log(error.message);
    }
  }

  function downloadSvg() {
    if (!svg || !markmap) return;
    try {
      var rect = svg.getBoundingClientRect();
      var clone = svg.cloneNode(true);
      clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      clone.setAttribute('width', Math.max(1, Math.round(rect.width)));
      clone.setAttribute('height', Math.max(1, Math.round(rect.height)));

      var dark = document.documentElement.getAttribute('data-theme') === 'dark';
      var surface = dark ? '#1a201c' : '#fffdf9';
      var ink = dark ? '#e9e8e1' : '#1e241f';

      var background = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      background.setAttribute('width', '100%');
      background.setAttribute('height', '100%');
      background.setAttribute('fill', surface);
      clone.insertBefore(background, clone.firstChild);

      var style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
      style.textContent = '.markmap{--markmap-text-color:' + ink + ';--markmap-circle-open-bg:' + surface + ';--markmap-font:500 14px/19px Outfit, Segoe UI, sans-serif}';
      clone.insertBefore(style, clone.firstChild);

      var source = '<?xml version="1.0" encoding="UTF-8"?>\n' + new XMLSerializer().serializeToString(clone);
      var blob = new Blob([source], { type: 'image/svg+xml;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var link = document.createElement('a');
      link.href = url;
      link.download = 'bst-chapter-' + chapter + '-mindmap.svg';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    } catch (error) {
      log('SVG export failed: ' + error.message);
    }
  }

  function render() {
    if (markmap) {
      window.requestAnimationFrame(function () { markmap.fit(); });
      return;
    }
    if (creating) return;

    creating = true;
    loading.hidden = false;
    errorBox.hidden = true;

    loadView()
      .then(function (view) {
        if (!overlay.classList.contains('active')) return null;
        if (!view.Markmap) throw new Error('markmap-view is unavailable');

        return loadLib().then(function (Transformer) {
          if (!Transformer) throw new Error('markmap-lib is unavailable');
          if (!overlay.classList.contains('active')) return null;

          var data = new Transformer().transform(config.markdown);
          root = data.root;

          var rawOptions = {
            duration: reducedMotion ? 0 : 300,
            fitRatio: 0.92,
            initialExpandLevel: 2,
            maxWidth: 320,
            nodeMinHeight: 16,
            paddingX: 8,
            spacingHorizontal: 90,
            spacingVertical: 8,
            color: themeColours(),
            colorFreezeLevel: 2
          };
          var options = typeof view.deriveOptions === 'function'
            ? view.deriveOptions(rawOptions)
            : rawOptions;

          if (markmap && typeof markmap.destroy === 'function') markmap.destroy();
          svg.innerHTML = '';
          markmap = view.Markmap.create(svg, options);
          mapTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
          return markmap.setData(root).then(function () { return markmap.fit(); });
        });
      })
      .then(function () {
        creating = false;
        loading.hidden = true;
      })
      .catch(function (error) {
        creating = false;
        loading.hidden = true;
        errorBox.hidden = false;
        log(error.message);
      });
  }

  function retry() {
    libPromise = null;
    viewPromise = null;
    if (markmap && typeof markmap.destroy === 'function') markmap.destroy();
    markmap = null;
    root = null;
    render();
  }

  function open() {
    build();

    /* Node colours are baked in at render time, so rebuild the map if the
       user changed the page theme while it was closed. */
    var theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    if (markmap && mapTheme !== theme) {
      if (typeof markmap.destroy === 'function') markmap.destroy();
      markmap = null;
      root = null;
    }

    lastFocus = document.activeElement;
    previousOverflow = document.body.style.overflow;
    overlay.classList.add('active');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    toggles.forEach(function (toggle) { toggle.setAttribute('aria-expanded', 'true'); });
    dialog.focus();
    render();
  }

  function close() {
    if (!overlay || !overlay.classList.contains('active')) return;
    overlay.classList.remove('active');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = previousOverflow;
    toggles.forEach(function (toggle) { toggle.setAttribute('aria-expanded', 'false'); });
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
  }

  function onKeydown(event) {
    if (!overlay || !overlay.classList.contains('active')) return;

    if (event.key === 'Escape') {
      event.preventDefault();
      close();
      return;
    }

    if (event.key !== 'Tab') return;

    var focusable = Array.prototype.slice.call(
      dialog.querySelectorAll('button:not([disabled]), [href], [tabindex]:not([tabindex="-1"])')
    ).filter(function (element) {
      return element.offsetParent !== null;
    });
    if (!focusable.length) return;

    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    if (event.shiftKey && (document.activeElement === first || document.activeElement === dialog)) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  toggles.forEach(function (toggle) {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.addEventListener('click', open);
  });
})();
