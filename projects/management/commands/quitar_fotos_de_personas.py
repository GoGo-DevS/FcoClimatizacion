"""Borra del portafolio los trabajos que venian de `clientes.zip`.

Esas fotos son testimonios: la CARA de clientes reales, y capturas de pantalla
de Instagram con la interfaz del telefono a la vista. Publicarlas en el sitio
comercial tiene dos problemas, y el segundo es el caro:

  1. no muestran el trabajo (no se ve el equipo, se ve una persona saludando),
  2. son rostros de terceros publicados sin que conste su permiso.

Este comando los saca. Corre en cada despliegue porque la base de produccion ya
los tiene cargados desde febrero.

Si algun dia el cliente quiere publicar testimonios, se hace aparte y con su
permiso por escrito -- no mezclados con el portafolio.
"""
from django.core.management.base import BaseCommand

from projects.models import Project

PREFIJOS = ("Trabajo realizado",)


class Command(BaseCommand):
    help = "Quita del portafolio las fotos de personas (testimonios de clientes.zip)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true",
                            help="Solo dice cuántos borraría.")

    def handle(self, *args, **options):
        qs = Project.objects.none()
        for prefijo in PREFIJOS:
            qs = qs | Project.objects.filter(title__startswith=prefijo)
        total = qs.count()
        imagenes = sum(p.images.count() for p in qs)
        if options["dry_run"]:
            self.stdout.write(f"ENSAYO: se quitarían {total} trabajos ({imagenes} fotos).")
            return
        qs.delete()
        self.stdout.write(self.style.SUCCESS(
            f"OK: {total} trabajos con fotos de personas fuera del portafolio "
            f"({imagenes} fotos)."))
