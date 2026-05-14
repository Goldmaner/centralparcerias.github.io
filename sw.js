// Service Worker — Network-first com fallback offline
const CACHE_NAME = 'central-parcerias-v6';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './Pages/visita_tecnica.html',
  './Pages/monitoramento_avaliacao.html'
];

// Instala e cacheia os assets essenciais para uso offline
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Limpa caches antigos ao ativar nova versão
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Estratégia: network-first, fallback para cache se offline
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  // Navegações de página (cliques em links) nunca devem ser interceptadas pelo SW
  // para evitar que conteúdo cacheado antigo seja servido no lugar da página correta.
  if (event.request.mode === 'navigate') return;
  event.respondWith(
    fetch(event.request).then(response => {
      // Atualiza o cache com a resposta mais recente
      if (response.ok) {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
      }
      return response;
    }).catch(() => {
      // Sem rede — entrega do cache (apenas assets, nunca HTML de navegação)
      return caches.match(event.request) || Promise.reject('offline');
    })
  );
});

// Permite que uma página force o SW a ativar imediatamente
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
