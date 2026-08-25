/* ===== Study OS Service Worker ===== */
/* Notes Hub — Class 11 Commerce PWA     */
/* Version 1.0                           */

var CACHE_NAME = 'study-os-v2';
var ASSETS_TO_CACHE = [
  './',
  './index.html',
  './assets/study-os.css',
  './assets/study-os.js',
  'https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Outfit:wght@300;400;500;600&display=swap',
  'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js'
];

/* ---- Cache-First strategy for static assets ---- */
async function cacheFirst(request) {
  try {
    var cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    var networkResponse = await fetch(request);
    if (networkResponse && networkResponse.ok) {
      var cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.error('[SW] cacheFirst error:', error.message);
    // If we have a cached response, return it even though we already checked
    var fallback = await caches.match(request);
    if (fallback) return fallback;
    // Otherwise return a basic offline fallback
    return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
  }
}

/* ---- Network-First strategy for HTML pages ---- */
async function networkFirst(request) {
  try {
    var networkResponse = await fetch(request);
    if (networkResponse && networkResponse.ok) {
      var cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.error('[SW] networkFirst error:', error.message);
    var cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
  }
}

/* ---- Install ---- */
self.addEventListener('install', function (event) {
  console.log('[SW] Installing service worker...');
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      console.log('[SW] Caching app shell and static assets');
      return cache.addAll(ASSETS_TO_CACHE).catch(function (err) {
        console.error('[SW] Failed to cache some assets:', err.message);
      });
    })
  );
  self.skipWaiting();
});

/* ---- Activate ---- */
self.addEventListener('activate', function (event) {
  console.log('[SW] Activating service worker...');
  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames.map(function (name) {
          if (name !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          }
        })
      );
    }).then(function () {
      console.log('[SW] Service worker activated, claiming clients');
      return self.clients.claim();
    })
  );
});

/* ---- Fetch ---- */
self.addEventListener('fetch', function (event) {
  var request = event.request;
  var url = new URL(request.url);

  // Determine strategy based on request type and URL patterns

  // Cache-First for static assets
  if (
    /\.(css|js|png|svg|jpg|jpeg|gif|webp|woff2?|ttf|eot|ico)$/i.test(url.pathname) ||
    url.hostname === 'fonts.googleapis.com' ||
    url.hostname === 'fonts.gstatic.com' ||
    url.hostname === 'cdn.jsdelivr.net'
  ) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Network-First for navigation requests and HTML pages
  if (request.mode === 'navigate' || /\.html$/i.test(url.pathname)) {
    event.respondWith(networkFirst(request));
    return;
  }

  // For everything else, try network first with cache fallback
  event.respondWith(networkFirst(request));
});
