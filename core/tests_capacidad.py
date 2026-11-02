"""La calculadora de capacidad de la portada.

Entre el 16-09 y el 02-11-2026 el boton "Calcular" no hacia nada: el rediseno
conservo el HTML de la calculadora pero no el <script> que la hacia funcionar,
que vivia dentro de home.html. Las pruebas de entonces revisaban que la
seccion estuviera, y estaba: por eso nadie lo noto.

Lo que se cuida aca es el HECHO (que al apretar el boton aparezca una
recomendacion), no la forma: la prueba de comportamiento corre el script con
node, con los mismos ids que dibuja la plantilla.
"""
import re
import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.test import TestCase

JS = Path(settings.BASE_DIR, "static", "js", "capacidad.js")
PRUEBA_JS = Path(settings.BASE_DIR, "static", "js", "capacidad.test.mjs")
IDS = ("m2", "uso", "btnCalc", "resultado", "btnCotizarConBtu")


class CalculadoraTests(TestCase):

    def setUp(self):
        self.html = self.client.get("/").content.decode()

    def test_la_portada_carga_el_script_de_la_calculadora(self):
        self.assertRegex(self.html, r'<script src="[^"]*js/capacidad\.js"[^>]*defer')

    def test_la_plantilla_tiene_los_ids_que_usa_el_script(self):
        """Si alguien renombra un id en la plantilla, el script se queda sin
        boton que escuchar y la calculadora vuelve a morir en silencio."""
        js = JS.read_text(encoding="utf-8")
        for id_ in IDS:
            self.assertIn(f'id="{id_}"', self.html, id_)
            self.assertIn(f"getElementById('{id_}')", js, id_)

    def test_el_boton_de_cotizar_trae_el_whatsapp_del_negocio(self):
        """El script toma el numero de este enlace: no hay un segundo lugar
        donde pueda quedar un telefono distinto."""
        boton = re.search(r'<a id="btnCotizarConBtu"[^>]*>', self.html, re.S)
        self.assertIsNotNone(boton)
        numero = settings.WHATSAPP_PHONE.replace("+", "").replace(" ", "")
        self.assertIn(f'href="https://wa.me/{numero}?', boton.group(0))

    def test_al_calcular_aparece_la_recomendacion(self):
        """El comportamiento: 18 m2 dan 12.000 BTU, el boton de cotizar se
        habilita con la estimacion y GA4 recibe el uso."""
        node = shutil.which("node")
        if not node:
            self.skipTest("node no esta instalado")
        r = subprocess.run([node, str(PRUEBA_JS), str(JS)], capture_output=True,
                           text=True, encoding="utf-8", timeout=60)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
