/* GCAR — sdílené chování. Bez závislostí, bez build kroku. */
(function () {
  'use strict';

  /* ---------- Mobilní menu ---------- */
  function initMenu() {
    var b = document.getElementById('burger');
    var m = document.getElementById('mobmenu');
    if (!b || !m) return;

    function set(open) {
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
      b.setAttribute('aria-label', open ? 'Zavřít menu' : 'Otevřít menu');
      m.hidden = !open;
    }

    b.addEventListener('click', function () { set(m.hidden); });
    m.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') set(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !m.hidden) { set(false); b.focus(); }
    });

    var mq = window.matchMedia('(min-width:981px)');
    var onChange = function (e) { if (e.matches) set(false); };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  /* ---------- Živý stav otevírací doby ----------
     Jediné místo, kde je otevírací doba v kódu. Změna je jen tady.
     Minuty od půlnoci. Neděle = 0.                                   */
  var HOURS = {
    1: [480, 1020],  // pondělí   8:00–17:00
    2: [480, 1020],
    3: [480, 1020],
    4: [480, 1020],
    5: [480, 1020],  // pátek
    6: [540, 600]    // sobota    9:00–10:00 (potvrzeno firmy.cz)
  };

  function isOpen(now) {
    var h = HOURS[now.getDay()];
    if (!h) return false;
    var m = now.getHours() * 60 + now.getMinutes();
    return m >= h[0] && m < h[1];
  }

  function nextText(now) {
    var d = now.getDay();
    var m = now.getHours() * 60 + now.getMinutes();
    if (HOURS[d] && m < HOURS[d][0]) {
      return 'Otevřeme v ' + fmt(HOURS[d][0]);
    }
    for (var i = 1; i <= 7; i++) {
      var day = (d + i) % 7;
      if (HOURS[day]) {
        var names = ['v neděli', 'v pondělí', 'v úterý', 've středu', 've čtvrtek', 'v pátek', 'v sobotu'];
        var label = (i === 1) ? 'zítra' : names[day];
        return 'Otevřeme ' + label + ' v ' + fmt(HOURS[day][0]);
      }
    }
    return 'Zavřeno';
  }

  function fmt(mins) {
    var h = Math.floor(mins / 60), m = mins % 60;
    return h + ':' + (m < 10 ? '0' + m : m);
  }

  function initHours() {
    var nodes = document.querySelectorAll('[data-branch]');
    if (!nodes.length) return;

    function render() {
      var now = new Date();
      var open = isOpen(now);
      var text = open ? 'Teď otevřeno' : nextText(now);
      Array.prototype.forEach.call(nodes, function (el) {
        var dot = el.querySelector('.dot');
        var st = el.querySelector('.status');
        if (dot) dot.classList.toggle('is-open', open);
        if (st) {
          st.classList.toggle('is-open', open);
          st.textContent = text;
        }
      });
    }

    render();
    setInterval(render, 60000);
  }

  /* ---------- Kontaktní formulář ----------
     Zatím jen klientská validace a odeslání přes mailto jako záloha.
     Až bude endpoint (Formspree / vlastní), přepíše se sem fetch().   */
  function initForm() {
    var f = document.getElementById('kontaktni-formular');
    if (!f) return;

    f.addEventListener('submit', function (e) {
      // honeypot proti botům
      var hp = f.querySelector('[name="_gotcha"]');
      if (hp && hp.value) { e.preventDefault(); return; }

      if (!f.getAttribute('action')) {
        e.preventDefault();
        var get = function (n) {
          var el = f.querySelector('[name="' + n + '"]');
          return el ? el.value : '';
        };
        var body = [
          'Jméno: ' + get('jmeno'),
          'Firma: ' + get('firma'),
          'Telefon: ' + get('telefon'),
          'E-mail: ' + get('email'),
          'Vozidlo / VIN: ' + get('vozidlo'),
          '',
          get('zprava')
        ].join('\n');
        window.location.href = 'mailto:gcar@gcar.cz'
          + '?subject=' + encodeURIComponent('Poptávka z webu')
          + '&body=' + encodeURIComponent(body);
      }
    });
  }

  /* ---------- Vyhledávání v e-shopu ----------
     E-shop používá cestovou adresu: /cs/hledani/5/-1/{dotaz}
     (5 = režim hledání podle textu, -1 = všechny kategorie).   */
  function initSearch() {
    var f = document.getElementById('hledani');
    if (!f) return;
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = f.querySelector('input[name="q"]');
      var q = (input && input.value || '').trim();
      if (!q) { if (input) input.focus(); return; }
      window.location.href = f.getAttribute('data-base') + encodeURIComponent(q);
    });
  }

  /* ---------- Přepínač denního a nočního režimu ----------
     Výchozí stav bere z nastavení systému. Jakmile ho člověk přepne,
     volba se uloží a systém už ji nepřebíjí.                        */
  function initTheme() {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    var root = document.documentElement;

    function apply(t) {
      root.setAttribute('data-theme', t);
      btn.setAttribute('aria-label', t === 'dark' ? 'Přepnout na denní režim' : 'Přepnout na noční režim');
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute('content', t === 'dark' ? '#0B101A' : '#1A243D');
    }

    apply(root.getAttribute('data-theme') || 'light');

    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      apply(next);
      try { localStorage.setItem('gcar-theme', next); } catch (e) {}
    });

    // dokud si člověk nevybral sám, sleduj nastavení systému
    var mq = window.matchMedia('(prefers-color-scheme:dark)');
    var follow = function (e) {
      var saved = null;
      try { saved = localStorage.getItem('gcar-theme'); } catch (err) {}
      if (saved !== 'dark' && saved !== 'light') apply(e.matches ? 'dark' : 'light');
    };
    if (mq.addEventListener) mq.addEventListener('change', follow);
    else if (mq.addListener) mq.addListener(follow);
  }

  function init() { initTheme(); initMenu(); initHours(); initForm(); initSearch(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
