// Service Worker Básico de Netmarlyn (PWA)
const CACHE_NAME = 'netmarlyn-pwa-v1';

self.addEventListener('install', (event) => {
    console.log('[Service Worker] Instalando el Service Worker...');
    // Actualmente no cacheamos todo automáticamente porque estamos en diseño
    // y el usuario pidió explícitamente ver sus cambios en vivo.
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activado.');
    return self.clients.claim();
});

// Interceptor de llamadas básico requerido para PWA
self.addEventListener('fetch', (event) => {
    event.respondWith(
        fetch(event.request).catch(() => {
            console.log("Intento de conexión offline");
        })
    );
});
