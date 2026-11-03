// Prueba el COMPORTAMIENTO de la calculadora, no su presencia: arma los
// elementos de la portada, aprieta "Calcular" y mira lo que queda escrito.
// Uso: node capacidad.test.mjs capacidad.js   (sale con 1 si algo falla)
import fs from 'node:fs';
const src = fs.readFileSync(process.argv[2], 'utf8');

function elemento(props = {}) {
  const attrs = { ...(props.attrs || {}) };
  const clases = new Set(props.clases || []);
  const oyentes = {};
  return {
    value: props.value || '',
    textContent: '',
    classList: {
      add: (c) => clases.add(c),
      remove: (c) => clases.delete(c),
      contains: (c) => clases.has(c),
    },
    getAttribute: (a) => (a in attrs ? attrs[a] : null),
    setAttribute: (a, v) => { attrs[a] = String(v); },
    removeAttribute: (a) => { delete attrs[a]; },
    addEventListener: (t, fn) => { (oyentes[t] = oyentes[t] || []).push(fn); },
    disparar: (t) => (oyentes[t] || []).forEach((fn) => fn({})),
  };
}

const eventos = [];
const els = {
  m2: elemento(),
  uso: elemento({ value: 'normal' }),
  btnCalc: elemento(),
  resultado: elemento(),
  btnCotizarConBtu: elemento({
    clases: ['btn', 'disabled'],
    attrs: { href: 'https://wa.me/56956393341?text=Hola,%20quiero%20cotizar%20aire%20acondicionado.' },
  }),
};
globalThis.window = { gtag: (tipo, nombre, datos) => { if (tipo === 'event') eventos.push([nombre, datos]); } };
globalThis.document = { getElementById: (id) => els[id] || null };
eval(src);

let ok = 0;
let total = 0;
function revisar(nombre, condicion, detalle) {
  total += 1;
  ok += condicion ? 1 : 0;
  console.log(`  ${condicion ? 'OK  ' : 'FALLA'} ${nombre}${condicion ? '' : '  -> ' + detalle}`);
}

function calcular(m2, uso) {
  els.m2.value = String(m2);
  els.uso.value = uso;
  eventos.length = 0;
  els.btnCalc.disparar('click');
  return els.resultado.textContent;
}

// 18 m2 normal = 10.800 -> 12.000; 15 m2 = 9.000 justo; con sol, 15 m2 sube.
const casos = [
  [15, 'normal', '9.000 BTU (estimado)'],
  [18, 'normal', '12.000 BTU (estimado)'],
  [15, 'caluroso', '12.000 BTU (estimado)'],
  [25, 'muchas_personas', '18.000 BTU (estimado)'],
  [200, 'normal', '48.000 BTU (estimado)'],
];
for (const [m2, uso, esperado] of casos) {
  const got = calcular(m2, uso);
  revisar(`${m2} m2 ${uso}`, got === esperado, got || '(vacio)');
}

// 03-11-2026: casos extra desde un JSON [[m2, uso, btu], ...]. Los manda
// core/tests_btu.py con CADA celda de la tabla de /cuantos-btu-necesito/,
// para que la tabla publicada y la calculadora no puedan decir cosas distintas.
if (process.argv[3]) {
  const extra = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
  for (const [m2, uso, btu] of extra) {
    const esperado = btu.toLocaleString('es-CL') + ' BTU (estimado)';
    const got = calcular(m2, uso);
    revisar(`tabla: ${m2} m2 ${uso}`, got === esperado, `${got} en vez de ${esperado}`);
  }
}

calcular(18, 'normal');
const href = els.btnCotizarConBtu.getAttribute('href');
revisar('el boton de cotizar queda habilitado', !els.btnCotizarConBtu.classList.contains('disabled'), 'sigue disabled');
revisar('cotiza al MISMO numero de la plantilla', href.startsWith('https://wa.me/56956393341?text='), href);
revisar('el mensaje lleva la estimacion', decodeURIComponent(href).includes('12000 BTU'), href);
revisar('avisa a GA4 que se uso', eventos.length === 1 && eventos[0][0] === 'calculadora_capacidad', JSON.stringify(eventos));

calcular('', 'normal');
revisar('sin m2 no recomienda nada', !els.resultado.textContent.includes('BTU'), els.resultado.textContent);
revisar('sin m2 el boton vuelve a deshabilitarse', els.btnCotizarConBtu.classList.contains('disabled'), 'quedo habilitado');

// sin GA4 (medicion apagada o bloqueador) tiene que calcular igual
delete globalThis.window.gtag;
let revento = false;
try { calcular(18, 'normal'); } catch { revento = true; }
revisar('sin gtag calcula igual', !revento && els.resultado.textContent === '12.000 BTU (estimado)', els.resultado.textContent);

console.log(`\n${ok}/${total}`);
if (ok !== total) process.exitCode = 1;
