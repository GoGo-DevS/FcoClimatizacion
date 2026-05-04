import re
import random
from django.core.management.base import BaseCommand
from projects.models import Project

HUMAN_TITLES = [
    "Instalación residencial — RM",
    "Instalación comercial — RM",
    "Instalación split mural — RM",
    "Instalación en oficina — RM",
    "Instalación en local — RM",
    "Instalación en departamento — RM",
    "Instalación en casa — RM",
    "Instalación multipunto — RM",
]

DESCRIPTIONS = [
    "Instalación realizada por FCOCLIMATIZACION. Trabajo limpio, pruebas y puesta en marcha.",
    "Montaje y suministro según requerimiento. Instalación profesional con garantía.",
    "Instalación con terminaciones prolijas y validación de funcionamiento.",
]

class Command(BaseCommand):
    help = "Renombra proyectos tipo 'Instalación 1' a títulos más humanos y agrega descripción base."

    def add_arguments(self, parser):
        parser.add_argument("--prefix", type=str, default="Instalación", help="Prefijo a buscar (default Instalación)")
        parser.add_argument("--set_featured", action="store_true", help="Marca como destacados los proyectos renombrados")

    def handle(self, *args, **opts):
        prefix = opts["prefix"]
        set_featured = opts["set_featured"]

        qs = Project.objects.filter(title__startswith=prefix).order_by("id")
        count = qs.count()
        if count == 0:
            self.stdout.write("No encontré proyectos con ese prefijo.")
            return

        for idx, p in enumerate(qs, start=1):
            base = random.choice(HUMAN_TITLES)
            p.title = f"{base} ({idx:02d})"
            if not p.description:
                p.description = random.choice(DESCRIPTIONS)
            if set_featured:
                p.featured = True
            p.save()

        self.stdout.write(self.style.SUCCESS(f"OK ✅ Renombrados {count} proyectos."))