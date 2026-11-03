"""La guia /cuantos-btu-necesito/ (core/btu.py), tanda SEO del 03-11-2026.

Lo que se cuida:
- que responda las busquedas del autocompletado con la palabra exacta
  (titulo, H1 y meta dentro del largo);
- que la tabla publicada diga LO MISMO que la calculadora: cada celda se le
  pasa al script real (capacidad.js) con node;
- que el FAQ marcado sea el visible, que este en el sitemap y que el sitio la
  enlace (una pagina que nadie enlaza no se indexa);
- que no publique precios ni sea una copia de la portada.
"""
import html as html_lib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.test import TestCase

from core import btu, seo
from core.similitud import parte_copiada

RUTA = "/cuantos-btu-necesito/"
BLOQUE_LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
JS = Path(settings.BASE_DIR, "static", "js", "capacidad.js")
PRUEBA_JS = Path(settings.BASE_DIR, "static", "js", "capacidad.test.mjs")


def _partes(html):
    titulo = html_lib.unescape(html.split("<title>", 1)[1].split("</title>", 1)[0].strip())
    meta = html_lib.unescape(re.search(r'<meta name="description" content="([^"]*)"', html).group(1))
    h1s = [html_lib.unescape(re.sub(r"<[^>]+>|\s+", " ", h).strip())
           for h in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)]
    return titulo, meta, h1s


class PaginaBtuTests(TestCase):

    def setUp(self):
        self.r = self.client.get(RUTA)
        self.html = self.r.content.decode()

    def test_la_pagina_existe(self):
        self.assertEqual(self.r.status_code, 200)

    def test_titulo_h1_y_meta_con_la_palabra_que_se_busca(self):
        titulo, meta, h1s = _partes(self.html)
        self.assertIn("¿Cuántos BTU necesito?", titulo)
        self.assertIn("metros cuadrados", titulo)
        self.assertLessEqual(len(titulo), 60, titulo)
        self.assertNotIn("Santiago", titulo)
        self.assertEqual(len(h1s), 1)
        self.assertIn("Cuántos BTU necesito", h1s[0])
        self.assertIn("BTU por metro cuadrado", meta)
        self.assertIn("12.000 BTU hasta 20 m²", meta)
        self.assertLessEqual(len(meta), 160, meta)

    def test_canonical_absoluto_a_si_misma(self):
        self.assertIn(f'<link rel="canonical" href="{seo.DOMINIO}{RUTA}"', self.html)

    def test_la_respuesta_corta_va_arriba(self):
        """Lo primero que se lee responde la pregunta, antes de la tabla."""
        cuerpo = self.html.split("<main", 1)[1]
        antes_de_la_tabla = cuerpo.split('id="tabla-m2"', 1)[0]
        self.assertIn("600 BTU por metro", antes_de_la_tabla)
        self.assertIn("12.000 BTU hasta 20 m²", antes_de_la_tabla)

    def test_la_tabla_publica_lo_que_da_la_formula(self):
        tabla = self.html.split('aria-labelledby="tabla-m2"', 1)[1].split("</table>", 1)[0]
        for fila in btu.tabla_por_m2():
            celda = tabla.split(f"{fila['m2']} m²", 1)[1].split("</tr>", 1)[0]
            for uso in btu.USOS:
                self.assertIn(f"{btu.miles(fila['btu'][uso])} BTU", celda, (fila["m2"], uso))
        # las piezas que mas se buscan, con su nombre
        for pieza in ("3 x 3", "4 x 4", "5 x 5"):
            self.assertIn(pieza, tabla)

    def test_la_tabla_por_equipo_responde_para_cuantos_metros(self):
        tabla = self.html.split('aria-labelledby="tabla-equipo"', 1)[1].split("</table>", 1)[0]
        self.assertIn("12.000 BTU", tabla)
        self.assertIn("hasta 20 m²", tabla)
        self.assertIn("3.020", tabla)  # frigorias de 12.000 BTU

    def test_la_tabla_y_la_calculadora_dicen_lo_mismo(self):
        """Cada celda publicada se le pasa al script real. Para la tabla por
        equipo: el maximo de m2 da ese equipo (o uno menor) y un m2 mas ya no."""
        node = shutil.which("node")
        if not node:
            self.skipTest("node no esta instalado")
        casos = []
        for fila in btu.tabla_por_m2():
            for uso in btu.USOS:
                casos.append([fila["m2"], uso, fila["btu"][uso]])
        for fila in btu.tabla_por_equipo():
            for uso in btu.USOS:
                m2 = fila["m2"][uso]
                self.assertLessEqual(btu.estimar_btu(m2, uso), fila["btu"])
                self.assertGreater(btu.estimar_btu(m2 + 1, uso), fila["btu"])
                casos.append([m2, uso, btu.estimar_btu(m2, uso)])
                casos.append([m2 + 1, uso, btu.estimar_btu(m2 + 1, uso)])
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                         encoding="utf-8") as f:
            json.dump(casos, f)
        try:
            r = subprocess.run([node, str(PRUEBA_JS), str(JS), f.name], capture_output=True,
                               text=True, encoding="utf-8", timeout=60)
        finally:
            Path(f.name).unlink()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(r.stdout.count("OK   tabla:"), len(casos), r.stdout)

    def test_tiene_la_calculadora_funcionando(self):
        for id_ in ("m2", "uso", "btnCalc", "resultado", "btnCotizarConBtu"):
            self.assertIn(f'id="{id_}"', self.html, id_)
        self.assertRegex(self.html, r'<script src="[^"]*js/capacidad\.js"[^>]*defer')

    def test_el_faq_marcado_es_el_que_se_ve(self):
        bloques = [json.loads(b) for b in BLOQUE_LD.findall(self.html)]
        faq = [b for b in bloques if b.get("@type") == "FAQPage"]
        self.assertEqual(len(faq), 1)
        marcadas = [q["name"] for q in faq[0]["mainEntity"]]
        visibles = [html_lib.unescape(p) for p in re.findall(r"<summary>(.*?)</summary>", self.html)]
        self.assertEqual(sorted(marcadas), sorted(visibles))
        self.assertIn("¿Cuántos BTU necesito para 20 m²?", visibles)

    def test_la_miga_es_la_pagina(self):
        bloques = [json.loads(b) for b in BLOQUE_LD.findall(self.html)]
        migas = next(b for b in bloques if b.get("@type") == "BreadcrumbList")
        self.assertEqual(migas["itemListElement"][-1]["item"], f"{seo.DOMINIO}{RUTA}")

    def test_enlaza_a_instalacion_y_venta(self):
        """Guia -> servicios: quien ya sabe los BTU sigue al equipo."""
        self.assertIn('href="/servicios/instalacion-aire-acondicionado/"', self.html)
        self.assertIn('href="/servicios/venta-equipos-climatizacion/"', self.html)

    def test_no_publica_precios(self):
        principal = self.html.split("<main", 1)[1].split("</main>", 1)[0]
        self.assertNotRegex(principal, r"\$\s?\d")

    def test_no_es_una_copia_de_la_portada_ni_de_la_venta(self):
        for otra in ("/", "/servicios/venta-equipos-climatizacion/"):
            parte = parte_copiada(self.html, self.client.get(otra).content.decode())
            self.assertLess(parte, 0.25, f"{otra}: {parte:.0%} del texto repetido")


