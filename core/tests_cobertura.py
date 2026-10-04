"""La cobertura por comuna.

El sitio decia "Región Metropolitana y comunas cercanas" en cinco lugares
distintos, escrito a mano en cada uno. Con eso compite contra toda la region y
no gana ninguna comuna: quien tiene el equipo malo busca "aire acondicionado
Ciudad de los Valles" y, antes de escribir, quiere saber si el tecnico llega
hasta su casa.

Lo que estas pruebas cuidan es que la lista viva en UN solo lugar
(core/seo.COMUNAS) y que ninguna pantalla pueda contradecirla.
"""
from django.test import TestCase

from core import seo


class ZonaTests(TestCase):

    def test_la_zona_se_arma_de_la_lista_y_no_esta_escrita_a_mano(self):
        for comuna in seo.COMUNAS:
            self.assertIn(comuna, seo.ZONA, comuna)
        self.assertIn(seo.ZONA_PRINCIPAL, seo.ZONA)
        # y se lee como una frase, no como una lista separada por comas
        self.assertIn(" y ", seo.ZONA)

    def test_ciudad_de_los_valles_va_primero(self):
        # Es el sector que pidio Francisco y por donde entra su gente.
        self.assertTrue(seo.ZONA.startswith("Ciudad de los Valles"), seo.ZONA)

    def test_ya_no_se_promete_la_region_entera(self):
        # "Region Metropolitana y comunas cercanas" no lo busca nadie.
        self.assertNotIn("comunas cercanas", seo.ZONA)
        self.assertNotIn("comunas cercanas", seo.DESCRIPCION_CORTA)

    def test_el_area_servida_son_ciudades_con_nombre(self):
        """Un AdministrativeArea generico no le sirve a Google para cruzarlo
        con la comuna de quien busca. Una lista de City si."""
        area = seo.area_servida()
        self.assertEqual(len(area), len(seo.COMUNAS))
        for ciudad in area:
            self.assertEqual(ciudad["@type"], "City")
            self.assertIn(ciudad["name"], seo.COMUNAS)
            self.assertEqual(ciudad["addressCountry"], "CL")

    def test_el_json_ld_del_negocio_publica_las_comunas(self):
        datos = seo.datos_del_negocio()
        nombres = [c["name"] for c in datos["areaServed"]]
        self.assertIn("Pudahuel", nombres)
        self.assertIn("Lampa", nombres)


class PantallasTests(TestCase):
    """Ninguna pantalla puede decir una zona distinta a la de seo.COMUNAS."""

    def test_la_portada_nombra_la_comuna_principal_y_las_demas(self):
        """Dentro de la FRANJA del hero, no en cualquier parte: "Ciudad de los
        Valles" tambien sale en el pie y en los titulos, asi que buscarla en el
        HTML entero pasaba aunque la franja no existiera."""
        html = self.client.get("/").content.decode()
        self.assertIn("hero-comunas__lista", html)
        franja = html.split("hero-comunas__lista", 1)[1].split("</ul>", 1)[0]
        self.assertIn("Ciudad de los Valles", franja)
        for comuna in seo.COMUNAS:
            self.assertIn(comuna, franja, comuna)

    def test_la_portada_ya_no_dice_comunas_cercanas(self):
        html = self.client.get("/").content.decode()
        self.assertNotIn("comunas cercanas", html)

    def test_el_pie_publica_la_cobertura_en_todas_las_paginas(self):
        """El pie se repite en todo el sitio: si la zona vive ahi, cualquier
        pagina responde "¿llegas hasta aca?" sin tener que volver a la home."""
        for ruta in ("/", "/servicios/", "/trabajos/"):
            html = self.client.get(ruta).content.decode()
            # dentro del <footer>: el nombre de la comuna sale en otros lugares
            self.assertIn("<footer", html, ruta)
            pie = html.split("<footer", 1)[1].split("</footer>", 1)[0]
            self.assertIn("Ciudad de los Valles", pie, ruta)
            self.assertIn("Lampa", pie, ruta)

    def test_la_respuesta_de_la_faq_nombra_las_comunas(self):
        html = self.client.get("/").content.decode()
        self.assertIn("¿En qué zonas atienden?", html)
        # la respuesta, no solo la pregunta
        self.assertIn("Quilicura", html)

    def test_los_titulos_de_servicio_nombran_la_comuna_y_no_santiago_a_secas(self):
        from services import catalogo
        for s in catalogo.SERVICIOS:
            titulo = s["titulo_seo"]
            self.assertTrue(
                "Ciudad de los Valles" in titulo or "Pudahuel" in titulo,
                f"{s['slug']}: {titulo}")


class MarcaTests(TestCase):
    """La paleta sale del logo, no de una plantilla."""

    def test_los_cuatro_servicios_tienen_icono(self):
        from services import catalogo
        for s in catalogo.SERVICIOS:
            self.assertIn("<svg", s.get("icono", ""), s["slug"])

    def test_el_icono_toma_el_color_de_la_tarjeta(self):
        """currentColor: al pintarse el cuadrito, el icono se pinta con el.
        Un stroke fijo quedaria azul sobre azul al pasar por encima."""
        from services import catalogo
        for s in catalogo.SERVICIOS:
            self.assertIn("currentColor", s["icono"], s["slug"])

    def test_el_sitio_usa_los_colores_del_logo(self):
        """#2060E8 y #081028 estan medidos sobre el PNG del logo. Los que habia
        (#1f6fb2, #0b3a66) no estaban en el logo: eran de plantilla."""
        from pathlib import Path
        from django.conf import settings
        css = Path(settings.BASE_DIR, "static", "css", "site.css").read_text(encoding="utf-8")
        self.assertIn("#2060E8", css)
        self.assertIn("#081028", css)
        self.assertNotIn("#1f6fb2", css)
        self.assertNotIn("#0b3a66", css)

    def test_el_boton_de_whatsapp_no_lleva_texto_blanco(self):
        """Blanco sobre el verde de WhatsApp da 1.98:1, muy debajo del 4.5 que
        pide AA -- y es el boton principal del sitio. Con #06301A da 7.33:1."""
        from pathlib import Path
        from django.conf import settings
        css = Path(settings.BASE_DIR, "static", "css", "site.css").read_text(encoding="utf-8")
        bloque = css.split(".btn-success {", 1)[1].split("}", 1)[0]
        self.assertIn("--bs-btn-color: #06301A", bloque)
