/* Unique You Media - Kopfbereich, Menue und Einblenden beim Scrollen.
   Laeuft ohne fremde Bibliotheken. Faellt die Datei aus, bleibt die Seite voll lesbar. */
(function () {
  'use strict';

  /* ---- Kopfbereich bekommt beim Scrollen eine Linie ---- */
  var head = document.getElementById('head');
  if (head) {
    var onScroll = function () {
      if (window.scrollY > 6) head.classList.add('stuck');
      else head.classList.remove('stuck');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    /* ---- Menue auf dem Handy ---- */
    var burger = head.querySelector('.burger');
    if (burger) {
      burger.addEventListener('click', function () {
        var open = head.classList.toggle('open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      // Beim Klick auf einen Menuepunkt wieder schliessen
      head.querySelectorAll('.mobile-nav a').forEach(function (a) {
        a.addEventListener('click', function () {
          head.classList.remove('open');
          burger.setAttribute('aria-expanded', 'false');
        });
      });
      // Esc schliesst ebenfalls
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && head.classList.contains('open')) {
          head.classList.remove('open');
          burger.setAttribute('aria-expanded', 'false');
          burger.focus();
        }
      });
    }
  }

  /* ---- Einblenden beim Scrollen ---- */
  var d = document.documentElement;
  if (d.className.indexOf('js') < 0) return;

  var els = [].slice.call(document.querySelectorAll('.rv'));
  if (!els.length) return;

  els.forEach(function (el) {
    var par = el.parentNode;
    if (par && par.className && String(par.className).indexOf('rv-group') >= 0) {
      var i = [].slice.call(par.children).indexOf(el);
      el.style.setProperty('--d', (i * 120) + 'ms');
    }
  });

  var show = function (el) { el.classList.add('in'); };

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.04 });

  els.forEach(function (el) { io.observe(el); });

  // Sicherheitsnetz: Greift nur, wenn nach 3 Sekunden ueberhaupt nichts
  // eingeblendet wurde. Dann ist etwas kaputt und wir zeigen alles.
  // Sonst bliebe die Animation beim Scrollen unten aus.
  setTimeout(function () {
    if (!document.querySelector('.rv.in')) els.forEach(show);
  }, 3000);
  window.addEventListener('beforeprint', function () { els.forEach(show); });
})();