class EnlacesHaciaLaGuiaTests(TestCase):
    """Sin enlaces internos la pagina queda huerfana."""

    def _enlaza(self, url):
        return f'href="{RUTA}"' in self.client.get(url).content.decode()

    def test_la_portada_la_enlaza_desde_la_calculadora(self):
        html = self.client.get("/").content.decode()
        calculadora = html.split('id="capacidad"', 1)[1].split("</section>", 1)[0]
        self.assertIn(f'href="{RUTA}"', calculadora)

    def test_el_pie_la_enlaza_en_todo_el_sitio(self):
        html = self.client.get("/trabajos/").content.decode()
        pie = html.split("<footer", 1)[1]
        self.assertIn(f'href="{RUTA}"', pie)

    def test_la_venta_la_enlaza_donde_explica_la_capacidad(self):
        self.assertTrue(self._enlaza("/servicios/venta-equipos-climatizacion/"))

    def test_esta_en_el_sitemap(self):
        xml = self.client.get("/sitemap.xml").content.decode()
        self.assertIn(f"{RUTA}</loc>", xml)

    def test_la_portada_sigue_con_su_calculadora(self):
        """La calculadora paso a un parcial: la portada la sigue mostrando."""
        html = self.client.get("/").content.decode()
        self.assertIn('id="btnCalc"', html)
        self.assertIn("¿Qué capacidad necesito?", html)
