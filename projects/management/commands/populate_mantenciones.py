import random

from django.core.management.base import BaseCommand
from django.db.models import Count

from projects.models import Project


COMUNAS_RM = [
    "Santiago",
    "Maipu",
    "Pudahuel",
    "Providencia",
    "Las Condes",
    "Nunoa",
    "La Florida",
    "San Bernardo",
]

BRANDS = ["CLARK", "Kendal", "Anwo", "Midea", "LG", "Samsung", "Gree", "Hisense"]

DESCRIPTIONS = [
    "Mantencion preventiva de aire acondicionado con limpieza, revision y prueba final.",
    "Mantencion correctiva con ajuste de funcionamiento y recomendaciones de uso.",
    "Servicio de mantencion con inspeccion general y puesta en marcha.",
]


class Command(BaseCommand):
    help = "Renombra proyectos con fotos a formato Mantencion y completa metadatos genericos."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=12, help="Cantidad de proyectos a normalizar")
        parser.add_argument("--set_featured", action="store_true", help="Marca como destacados los proyectos seleccionados")
        parser.add_argument(
            "--clear_featured",
            action="store_true",
            help="Limpia destacados antes de aplicar --set_featured",
        )

    def handle(self, *args, **options):
        count = max(options["count"], 0)
        set_featured = options["set_featured"]
        clear_featured = options["clear_featured"]

        qs = (
            Project.objects
            .annotate(image_count=Count("images"))
            .filter(image_count__gt=0)
            .order_by("-created_at", "-id")
        )

        selected = list(qs[:count])
        if not selected:
            self.stdout.write("No se encontraron proyectos con imagenes.")
            return

        if clear_featured:
            Project.objects.filter(featured=True).update(featured=False)

        updated = 0
        for idx, project in enumerate(selected, start=1):
            project.title = f"Mantencion de aire acondicionado ({idx:02d})"
            project.region = project.region or "RM"
            project.comuna = project.comuna or random.choice(COMUNAS_RM)
            project.project_type = project.project_type or "local"
            project.brand = project.brand or random.choice(BRANDS)
            project.btu = project.btu or random.choice([9000, 12000, 18000, 24000, 30000, 36000])
            project.description = project.description or random.choice(DESCRIPTIONS)

            if set_featured:
                project.featured = True

            project.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"OK: actualizados {updated} proyectos de mantencion."))
