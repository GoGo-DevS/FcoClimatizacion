"""El SEO de las fichas de trabajo y de las paginas de servicio (07-10-2026).

Search Console: 7 de 13 fichas "descubiertas, sin indexar", y el servicio de
instalacion -- el principal -- en la posicion 41. Las fichas eran la misma
pagina con otro numero, y nada importante las enlazaba.

Lo que cuidan estas pruebas:
  . que cada ficha tenga titulo y descripcion PROPIOS y que no inventen una
    comuna que el trabajo no tiene;
  . que la ficha enlace a su servicio y el servicio a sus trabajos;
  . titulos <= 60, descripciones <= 155, y todo el JSON-LD legible, con el
    FAQPage igual a las preguntas que se ven.
"""
import json
import re

from django.test import TestCase
from django.urls import reverse

from core import seo
from projects.ficha import ficha
from projects.models import Project
from services import catalogo

BLOQUE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def _titulo(html):
    return html.split("<title>", 1)[1].split("</title>", 1)[0]


def _meta(html):
    return re.search(r'<meta name="description" content="([^"]*)"', html).group(1)


def _h1(html):
    return re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1)).strip()


def _jsonld(html):
    return [json.loads(b) for b in BLOQUE.findall(html)]


class FichaDeTrabajoTests(TestCase):

    def setUp(self):
        self.inst = [Project.objects.create(title=f"Instalación de aire acondicionado ({n:02d})")
                     for n in (1, 2, 3)]
        self.mant = Project.objects.create(title="Mantención de aire acondicionado (01)")

    def get(self, p):
        r = self.client.get(reverse("projects:detail", args=[p.id]))
        self.assertEqual(r.status_code, 200)
        return r.content.decode()

    def test_titulo_y_h1_dicen_que_se_hizo_sin_inventar_lugar(self):
        html = self.get(self.inst[1])
        titulo, h1 = _titulo(html), _h1(html)
        self.assertLessEqual(len(titulo), 60, titulo)
        self.assertIn("Instalación de aire acondicionado", titulo)
        self.assertEqual(h1, "Instalación de aire acondicionado, trabajo 02")
        # Sin comuna cargada, el titulo y el H1 no nombran ninguna.
        for lugar in [seo.ZONA_PRINCIPAL] + seo.COMUNAS:
            self.assertNotIn(lugar, titulo, lugar)
            self.assertNotIn(lugar, h1, lugar)

    def test_con_comuna_cargada_la_nombra(self):
        p = self.inst[0]
        p.comuna = "Lampa"
        p.save()
        html = self.get(p)
        self.assertIn("en Lampa", _titulo(html))
        self.assertIn("en Lampa", _h1(html))
        self.assertLessEqual(len(_titulo(html)), 60)

    def test_comuna_larga_no_pasa_de_60(self):
        p = self.inst[0]
        p.comuna = "Estación Central"
        f = ficha(p)
        self.assertLessEqual(len(f["titulo_seo"]), 60, f["titulo_seo"])
        self.assertIn("Estación Central", f["titulo_seo"])

    def test_la_descripcion_es_distinta_en_cada_ficha(self):
        metas = [_meta(self.get(p)) for p in self.inst]
        self.assertEqual(len(set(metas)), len(metas), metas)
        for m in metas:
            self.assertLessEqual(len(m), 155, m)

    def test_la_descripcion_generica_no_se_usa_de_meta(self):
        """Era la MISMA en todas las instalaciones: por eso eran duplicadas."""
        from projects.management.commands.fill_metadata import DESCRIPCION_POR_FAMILIA
        p = self.inst[0]
        p.description = DESCRIPCION_POR_FAMILIA["instalacion"]
        p.save()
        self.assertNotEqual(_meta(self.get(p)), DESCRIPCION_POR_FAMILIA["instalacion"])

    def test_la_descripcion_que_escribe_francisco_si_se_usa(self):
        p = self.inst[0]
        p.description = "Split en dormitorio de segundo piso con cañería por fachada."
        p.save()
        self.assertEqual(_meta(self.get(p)), p.description)

    def test_enlaza_a_su_servicio_y_a_otros_trabajos(self):
        html = self.get(self.inst[0])
        self.assertIn('href="/servicios/instalacion-aire-acondicionado/"', html)
        for otro in self.inst[1:]:
            self.assertIn(f'href="/trabajos/{otro.id}/"', html)
        # y no se enlaza a si mismo ni a otra familia como "otros trabajos"
        bloque = html.split('id="otros-trabajos"', 1)[1]
        self.assertNotIn(f'href="/trabajos/{self.inst[0].id}/"', bloque)
        self.assertNotIn(f'href="/trabajos/{self.mant.id}/"', bloque)

    def test_mantencion_enlaza_a_mantencion(self):
        html = self.get(self.mant)
        self.assertIn('href="/servicios/mantencion-aire-acondicionado/"', html)

    def test_jsonld_legible_con_migas_al_servicio(self):
        datos = _jsonld(self.get(self.inst[0]))
        migas = [d for d in datos if d["@type"] == "BreadcrumbList"][0]
        nombres = [i["name"] for i in migas["itemListElement"]]
        self.assertIn("Instalación de aire acondicionado", nombres)

    def test_sin_comentarios_de_plantilla_impresos(self):
        for p in (self.inst[0], self.mant):
            self.assertNotIn("{#", self.get(p))
        self.assertNotIn("{#", self.client.get(reverse("projects:list")).content.decode())

    def test_el_listado_ya_no_dice_proyecto_en_cada_tarjeta(self):
        """El badge buscaba "Instalacion" sin tilde: con los titulos nuevos
        TODAS las tarjetas decian "Proyecto"."""
        html = self.client.get(reverse("projects:list")).content.decode()
        badges = re.findall(r'project-badge">([^<]*)<', html)
        self.assertIn("Instalación", badges)
        self.assertIn("Mantención", badges)
        self.assertNotIn("Proyecto", badges)


