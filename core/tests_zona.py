"""La pagina de Ciudad de los Valles (core/zonas.py).

Lo que se cuida: que la pagina exista con su keyword en la URL, el titulo y el
H1; que el FAQ marcado sea el visible; que este en el sitemap; y que el resto
del sitio la ENLACE, que es como Google entiende que es la pagina importante
del sector. Una pagina que nadie enlaza es una pagina que no se indexa.
"""
import json
import re

from django.test import TestCase

from core import seo, zonas

RUTA = "/aire-acondicionado-ciudad-de-los-valles/"


def _json_ld(html):
    return [json.loads(b) for b in re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]


class PaginaZonaTests(TestCase):

    def setUp(self):
        self.r = self.client.get(RUTA)
        self.html = self.r.content.decode()

    def test_la_pagina_existe(self):
        self.assertEqual(self.r.status_code, 200)

    def test_una_zona_que_no_existe_da_404(self):
        # Nunca una pagina vacia: una comuna sin confirmar no tiene pagina.
        self.assertEqual(self.client.get("/aire-acondicionado-renca/").status_code, 404)

    def test_titulo_h1_y_meta_nombran_el_sector(self):
        titulo = self.html.split("<title>", 1)[1].split("</title>", 1)[0]
        self.assertIn("Ciudad de los Valles", titulo)
        self.assertLessEqual(len(titulo), 60, titulo)
        h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", self.html, re.S)
        self.assertEqual(h1s, ["Aire acondicionado en Ciudad de los Valles"])
        meta = re.search(r'<meta name="description" content="([^"]*)"', self.html).group(1)
        self.assertIn("Ciudad de los Valles", meta)
        self.assertLessEqual(len(meta), 160, meta)
        self.assertNotIn("\n", meta)

    def test_canonical_absoluto_a_si_misma(self):
        self.assertIn(f'<link rel="canonical" href="{seo.DOMINIO}{RUTA}"', self.html)

    def test_el_faq_marcado_es_el_que_se_ve(self):
        faq = next(b for b in _json_ld(self.html) if b.get("@type") == "FAQPage")
        for q in faq["mainEntity"]:
            self.assertIn(f"<summary>{q['name']}</summary>", self.html, q["name"])

    def test_la_miga_es_el_h1(self):
        migas = next(b for b in _json_ld(self.html) if b.get("@type") == "BreadcrumbList")
        ultimo = migas["itemListElement"][-1]
        self.assertEqual(ultimo["name"], "Aire acondicionado en Ciudad de los Valles")
        self.assertEqual(ultimo["item"], f"{seo.DOMINIO}{RUTA}")

    def test_el_sector_es_un_place_dentro_de_pudahuel(self):
        """No es una comuna: declararlo City seria falso."""
        servicio = next(b for b in _json_ld(self.html) if b.get("@type") == "Service")
        area = servicio["areaServed"]
        self.assertEqual(area["@type"], "Place")
        self.assertEqual(area["containedInPlace"]["name"], "Pudahuel")

    def test_enlaza_a_los_cuatro_servicios(self):
        from services import catalogo
        for s in catalogo.SERVICIOS:
            self.assertIn(f'href="/servicios/{s["slug"]}/"', self.html, s["slug"])

    def test_el_whatsapp_dice_desde_donde_escribe(self):
        self.assertIn("estoy%20en%20Ciudad%20de%20los%20Valles", self.html)


class EnlacesHaciaLaZonaTests(TestCase):
    """Sin enlaces internos la pagina queda huerfana y Google no la prioriza."""

    def _enlaza(self, url):
        html = self.client.get(url).content.decode()
        return f'href="{RUTA}"' in html

    def test_la_portada_la_enlaza(self):
        self.assertTrue(self._enlaza("/"))

    def test_cada_servicio_la_enlaza(self):
        from services import catalogo
        for s in catalogo.SERVICIOS:
            self.assertTrue(self._enlaza(f"/servicios/{s['slug']}/"), s["slug"])

    def test_el_pie_la_enlaza_en_todo_el_sitio(self):
        self.assertTrue(self._enlaza("/trabajos/"))

    def test_esta_en_el_sitemap(self):
        xml = self.client.get("/sitemap.xml").content.decode()
        self.assertIn(f"{RUTA}</loc>", xml)

    def test_el_negocio_declara_el_sector(self):
        nombres = [a["name"] for a in seo.datos_del_negocio()["areaServed"]]
        self.assertIn("Ciudad de los Valles", nombres)

    def test_la_ruta_sale_de_los_datos(self):
        self.assertEqual(zonas.ruta(zonas.ZONAS[0]), RUTA)


class MaipuTests(TestCase):
    """19-10-2026: Maipu confirmada. Es comuna, no sector."""
    RUTA = "/aire-acondicionado-maipu/"

    def setUp(self):
        self.r = self.client.get(self.RUTA)
        self.html = self.r.content.decode()

    def test_existe_con_su_titulo(self):
        self.assertEqual(self.r.status_code, 200)
        titulo = self.html.split("<title>", 1)[1].split("</title>", 1)[0]
        self.assertIn("Maipú", titulo)
        self.assertLessEqual(len(titulo), 60, titulo)

    def test_es_city_y_no_place(self):
        servicio = next(b for b in _json_ld(self.html) if b.get("@type") == "Service")
        self.assertEqual(servicio["areaServed"]["@type"], "City")
        # y el negocio no la declara dos veces
        nombres = [a["name"] for a in seo.datos_del_negocio()["areaServed"]]
        self.assertEqual(nombres.count("Maipú"), 1)

    def test_no_se_lista_a_si_misma_y_enlaza_a_la_base(self):
        cerca = self.html.split("También llegamos cerca", 1)[1]
        self.assertNotIn(">Maipú<", cerca)
        self.assertIn(f'href="{RUTA}"', cerca)

    def test_no_copia_el_texto_de_ciudad_de_los_valles(self):
        """Dos paginas con el mismo texto compiten entre si (regla 1)."""
        cdlv = zonas.zona("ciudad-de-los-valles")
        maipu = zonas.zona("maipu")
        textos_maipu = maipu["intro"] + [s["titulo"] for s in maipu["secciones"]]
        for t in cdlv["intro"] + [s["titulo"] for s in cdlv["secciones"]]:
            self.assertNotIn(t, textos_maipu)

    def test_la_portada_y_los_servicios_la_enlazan(self):
        self.assertIn(f'href="{self.RUTA}"', self.client.get("/").content.decode())
        self.assertIn(f'href="{self.RUTA}"', self.client.get(
            "/servicios/mantencion-aire-acondicionado/").content.decode())

    def test_esta_en_el_sitemap(self):
        self.assertIn(f"{self.RUTA}</loc>", self.client.get("/sitemap.xml").content.decode())

    def test_una_comuna_sin_pagina_va_sin_enlace(self):
        """Nunca un enlace a un 404."""
        self.assertIn(("Renca", None), zonas.enlazar(["Renca"]))
