"""achicar_fotos (04-11-2026): las fotos del portafolio pesaban hasta 1,9 MB por ficha."""
import os
import random
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import SimpleTestCase, override_settings
from PIL import Image


def _foto_ruidosa(ruta, lado=3000):
    # Degrade con grano, guardado casi sin compresion: pesa como una foto de
    # WhatsApp (> 1 MB) y se comprime como una foto real, no como ruido puro.
    random.seed(1)
    alto = lado * 3 // 4
    img = Image.linear_gradient("L").resize((lado, alto)).convert("RGB")
    grano = Image.effect_noise((lado, alto), 40).convert("RGB")
    Image.blend(img, grano, 0.35).save(ruta, "JPEG", quality=98)


class AchicarFotos(SimpleTestCase):

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.raiz = Path(self.dir.name)
        (self.raiz / "projects" / "3").mkdir(parents=True)
        self.pesada = self.raiz / "projects" / "3" / "3_0_WhatsApp_Image.jpeg"
        _foto_ruidosa(self.pesada)
        self.liviana = self.raiz / "projects" / "3" / "chica.jpg"
        Image.new("RGB", (300, 200), "white").save(self.liviana, "JPEG")

    def tearDown(self):
        self.dir.cleanup()

    def _correr(self):
        with override_settings(MEDIA_ROOT=self.dir.name):
            call_command("achicar_fotos", stdout=StringIO())

    def test_la_pesada_queda_bajo_150_kb_con_el_mismo_nombre(self):
        self.assertGreater(self.pesada.stat().st_size, 150 * 1024)
        self._correr()
        self.assertTrue(self.pesada.exists())
        self.assertLessEqual(self.pesada.stat().st_size, 150 * 1024)
        with Image.open(self.pesada) as img:
            self.assertEqual(img.format, "JPEG")
            self.assertLessEqual(max(img.size), 1600)

    def test_la_liviana_no_se_toca(self):
        antes = self.liviana.read_bytes()
        self._correr()
        self.assertEqual(self.liviana.read_bytes(), antes)

    def test_correr_dos_veces_no_vuelve_a_comprimir(self):
        self._correr()
        despues = self.pesada.read_bytes()
        self._correr()
        self.assertEqual(self.pesada.read_bytes(), despues)

    def test_sin_carpeta_media_no_revienta(self):
        with override_settings(MEDIA_ROOT=os.path.join(self.dir.name, "no-existe")):
            call_command("achicar_fotos", stdout=StringIO())
