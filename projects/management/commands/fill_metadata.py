import random

from django.core.management.base import BaseCommand

from projects.models import Project
from projects.utils import is_segmented_title

REGION_COMUNAS = {
    "RM": ["Santiago", "Maipu", "Pudahuel", "Providencia", "Las Condes", "Nunoa"],
    "Valparaiso": ["Vina del Mar", "Valparaiso", "Quilpue"],
    "Antofagasta": ["Antofagasta", "Calama"],
    "Coquimbo": ["La Serena", "Coquimbo"],
    "Biobio": ["Concepcion", "Talcahuano"],
}

BRANDS = ["CLARK", "Kendal", "Anwo", "Midea", "LG", "Samsung", "Gree", "Hisense"]
BTU_HOME = [9000, 12000, 18000, 24000]
BTU_COMMERCIAL = [18000, 24000, 30000, 36000, 48000]

DESCRIPTIONS = {
    "instalacion": [
        "Instalacion profesional con canalizacion, pruebas de funcionamiento y entrega operativa.",
        "Proyecto de instalacion con terminaciones limpias y puesta en marcha validada.",
        "Instalacion ejecutada con recomendaciones de uso y verificacion final del equipo.",
    ],
    "mantencion": [
        "Mantencion preventiva con limpieza, revision general y prueba de rendimiento.",
        "Mantencion correctiva con ajuste de parametros y chequeo de funcionamiento.",
        "Servicio de mantencion y limpieza de filtros con puesta a punto final.",
    ],
    "cliente": [
        "Trabajo realizado con estandar tecnico, limpieza de area y validacion final.",
        "Proyecto ejecutado con verificacion de funcionamiento y recomendaciones de uso.",
        "Servicio completado con pruebas operativas y cierre tecnico del trabajo.",
    ],
}


def _parse_region(title: str):
    region = "RM"
    if " - " not in title:
        return region
    right = title.split(" - ", 1)[1]
    region = right.split("(", 1)[0].strip()
    return region or "RM"


def _family(title: str):
    if title.startswith("Instalacion "):
        return "instalacion"
    if title.startswith("Mantencion "):
        return "mantencion"
    return "cliente"


def _project_type_from_title(title: str):
    lower = title.lower()
    if "oficina" in lower or "comercial" in lower:
        return "local"
    if "residencial" in lower:
        return random.choice(["casa", "depto"])
    if "multipunto" in lower:
        return random.choice(["local", "casa"])
    return random.choice(["casa", "depto", "local"])


class Command(BaseCommand):
    help = "Completa metadata de proyectos segmentados (region, comuna, brand, btu, project_type, description)."

    def add_arguments(self, parser):
        parser.add_argument("--only-missing", action="store_true", help="Solo completa campos vacios.")
        parser.add_argument("--set-featured", action="store_true", help="Marca segmentados como destacados.")
        parser.add_argument(
            "--clear-featured-non-segmented",
            action="store_true",
            help="Desmarca destacados fuera del conjunto segmentado.",
        )

    def handle(self, *args, **options):
        only_missing = options["only_missing"]
        set_featured = options["set_featured"]
        clear_featured_non_segmented = options["clear_featured_non_segmented"]

        projects = [p for p in Project.objects.all() if is_segmented_title(p.title)]
        updated = 0

        segmented_ids = {p.id for p in projects}
        if clear_featured_non_segmented:
            Project.objects.exclude(id__in=segmented_ids).filter(featured=True).update(featured=False)

        for project in projects:
            family = _family(project.title)
            region = _parse_region(project.title)
            comunas = REGION_COMUNAS.get(region) or REGION_COMUNAS["RM"]

            if not only_missing or not project.region:
                project.region = region
            if not only_missing or not project.comuna:
                project.comuna = random.choice(comunas)
            if not only_missing or not project.brand:
                project.brand = random.choice(BRANDS)
            if not only_missing or not project.project_type:
                project.project_type = _project_type_from_title(project.title)
            if not only_missing or not project.btu:
                if family == "instalacion":
                    project.btu = random.choice(BTU_COMMERCIAL if project.project_type == "local" else BTU_HOME)
                elif family == "mantencion":
                    project.btu = random.choice(BTU_HOME + [30000])
                else:
                    project.btu = random.choice(BTU_HOME + [30000, 36000])
            if not only_missing or not project.description or project.description == "Pendiente de metadata.":
                project.description = random.choice(DESCRIPTIONS[family])
            if set_featured:
                project.featured = True

            project.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"OK: metadata completada en {updated} proyectos segmentados."))
