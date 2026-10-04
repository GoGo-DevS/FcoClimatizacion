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
    """El comando toca la base por ID. Si los ids no son los que se revisaron,
    no puede ordenar igual: pondria cualquier foto en la portada."""

    def _correr(self, *args):
        salida = StringIO()
        call_command("ordenar_portafolio", *args, stdout=salida, stderr=salida)
        return salida.getvalue()

    def test_sin_los_trabajos_no_toca_nada(self):
        otro = Project.objects.create(title="Instalación de aire acondicionado (04)",
                                      featured=True, orden=100)
        salida = self._correr("--confirmar")
        self.assertIn("NO SE TOCO NADA", salida)
        otro.refresh_from_db()
        self.assertEqual(otro.orden, 100, "escribio pese a que los ids no calzan")

    def test_si_el_titulo_no_calza_lo_nombra_y_se_detiene(self):
        p = Project.objects.create(id=4, title="Otra cosa", featured=True)
        salida = self._correr("--confirmar")
        self.assertIn("NO SE TOCO NADA", salida)
        self.assertIn("Otra cosa", salida)
        p.refresh_from_db()
        self.assertEqual(p.orden, 100)

    def test_con_los_doce_correctos_ordena(self):
        from projects.management.commands.ordenar_portafolio import ORDEN
        for pk, (titulo, _orden, _motivo) in ORDEN.items():
            Project.objects.create(id=pk, title=titulo, featured=True, orden=100)

        ensayo = self._correr()
        self.assertIn("ENSAYO", ensayo)
        self.assertEqual(Project.objects.get(id=4).orden, 100, "el ensayo escribio")

        self._correr("--confirmar")
        self.assertEqual(Project.objects.get(id=4).orden, 10)
        self.assertEqual(Project.objects.get(id=10).orden, 20)
        # la sala de clases queda atras
        self.assertEqual(Project.objects.get(id=7).orden, 100)

    def test_correrlo_dos_veces_no_cambia_nada(self):
        from projects.management.commands.ordenar_portafolio import ORDEN
        for pk, (titulo, _o, _m) in ORDEN.items():
            Project.objects.create(id=pk, title=titulo, featured=True, orden=100)
        self._correr("--confirmar")
        segunda = self._correr("--confirmar")
        self.assertIn("Ya estaba ordenado", segunda)
