"""GoGoDevS Tree (/links/): el link de la bio de Instagram.

Cuida que exista, que no compita en Google con las paginas de verdad, que el
boton principal sea WhatsApp, que no lleve a ningun 404, y que se mida igual
que en los otros sitios (evento tree_click) solo cuando GA4 esta cargado.
"""
import re

from django.test import TestCase, override_settings


class TreeTests(TestCase):

    def _html(self):
        r = self.client.get("/links/")
        self.assertEqual(r.status_code, 200)
        return r.content.decode()

    def test_no_compite_en_google_y_no_esta_en_el_sitemap(self):
        self.assertIn('<meta name="robots" content="noindex,follow">', self._html())
        self.assertNotIn("/links/", self.client.get("/sitemap.xml").content.decode())

    def test_las_demas_paginas_siguen_indexables(self):
        html = self.client.get("/").content.decode()
        self.assertIn('content="index,follow,max-image-preview:large"', html)

    def test_va_sin_menu_ni_pie_ni_flotante(self):
        html = self._html()
        self.assertNotIn("site-nav", html)
        self.assertNotIn("site-footer", html)
        self.assertNotIn("wa-float", html)

    def test_lo_primero_es_whatsapp(self):
        html = self._html()
        primer = re.search(r'<a [^>]*href="([^"]+)"', html.split('class="tree"', 1)[1].split("tree-cabecera", 1)[1]).group(1)
        self.assertIn("wa.me/", primer)
        self.assertIn("vengo%20de%20Instagram", primer)

    def test_ningun_enlace_interno_da_404(self):
        html = self._html()
        internos = set(re.findall(r'<a [^>]*href="(/[^"#]*)', html)) - {"/links/"}
        self.assertTrue(internos)
        for ruta in internos:
            self.assertEqual(self.client.get(ruta).status_code, 200, ruta)

    def test_enlaza_servicios_y_zonas(self):
        html = self._html()
        self.assertIn('href="/servicios/mantencion-aire-acondicionado/"', html)
        self.assertIn('href="/aire-acondicionado-ciudad-de-los-valles/"', html)
        self.assertIn('href="/aire-acondicionado-maipu/"', html)

    def test_con_ga4_carga_el_evento_tree_click(self):
        with override_settings(GA4_MEASUREMENT_ID="G-PRUEBA1234"):
            html = self._html()
        self.assertIn("js/tree.js", html)

    def test_sin_ga4_no_se_le_pide_nada_a_google(self):
        with override_settings(GA4_MEASUREMENT_ID=""):
            html = self._html()
        self.assertNotIn("googletagmanager", html)
        self.assertNotIn("tree.js", html)

    def test_el_comentario_no_se_imprime(self):
        html = self._html()
        self.assertNotIn("{%", html)
        self.assertNotIn("embudo", html)
