/* Чтение без сети.

   Книга была файлом и открывалась в самолёте; став сайтом, она это
   потеряла. Этот сценарий возвращает: браузер держит копию книги у себя и
   отдаёт её, когда сети нет.

   Сделано так, чтобы не пришлось помнить о версиях при каждом издании:

   — саму книгу берём из сети, если сеть есть, и из копии, если нет.
     Значит свежее издание читатель видит сразу, а не со второго захода;
   — шрифты и значки отдаём из копии сразу, а обновление тянем следом,
     в фоне. Пересобрали шрифты — новые приедут при следующем открытии;
   — имя хранилища меняется, только если понадобится выбросить старое
     целиком. При обычной правке книги менять ничего не нужно.
*/

const HRANILISHCHE = 'terruary';

// то, без чего книга не откроется в самолёте
const OSNOVA = [
  './',
  'index.html',
  'manifest.webmanifest',
  'fonts/literata.woff2',
  'fonts/literata-italic.woff2',
  'fonts/alegreya.woff2',
  'fonts/alegreya-italic.woff2',
  'fonts/plexmono-400.woff2',
  'fonts/plexmono-600.woff2',
  'favicon.svg',
  'favicon-32.png',
  'apple-touch-icon.png',
  'icon-192.png',
  'icon-512.png',
];

self.addEventListener('install', (sob) => {
  sob.waitUntil(
    caches.open(HRANILISHCHE)
      .then((h) => h.addAll(OSNOVA))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (sob) => {
  sob.waitUntil(
    caches.keys()
      .then((imena) => Promise.all(
        imena.filter((i) => i !== HRANILISHCHE).map((i) => caches.delete(i))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (sob) => {
  const zapros = sob.request;
  if (zapros.method !== 'GET') return;
  if (new URL(zapros.url).origin !== self.location.origin) return;

  // сама книга: сеть впереди, копия про запас
  if (zapros.mode === 'navigate' || zapros.destination === 'document') {
    sob.respondWith(
      fetch(zapros)
        .then((otvet) => {
          const kopija = otvet.clone();
          caches.open(HRANILISHCHE).then((h) => h.put('index.html', kopija));
          return otvet;
        })
        .catch(() => caches.match('index.html').then((k) => k || caches.match('./')))
    );
    return;
  }

  // всё остальное: копия сразу, обновление следом
  sob.respondWith(
    caches.match(zapros).then((kopija) => {
      const svezhee = fetch(zapros)
        .then((otvet) => {
          if (otvet && otvet.ok) {
            const dlja_hranilishcha = otvet.clone();
            caches.open(HRANILISHCHE).then((h) => h.put(zapros, dlja_hranilishcha));
          }
          return otvet;
        })
        .catch(() => kopija);
      return kopija || svezhee;
    })
  );
});