class PaginasDeServicioTests(TestCase):

    def setUp(self):
        self.inst = Project.objects.create(title="Instalación de aire acondicionado (01)")
        self.mant = Project.objects.create(title="Mantención de aire acondicionado (01)")

    def get(self, slug):
        r = self.client.get(reverse("services:detail", args=[slug]))
        self.assertEqual(r.status_code, 200)
        return r.content.decode()

    def test_titulos_y_descripciones_caben(self):
        for s in catalogo.SERVICIOS:
            html = self.get(s["slug"])
            self.assertLessEqual(len(_titulo(html)), 60, _titulo(html))
            self.assertLessEqual(len(_meta(html)), 155, _meta(html))
            self.assertNotIn("comunas cercanas", _meta(html))
            self.assertNotIn("{#", html)

    def test_el_h1_nombra_la_zona_principal(self):
        for slug in ("instalacion-aire-acondicionado", "reparacion-aire-acondicionado",
                     "venta-equipos-climatizacion"):
            self.assertIn(seo.ZONA_PRINCIPAL, _h1(self.get(slug)), slug)

    def test_el_faqpage_es_exactamente_lo_que_se_ve(self):
        for s in catalogo.SERVICIOS:
            html = self.get(s["slug"])
            faq = [d for d in _jsonld(html) if d["@type"] == "FAQPage"][0]
            marcadas = [q["name"] for q in faq["mainEntity"]]
            visibles = re.findall(r"<summary>(.*?)</summary>", html, re.S)
            self.assertEqual(marcadas, [v.strip() for v in visibles], s["slug"])
            self.assertTrue(any(seo.ZONA_PRINCIPAL in m for m in marcadas), s["slug"])

    def test_cada_servicio_publica_las_comunas_de_la_lista(self):
        html = self.get("instalacion-aire-acondicionado")
        bloque = html.split("Dónde trabajamos", 1)[1].split("</ul>", 1)[0]
        for comuna in seo.COMUNAS:
            self.assertIn(comuna, bloque, comuna)

    def test_instalacion_enlaza_sus_trabajos_y_no_los_de_mantencion(self):
        html = self.get("instalacion-aire-acondicionado")
        bloque = html.split('id="trabajos-servicio"', 1)[1].split("</section>", 1)[0]
        self.assertIn(f'href="/trabajos/{self.inst.id}/"', bloque)
        self.assertNotIn(f'href="/trabajos/{self.mant.id}/"', bloque)

    def test_mantencion_enlaza_sus_trabajos(self):
        html = self.get("mantencion-aire-acondicionado")
        self.assertIn(f'href="/trabajos/{self.mant.id}/"', html)

    def test_reparacion_no_muestra_trabajos_que_no_son_reparaciones(self):
        self.assertNotIn('id="trabajos-servicio"', self.get("reparacion-aire-acondicionado"))
