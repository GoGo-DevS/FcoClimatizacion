"""Lo que el portafolio NO puede volver a hacer.

Estas pruebas existen por dos defectos reales del sitio ya publicado:

  1. los datos de cada trabajo (comuna, region, marca, BTU) se inventaban con
     `random.choice`, asi que el sitio afirmaba "La Serena - Gree - 30000 BTU"
     sobre fotos de las que solo se sabia que eran una mantencion;
  2. se publicaban capturas de pantalla de Instagram y selfies de clientes con
     la cara visible, en vez del trabajo.
"""
import io
import zipfile
from pathlib import Path
from tempfile import mkdtemp

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from projects.management.commands._segmented_import import (
    es_captura_de_pantalla,
    import_segmented_zip,
)
from projects.models import Project
from projects.utils import is_segmented_title

CARPETA = mkdtemp()


def imagen(ancho, alto, color=(120, 140, 160)):
    buffer = io.BytesIO()
    Image.new("RGB", (ancho, alto), color).save(buffer, format="JPEG")
    return buffer.getvalue()


def zip_con(imagenes, nombre="fotos.zip"):
    ruta = Path(CARPETA) / nombre
    with zipfile.ZipFile(ruta, "w") as z:
        for nombre_foto, datos in imagenes:
            z.writestr(nombre_foto, datos)
    return ruta


class SegmentationTests(TestCase):

    def test_is_segmented_title(self):
        # El formato NUEVO (16-09-2026): sin región, porque la región se
        # inventaba. El viejo se sigue aceptando para no dejar sin portafolio a
        # una base que todavía no se ha vuelto a importar.
        self.assertTrue(is_segmented_title("Instalación de aire acondicionado (01)"))
        self.assertTrue(is_segmented_title("Mantención de aire acondicionado (07)"))
        self.assertTrue(is_segmented_title("Instalacion residencial - RM (01)"))
        self.assertTrue(is_segmented_title("Mantencion preventiva - Valparaiso (06)"))
        self.assertFalse(is_segmented_title("Centro Educacional Gaspar Cabrales"))
        self.assertFalse(is_segmented_title(""))

    def test_projects_list_shows_only_segmented_titles(self):
        Project.objects.create(title="Instalación de aire acondicionado (01)", featured=True)
        Project.objects.create(title="Centro Educacional Gaspar Cabrales", featured=True)

        response = self.client.get(reverse("projects:list"))

        self.assertContains(response, "Instalación de aire acondicionado (01)")
        self.assertNotContains(response, "Centro Educacional Gaspar Cabrales")


@override_settings(MEDIA_ROOT=CARPETA)
class ElImportadorNoInventaDatos(TestCase):

    def importar(self, imagenes, family="instalacion"):
        return import_segmented_zip(
            zip_path=zip_con(imagenes), family=family,
            per_project=8, base_projects=8, clear_existing=True)

    def test_no_escribe_comuna_region_marca_ni_btu(self):
        """Antes se rellenaban con random y el sitio los publicaba."""
        self.importar([("instalaciones/1.jpg", imagen(1200, 900))])
        proyecto = Project.objects.get()
        self.assertEqual(proyecto.comuna, "")
        self.assertEqual(proyecto.region, "")
        self.assertEqual(proyecto.brand, "")
        self.assertIsNone(proyecto.btu)

    def test_el_titulo_es_el_mismo_si_se_importa_de_nuevo(self):
        """Con random, cada despliegue renombraba los trabajos."""
        fotos = [(f"instalaciones/{i}.jpg", imagen(1200, 900)) for i in range(3)]
        self.importar(fotos)
        primero = sorted(Project.objects.values_list("title", flat=True))
        self.importar(fotos)
        self.assertEqual(sorted(Project.objects.values_list("title", flat=True)), primero)
        self.assertEqual(primero, ["Instalación de aire acondicionado (01)"])

    def test_el_titulo_no_nombra_una_region(self):
        self.importar([("instalaciones/1.jpg", imagen(1200, 900))])
        titulo = Project.objects.get().title
        for region in ("RM", "Antofagasta", "Coquimbo", "Biobio", "Valparaiso"):
            self.assertNotIn(region, titulo)
        self.assertTrue(is_segmented_title(titulo))

    def test_la_mantencion_se_distingue_de_la_instalacion(self):
        self.importar([("mantenciones/1.jpg", imagen(1200, 900))], family="mantencion")
        self.assertTrue(Project.objects.get().title.startswith("Mantención"))

    def test_reimportar_borra_los_trabajos_con_el_titulo_viejo(self):
        """Si no, los que traen la región inventada quedan publicados para siempre."""
        Project.objects.create(title="Instalacion split mural - Antofagasta (03)")
        self.importar([("instalaciones/1.jpg", imagen(1200, 900))])
        self.assertEqual(Project.objects.count(), 1)
        self.assertNotIn("Antofagasta", Project.objects.get().title)


