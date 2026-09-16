"""Deja los trabajos listos para publicar, SIN inventarles datos.

QUE HACIA ANTES (y por que se cambio, 16-09-2026)
-------------------------------------------------
Este comando rellenaba cada trabajo con `random.choice`:

    project.comuna = random.choice(comunas)     # "La Serena", "Maipu"...
    project.brand  = random.choice(BRANDS)      # "Gree", "Samsung"...
    project.btu    = random.choice(BTU_HOME)    # 9000, 12000, 18000...

El sitio publicaba entonces "Mantencion limpieza - Coquimbo (07) - La Serena -
Gree - 30000 BTU" sobre una foto de la que solo sabemos que es una mantencion.
Un dato asi no es un adorno: alguien puede llamar preguntando por ese trabajo, o
elegir a FCO porque cree que atiende en su comuna.

AHORA: la comuna, la region, la marca y los BTU quedan VACIOS. El sitio los
muestra solo si alguien los completa desde el panel, y mientras tanto no dice
nada de ellos. Lo unico que se completa es la descripcion, y describe lo que
SIEMPRE incluye ese servicio, no el trabajo particular.
"""
from django.core.management.base import BaseCommand

from projects.models import Project
from projects.utils import is_segmented_title

# Lo que se puede afirmar de CUALQUIER trabajo de esa familia, sin conocerlo.
DESCRIPCION_POR_FAMILIA = {
    "instalacion": (
        "Instalación con canalización, prueba de funcionamiento y entrega del "
        "equipo operativo."
    ),
    "mantencion": (
        "Mantención con limpieza de filtros y unidad, revisión general y prueba "
        "de funcionamiento."
    ),
    "cliente": "Trabajo realizado por FCO Climatización.",
}

# Los datos que ANTES se inventaban. Se listan para que la prueba pueda
# comprobar que este comando ya no los escribe.
CAMPOS_QUE_NO_SE_INVENTAN = ("comuna", "region", "brand", "btu")


def _family(title: str):
    titulo = (title or "").lower()
    if titulo.startswith(("instalación", "instalacion")):
        return "instalacion"
    if titulo.startswith(("mantención", "mantencion")):
        return "mantencion"
    return "cliente"


class Command(BaseCommand):
    help = "Completa la descripción de los trabajos y marca destacados. No inventa datos."

    def add_arguments(self, parser):
        parser.add_argument("--only-missing", action="store_true",
                            help="Solo completa lo que esté vacío.")
        parser.add_argument("--set-featured", action="store_true",
                            help="Marca los trabajos del portafolio como destacados.")
        parser.add_argument(
            "--clear-featured-non-segmented",
            action="store_true",
            help="Desmarca destacados fuera del portafolio.",
        )

    def handle(self, *args, **options):
        only_missing = options["only_missing"]
        set_featured = options["set_featured"]

        projects = [p for p in Project.objects.all() if is_segmented_title(p.title)]
        segmented_ids = {p.id for p in projects}
        if options["clear_featured_non_segmented"]:
            Project.objects.exclude(id__in=segmented_ids).filter(featured=True).update(featured=False)

        updated = 0
        for project in projects:
            familia = _family(project.title)
            if not only_missing or not project.description:
                project.description = DESCRIPCION_POR_FAMILIA[familia]
            if set_featured:
                project.featured = True
            project.save(update_fields=["description", "featured"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"OK: {updated} trabajos listos. Comuna, marca y BTU quedan vacíos "
            f"a propósito: los completa el cliente desde el panel."))
