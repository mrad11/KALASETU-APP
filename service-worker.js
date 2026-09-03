const CACHE_NAME = 'kalasetu-ai-v2';
const APP_ASSETS = [
  './',
  './index.html',
  './kalasetu-prototype.html',
  './manifest.webmanifest',
  './kalasetu-icon.svg',
  './icon-192.png',
  './icon-maskable-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png',
  './kalasetu-icon.ico',
  './audio/english.mp3',
  './audio/hindi.mp3',
  './audio/telugu.mp3',
  './audio/tamil.mp3',
  './audio/bhojpuri.mp3',
  './audio/marathi.mp3',
  './audio/bengali.mp3',
  './audio/kannada.mp3'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(APP_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
        return response;
      }).catch(() => caches.match('./index.html') || caches.match('./kalasetu-prototype.html'));
    })
  );
});