class NoSePublicanCapturasDePantalla(TestCase):

    def test_reconoce_una_captura_vertical_por_su_proporcion(self):
        # Pantalla completa de un teléfono: 720x1600.
        self.assertTrue(es_captura_de_pantalla(imagen(720, 1600)))

    def test_una_panoramica_horizontal_no_es_captura(self):
        """Pasó de verdad: la regla aplicada a las dos orientaciones descartó 5
        fotos buenas de salas de clase tomadas en panorámica."""
        self.assertFalse(es_captura_de_pantalla(imagen(1600, 720)))
        self.assertFalse(es_captura_de_pantalla(imagen(2000, 800)))

    def test_una_foto_vertical_normal_no_es_captura(self):
        # 3:4 y 9:16 son fotos de cámara, y son la mayoría del portafolio.
        self.assertFalse(es_captura_de_pantalla(imagen(1200, 1600)))
        self.assertFalse(es_captura_de_pantalla(imagen(1080, 1920)))
        self.assertFalse(es_captura_de_pantalla(imagen(1600, 1200)))

    def test_reconoce_la_captura_por_las_barras_negras(self):
        """Una captura recortada mantiene la barra de estado arriba y la de
        navegación abajo: dos franjas negras planas."""
        from PIL import Image as Im
        import io as _io
        captura = Im.new("RGB", (1000, 1300), (240, 240, 240))
        for y in list(range(0, 60)) + list(range(1240, 1300)):
            for x in range(0, 1000, 2):
                captura.putpixel((x, y), (8, 8, 8))
                captura.putpixel((x + 1, y), (8, 8, 8))
        buffer = _io.BytesIO()
        captura.save(buffer, format="JPEG", quality=95)
        self.assertTrue(es_captura_de_pantalla(buffer.getvalue()))

    def test_un_archivo_ilegible_no_rompe_la_importacion(self):
        self.assertFalse(es_captura_de_pantalla(b"esto no es una imagen"))

    @override_settings(MEDIA_ROOT=CARPETA)
    def test_la_captura_no_entra_al_portafolio(self):
        resultado = import_segmented_zip(
            zip_path=zip_con([("instalaciones/foto.jpg", imagen(1200, 900)),
                              ("instalaciones/pantallazo.jpg", imagen(720, 1600))],
                             nombre="mixto.zip"),
            family="instalacion", per_project=8, base_projects=8, clear_existing=True)
        self.assertEqual(resultado["total_images"], 1)
        self.assertEqual(resultado["descartadas"], 1)
        self.assertEqual(Project.objects.get().images.count(), 1)


@override_settings(MEDIA_ROOT=CARPETA)
class LasFotosDePersonasNoVanEnElPortafolio(TestCase):
    """`clientes.zip` son testimonios: caras de clientes y pantallazos de Instagram."""

    def test_el_comando_los_saca(self):
        Project.objects.create(title="Trabajo realizado - RM (08)")
        Project.objects.create(title="Trabajo realizado (02)")
        Project.objects.create(title="Instalación de aire acondicionado (01)")
        call_command("quitar_fotos_de_personas", verbosity=0)
        self.assertEqual([p.title for p in Project.objects.all()],
                         ["Instalación de aire acondicionado (01)"])

    def test_el_ensayo_no_borra(self):
        Project.objects.create(title="Trabajo realizado (02)")
        call_command("quitar_fotos_de_personas", dry_run=True, verbosity=0)
        self.assertEqual(Project.objects.count(), 1)


@override_settings(MEDIA_ROOT=CARPETA)
class LaDescripcionNoInventaElTrabajo(TestCase):

    def test_describe_el_servicio_y_no_el_caso(self):
        Project.objects.create(title="Instalación de aire acondicionado (01)")
        call_command("fill_metadata", set_featured=True, verbosity=0)
        proyecto = Project.objects.get()
        self.assertIn("canalización", proyecto.description)
        # Y sigue sin inventar lo que no se sabe.
        self.assertEqual((proyecto.comuna, proyecto.region, proyecto.brand), ("", "", ""))
        self.assertIsNone(proyecto.btu)
