/* Eventos de contacto. GA4 ya mide visitas; esto mide lo unico que importa:
   cuantas de esas visitas levantaron el telefono.

   Antes de esto el informe decia "71 sesiones" y no habia forma de saber si
   alguien llamo. Con esto el mismo informe dice cuantos clics a WhatsApp, al
   telefono, al correo y cuantos formularios se enviaron de verdad.

   UN solo escuchador en el documento, no uno por boton: asi tambien cuenta los
   enlaces que aparecen despues (acordeones, modales, contenido cargado por JS).

   Si gtag no existe (medicion apagada, bloqueador de anuncios) no hace nada y
   no rompe la pagina: el sitio tiene que funcionar igual sin medicion. */
(function () {
  'use strict';

  function medir(nombre, datos) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', nombre, datos || {});
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    var donde = window.location.pathname;

    if (/(?:wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)/i.test(href)) {
      medir('contacto_whatsapp', { ubicacion: donde });
    } else if (href.indexOf('tel:') === 0) {
      medir('contacto_telefono', { ubicacion: donde });
    } else if (href.indexOf('mailto:') === 0) {
      medir('contacto_email', { ubicacion: donde });
    } else if (/instagram\.com/i.test(href)) {
      medir('click_instagram', { ubicacion: donde });
    }
  }, true);   // fase de captura: cuenta aunque otro script detenga el evento

  /* El formulario se mide al ENVIARSE y solo si el navegador lo considera
     valido. Medir el clic en el boton contaria los intentos fallidos como
     contactos, y el informe diria que hay mas leads de los que hay. */
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM') return;
    if (typeof f.checkValidity === 'function' && !f.checkValidity()) return;
    medir('formulario_enviado', {
      ubicacion: window.location.pathname,
      formulario: f.getAttribute('name') || f.getAttribute('id') || 'sin-nombre'
    });
  }, true);
})();
