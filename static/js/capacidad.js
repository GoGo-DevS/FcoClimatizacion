/* Calculadora de capacidad de la portada ("¿Qué capacidad necesito?").

   02-11-2026: el boton "Calcular" no hacia NADA desde el rediseno del 16-09.
   El HTML de la calculadora se conservo, pero el <script> que la hacia
   funcionar vivia dentro de home.html y se perdio al reescribir la portada.
   El hero manda ahi con "¿Qué capacidad necesito?" y las paginas de servicio
   la recomiendan, asi que quien llegaba encontraba un boton muerto y un
   "Cotizar con estos datos" deshabilitado para siempre.

   La formula es la que publicaba el sitio original (deploy inicial): 600 BTU
   por m2, +15 % con sol directo, +20 % con muchas personas o equipos, y se
   redondea al tamano comercial siguiente. Es una referencia: la capacidad
   final se confirma en la visita.

   Vive en un archivo propio y no dentro de la plantilla para que no se vuelva
   a perder al editar la portada, y para poder probarla
   (capacidad.test.mjs, que corre dentro de la suite de Django). */
(function () {
  'use strict';

  var TAMANOS = [9000, 12000, 18000, 24000, 30000, 36000, 48000];

  function estimarBTU(m2, uso) {
    var btu = m2 * 600;
    if (uso === 'caluroso') btu *= 1.15;
    if (uso === 'muchas_personas') btu *= 1.2;
    for (var i = 0; i < TAMANOS.length; i++) {
      if (btu <= TAMANOS[i]) return TAMANOS[i];
    }
    return TAMANOS[TAMANOS.length - 1];
  }

  var m2Input = document.getElementById('m2');
  var usoSelect = document.getElementById('uso');
  var boton = document.getElementById('btnCalc');
  var resultado = document.getElementById('resultado');
  var cotizar = document.getElementById('btnCotizarConBtu');
  if (!m2Input || !usoSelect || !boton || !resultado || !cotizar) return;

  // El numero de WhatsApp sale del enlace que ya dibuja la plantilla: asi no
  // hay un segundo lugar donde pueda quedar un telefono distinto.
  var base = cotizar.getAttribute('href').split('?')[0];

  boton.addEventListener('click', function () {
    var m2 = parseFloat(m2Input.value);
    if (!m2 || m2 <= 0) {
      resultado.textContent = 'Ingresa los m² del ambiente';
      cotizar.classList.add('disabled');
      cotizar.setAttribute('aria-disabled', 'true');
      return;
    }
    var uso = usoSelect.value;
    var btu = estimarBTU(m2, uso);
    resultado.textContent = btu.toLocaleString('es-CL') + ' BTU (estimado)';

    var texto = 'Hola, quiero cotizar aire acondicionado. Estimación: ' + m2 +
      ' m², uso ' + uso + ', recomendado ' + btu + ' BTU.';
    cotizar.setAttribute('href', base + '?text=' + encodeURIComponent(texto));
    cotizar.classList.remove('disabled');
    cotizar.removeAttribute('aria-disabled');

    // Solo si GA4 esta cargado: el sitio funciona igual sin medicion.
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'calculadora_capacidad', { btu: btu, uso: uso });
    }
  });
})();
