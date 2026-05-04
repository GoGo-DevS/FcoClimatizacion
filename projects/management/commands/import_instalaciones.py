from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ._segmented_import import import_segmented_zip


class Command(BaseCommand):
    help = "Importa instalaciones.zip segmentado en 8x7 (+1 con resto)."

    def add_arguments(self, parser):
        parser.add_argument("--zip", default="instalaciones.zip")
        parser.add_argument("--keep-existing", action="store_true")

    def handle(self, *args, **options):
        zip_path = Path(settings.BASE_DIR) / options["zip"]
        try:
            result = import_segmented_zip(
                zip_path=zip_path,
                family="instalacion",
                per_project=7,
                base_projects=8,
                clear_existing=not options["keep_existing"],
            )
        except FileNotFoundError as exc:
            raise CommandError(str(exc))

        self.stdout.write(
            self.style.SUCCESS(
                f"OK: instalaciones importadas. proyectos={result['created']} "
                f"imagenes={result['total_images']} removidos={result['removed_projects']}"
            )
        )
