// Prueba el comportamiento del script, no su presencia: simula los clics y
// comprueba que gtag recibe el evento correcto.
import fs from 'node:fs';
const src = fs.readFileSync(process.argv[2], 'utf8');

const eventos = [];
const oyentes = { click: [], submit: [] };
globalThis.window = {
  gtag: (tipo, nombre, datos) => { if (tipo === 'event') eventos.push([nombre, datos]); },
  location: { pathname: '/contacto/' },
};
globalThis.document = {
  addEventListener: (t, fn) => oyentes[t] && oyentes[t].push(fn),
};
eval(src);

const enlace = (href) => ({ target: { closest: (s) => (s === 'a[href]' ? { getAttribute: () => href } : null) } });
const casos = [
  ['https://wa.me/56912345678', 'contacto_whatsapp'],
  ['tel:+56225590108',          'contacto_telefono'],
  ['mailto:hola@x.cl',          'contacto_email'],
  ['https://instagram.com/x',   'click_instagram'],
  ['/servicios/',               null],
];
let ok = 0;
for (const [href, esperado] of casos) {
  eventos.length = 0;
  oyentes.click.forEach((fn) => fn(enlace(href)));
  const got = eventos.length ? eventos[0][0] : null;
  const bien = got === esperado;
  ok += bien;
  console.log(`  ${bien ? 'OK  ' : 'FALLA'} ${href.padEnd(30)} -> ${got || '(ninguno)'}`);
}

// formulario: valido dispara, invalido NO (si no, los intentos fallidos se
// contarian como contactos y el informe mentiria hacia arriba)
for (const [valido, esperado] of [[true, 'formulario_enviado'], [false, null]]) {
  eventos.length = 0;
  const f = { tagName: 'FORM', checkValidity: () => valido, getAttribute: (a) => (a === 'name' ? 'contacto' : null) };
  oyentes.submit.forEach((fn) => fn({ target: f }));
  const got = eventos.length ? eventos[0][0] : null;
  const bien = got === esperado;
  ok += bien;
  console.log(`  ${bien ? 'OK  ' : 'FALLA'} formulario ${valido ? 'valido  ' : 'invalido'}             -> ${got || '(ninguno)'}`);
}

// sin gtag (medicion apagada o bloqueador) no debe reventar
eventos.length = 0;
delete globalThis.window.gtag;
let revento = false;
try { oyentes.click.forEach((fn) => fn(enlace('https://wa.me/569'))); } catch { revento = true; }
ok += !revento;
console.log(`  ${!revento ? 'OK  ' : 'FALLA'} sin gtag no revienta`);
console.log(`\n${ok}/8`);
