from django.core.management.base import BaseCommand
from projects.models import Project

class Command(BaseCommand):
    help = "Elimina proyectos por título exacto (y sus imágenes)."

    def add_arguments(self, parser):
        parser.add_argument("--titles", nargs="+", required=True, help="Lista de títulos exactos")

    def handle(self, *args, **opts):
        titles = opts["titles"]
        qs = Project.objects.filter(title__in=titles)
        count = qs.count()
        for p in qs:
            p.delete()
        self.stdout.write(self.style.SUCCESS(f"OK ✅ Eliminados {count} proyectos: {titles}"))