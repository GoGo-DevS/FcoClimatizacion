"""Los datos estructurados tienen que ser JSON que Google pueda leer.

22-09-2026: el FAQ de la portada, las migas y los servicios salian con las
comillas escapadas (&quot;). Se veian en el codigo fuente, pero Google no
podia leerlos, y ninguna prueba lo notaba porque el texto "FAQPage" seguia
estando en la pagina.
"""
import json
import re

from django.template import Context, Template
from django.test import TestCase
from django.urls import reverse

BLOQUE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


class JsonLdLegible(TestCase):
    def tipos(self, url):
        html = self.client.get(url).content.decode()
        bloques = BLOQUE.findall(html)
        self.assertTrue(bloques, f"{url} sin JSON-LD")
        return [json.loads(b)["@type"] for b in bloques]  # falla si no es JSON

    def test_portada_con_faq_legible(self):
        self.assertIn("FAQPage", self.tipos(reverse("home")))

    def test_migas_legibles_en_servicios(self):
        self.assertIn("BreadcrumbList", self.tipos("/servicios/"))

    def test_un_texto_con_script_no_cierra_la_etiqueta(self):
        salida = Template("{% load seo_extras %}{{ d|como_json }}").render(
            Context({"d": {"name": "</script><b>x</b> & y"}}))
        self.assertNotIn("</script>", salida)
        self.assertEqual(json.loads(salida)["name"], "</script><b>x</b> & y")
