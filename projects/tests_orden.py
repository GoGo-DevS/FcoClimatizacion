"""El orden del portafolio.

La portada muestra 6 de los 12 trabajos y, dentro de cada tipo, tomaba los tres
MAS ANTIGUOS. Mirando las 12 fotos juntas eso dejaba primera la sala de clases
-- oscura, con estanterias y el equipo perdido arriba -- y publicaba una donde
no se ve ningun equipo, mientras el split abierto con los filtros a la vista
quedaba fuera.

Ahora manda `Project.orden`, que Francisco edita desde el panel.
"""
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from projects.models import Project


class OrdenDelPortafolioTests(TestCase):

    def _trabajo(self, titulo, orden=100, featured=True):
        return Project.objects.create(title=titulo, featured=featured, orden=orden)

    def test_el_orden_manda_sobre_la_fecha(self):
        viejo = self._trabajo("Instalación de aire acondicionado (01)", orden=10)
        nuevo = self._trabajo("Instalación de aire acondicionado (02)", orden=20)
        # `nuevo` se creo despues: con el orden anterior (-created_at) iria primero
        self.assertEqual(list(Project.objects.all()), [viejo, nuevo])

    def test_a_igual_orden_sigue_mandando_la_fecha(self):
        primero = self._trabajo("Instalación de aire acondicionado (01)")
        segundo = self._trabajo("Instalación de aire acondicionado (02)")
        self.assertEqual(list(Project.objects.all()), [segundo, primero])

    def test_la_portada_respeta_el_orden_dentro_de_cada_tipo(self):
        """Lo que motivo todo: la peor foto de cada tipo abria la portada."""
        self._trabajo("Instalación de aire acondicionado (07)", orden=100)   # la fea
        buena = self._trabajo("Instalación de aire acondicionado (04)", orden=10)
        self._trabajo("Mantención de aire acondicionado (06)", orden=60)
        mejor = self._trabajo("Mantención de aire acondicionado (03)", orden=20)

        destacados = self.client.get("/").context["featured_projects"]
        self.assertEqual(destacados[0], buena, "la portada no abre con la mejor instalación")
        self.assertEqual(destacados[1], mejor, "no intercala con la mejor mantención")

    def test_la_portada_sigue_intercalando(self):
        """El intercalado es anterior a esto y no se puede perder: sin el,
        salian 6 mantenciones seguidas y parecia que solo hacen eso."""
        for i in range(4):
            self._trabajo(f"Mantención de aire acondicionado (0{i+1})", orden=i)
        for i in range(4):
            self._trabajo(f"Instalación de aire acondicionado (0{i+1})", orden=50 + i)

        tipos = ["M" if p.title.startswith("Mant") else "I"
                 for p in self.client.get("/").context["featured_projects"]]
        self.assertEqual(tipos, ["I", "M", "I", "M", "I", "M"], tipos)


class ComandoOrdenarTests(TestCase):
    """El comando mapea por TITULO, no por id: los importadores del build
    borran y recrean los trabajos en cada despliegue, asi que los ids cambian.
    El titulo no: "(03)" sigue siendo el (03) despues de reimportar."""

    def _correr(self, *args):
        salida = StringIO()
        call_command("ordenar_portafolio", *args, stdout=salida, stderr=salida)
        return salida.getvalue()

    def _los_doce(self):
        from projects.management.commands.ordenar_portafolio import ORDEN
        for titulo in ORDEN:
            Project.objects.create(title=titulo, featured=True)

    def test_ordena_los_doce(self):
        self._los_doce()
        ensayo = self._correr()
        self.assertIn("ENSAYO", ensayo)
        self.assertEqual(
            Project.objects.get(title="Instalación de aire acondicionado (04)").orden, 100,
            "el ensayo escribio")

        self._correr("--confirmar")
        self.assertEqual(
            Project.objects.get(title="Instalación de aire acondicionado (04)").orden, 10)
        self.assertEqual(
            Project.objects.get(title="Mantención de aire acondicionado (03)").orden, 20)
        # la sala de clases y la pared sin equipo quedan atras
        self.assertEqual(
            Project.objects.get(title="Instalación de aire acondicionado (05)").orden, 110)

    def test_correrlo_dos_veces_no_cambia_nada(self):
        """Corre en CADA despliegue: tiene que ser idempotente."""
        self._los_doce()
        self._correr("--confirmar")
        self.assertIn("Ya estaba ordenado", self._correr("--confirmar"))

    def test_no_pisa_lo_que_movio_el_cliente(self):
        """Lo mas importante: Francisco ordena sus fotos desde el panel y el
        despliegue siguiente NO puede devolverlas a donde estaban."""
        self._los_doce()
        suya = Project.objects.get(title="Instalación de aire acondicionado (07)")
        suya.orden = 1          # la quiere primera, aunque sea la mas fea
        suya.save(update_fields=["orden"])

        salida = self._correr("--confirmar")
        suya.refresh_from_db()
        self.assertEqual(suya.orden, 1, "el despliegue le deshizo el orden")
        self.assertIn("se respeta", salida)

    def test_con_forzar_si_la_reordena(self):
        self._los_doce()
        suya = Project.objects.get(title="Instalación de aire acondicionado (07)")
        suya.orden = 1
        suya.save(update_fields=["orden"])
        self._correr("--confirmar", "--forzar")
        suya.refresh_from_db()
        self.assertEqual(suya.orden, 100)

    def test_sin_los_trabajos_no_revienta(self):
        salida = self._correr("--confirmar")
        self.assertIn("no existe", salida)

    def test_el_orden_sobrevive_al_reimport(self):
        """Los importadores borran y recrean; `_segmented_import` rescata por
        titulo lo que edita el cliente, y el orden tiene que ir ahi."""
        import inspect
        from projects.management.commands import _segmented_import
        fuente = inspect.getsource(_segmented_import)
        bloque = fuente.split("guardado = {", 1)[1].split("}", 1)[0]
        self.assertIn('"orden"', bloque,
                      "el orden no se rescata: el deploy siguiente lo borra")
