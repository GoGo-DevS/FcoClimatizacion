"""SEO de las paginas de servicio: tanda del 02-11-2026.

Cada prueba revisa la pagina como la ve Google (el HTML que responde la URL),
no solo el diccionario de services/catalogo.py: un titulo bien escrito en el
catalogo no sirve si la plantilla no lo dibuja.
"""
import html as html_lib
import json
import re

from django.test import TestCase

BLOQUE_LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
MANTENCION = "/servicios/mantencion-aire-acondicionado/"
REPARACION = "/servicios/reparacion-aire-acondicionado/"


def partes(html):
    titulo = html_lib.unescape(html.split("<title>", 1)[1].split("</title>", 1)[0].strip())
    meta = html_lib.unescape(re.search(r'<meta name="description" content="([^"]*)"', html).group(1))
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1)
    h1 = html_lib.unescape(re.sub(r"<[^>]+>|\s+", " ", h1).strip())
    return titulo, meta, h1


class MantencionTests(TestCase):
    """"limpieza aire acondicionado" es una busqueda propia y "a domicilio" se
    repite en las sugerencias de mantencion, limpieza y tecnico."""

    def setUp(self):
        r = self.client.get(MANTENCION)
        self.assertEqual(r.status_code, 200)
        self.titulo, self.meta, self.h1 = partes(r.content.decode())

    def test_el_titulo_dice_limpieza_y_sigue_nombrando_la_comuna(self):
        self.assertIn("limpieza", self.titulo)
        self.assertIn("Mantención", self.titulo)
        self.assertIn("Pudahuel", self.titulo)
        self.assertLessEqual(len(self.titulo), 60, self.titulo)

    def test_el_h1_dice_a_domicilio(self):
        self.assertIn("a domicilio", self.h1)
        self.assertIn("limpieza", self.h1)

    def test_la_descripcion_cabe_y_dice_a_domicilio(self):
        self.assertIn("a domicilio", self.meta)
        self.assertLessEqual(len(self.meta), 160, self.meta)


class ReparacionTests(TestCase):
    """El bloque de sintomas (no enfria, gotea, le falta gas) y la pregunta
    por la recarga de gas."""

    def setUp(self):
        r = self.client.get(REPARACION)
        self.assertEqual(r.status_code, 200)
        self.html = r.content.decode()

    def test_la_seccion_de_sintomas_esta_en_la_pagina(self):
        self.assertIn("No enfría, gotea o le falta gas", self.html)
        seccion = self.html.split("No enfría, gotea o le falta gas", 1)[1].split("<h2", 1)[0]
        for sintoma in ("No enfría como antes", "Gotea dentro de la casa",
                        "Gotea afuera", "Le falta gas"):
            self.assertIn(sintoma, seccion, sintoma)

    def test_la_seccion_enlaza_a_la_mantencion_y_a_la_calculadora(self):
        """Enlaces que existen: el de la mantencion responde 200 y la
        calculadora es un ancla de la portada que tiene ese id."""
        seccion = self.html.split("No enfría, gotea o le falta gas", 1)[1].split("<h2", 1)[0]
        self.assertIn(f'href="{MANTENCION}"', seccion)
        self.assertIn('href="/#capacidad"', seccion)
        self.assertEqual(self.client.get(MANTENCION).status_code, 200)
        self.assertIn('id="capacidad"', self.client.get("/").content.decode())

    def test_la_pregunta_de_la_recarga_de_gas_se_ve_y_esta_marcada(self):
        """FAQPage solo con preguntas visibles: tiene que estar en los dos."""
        pregunta = "¿Hacen recarga de gas?"
        visibles = [html_lib.unescape(p) for p in re.findall(r"<summary>(.*?)</summary>", self.html)]
        self.assertIn(pregunta, visibles)
        faq = [json.loads(b) for b in BLOQUE_LD.findall(self.html)]
        faq = [b for b in faq if b.get("@type") == "FAQPage"]
        self.assertEqual(len(faq), 1)
        marcadas = [q["name"] for q in faq[0]["mainEntity"]]
        self.assertIn(pregunta, marcadas)
        # y no hay preguntas marcadas que no se vean
        self.assertEqual(sorted(marcadas), sorted(visibles))

    def test_la_descripcion_cabe_y_dice_carga_de_gas(self):
        _, meta, _ = partes(self.html)
        self.assertIn("carga de gas", meta)
        self.assertLessEqual(len(meta), 160, meta)

    def test_no_se_publica_precio_ni_plazo(self):
        """Ni precio ni tiempo de llegada: no los ha confirmado Francisco."""
        seccion = self.html.split("No enfría, gotea o le falta gas", 1)[1].split("<h2", 1)[0]
        self.assertNotRegex(seccion, r"\$\s?\d|\d+\s?(horas|hrs|minutos)")


class TodosLosServiciosTests(TestCase):

    def test_titulos_y_descripciones_caben(self):
        from services import catalogo
        for s in catalogo.SERVICIOS:
            html = self.client.get(f"/servicios/{s['slug']}/").content.decode()
            titulo, meta, _ = partes(html)
            self.assertLessEqual(len(titulo), 60, titulo)
            self.assertLessEqual(len(meta), 160, meta)
