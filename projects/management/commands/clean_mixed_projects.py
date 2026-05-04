from django.core.management.base import BaseCommand
from django.db.models import Q

from projects.models import Project
from projects.utils import is_segmented_title

MIXED_PREFIXES = [
    "Mantencion de aire acondicionado",
    "Mantenciones",
]


class Command(BaseCommand):
    help = "Limpia proyectos mezclados y deja visible solo el portafolio segmentado."

    def add_arguments(self, parser):
        parser.add_argument("--delete", action="store_true", help="Elimina proyectos mezclados (default).")
        parser.add_argument(
            "--soft",
            action="store_true",
            help="No elimina: solo desmarca featured para los no segmentados.",
        )

    def handle(self, *args, **options):
        soft_mode = options["soft"]

        mixed_q = Q()
        for prefix in MIXED_PREFIXES:
            mixed_q |= Q(title__startswith=prefix)

        explicitly_mixed = Project.objects.filter(mixed_q)
        explicitly_mixed_count = explicitly_mixed.count()

        all_projects = list(Project.objects.all())
        segmented_ids = {p.id for p in all_projects if is_segmented_title(p.title)}
        non_segmented = Project.objects.exclude(id__in=segmented_ids)
        non_segmented_count = non_segmented.count()

        deleted = 0
        if soft_mode:
            explicitly_mixed.update(featured=False)
            non_segmented.update(featured=False)
        else:
            deleted += explicitly_mixed_count
            explicitly_mixed.delete()

            rest_non_segmented = Project.objects.exclude(id__in=segmented_ids)
            deleted += rest_non_segmented.count()
            rest_non_segmented.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"OK: mixed_prefix={explicitly_mixed_count} non_segmented={non_segmented_count} deleted={deleted} soft={soft_mode}"
            )
        )
