/* GoGoDevS Tree: cada boton que se aprieta en /links/ se manda a GA4 como
   evento "tree_click" con el parametro "destino" (whatsapp, telefono,
   interno:/servicios/... ). Es el mismo evento que en los otros sitios de
   GoGoDevS, para leerlos todos con el mismo informe.

   gtag se busca AL HACER CLIC, no al cargar: si GA no esta (bloqueador,
   local) no hace nada y la pagina funciona igual. */
(function () {
  'use strict';
  var reglas = [
    [/wa\.me|whatsapp\.com/i, 'whatsapp'],
    [/instagram\.com/i, 'instagram'],
    [/google\.[a-z.]+\/maps|maps\.app\.goo|goo\.gl\/maps|maps\.google/i, 'mapa'],
    [/^mailto:/i, 'correo'],
    [/^tel:/i, 'telefono']
  ];
  function destino(a) {
    var href = a.getAttribute('href') || '';
    for (var i = 0; i < reglas.length; i++) {
      if (reglas[i][0].test(href)) return reglas[i][1];
    }
    try {
      var u = new URL(href, window.location.href);
      if (u.host === window.location.host) return 'interno:' + u.pathname;
    } catch (e) {}
    return 'externo';
  }
  document.addEventListener('click', function (ev) {
    if (typeof window.gtag !== 'function' || !ev.target.closest) return;
    var a = ev.target.closest('a[href]');
    if (!a) return;
    window.gtag('event', 'tree_click', {
      destino: destino(a),
      texto_boton: (a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60),
      transport_type: 'beacon'
    });
  }, true);
})();
