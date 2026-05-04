import zipfile
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from projects.models import Project, ProjectImage


ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


class Command(BaseCommand):
    help = "Divide un ZIP en múltiples proyectos automáticamente."

    def add_arguments(self, parser):
        parser.add_argument("--zip", type=str, required=True)
        parser.add_argument("--base_title", type=str, required=True)
        parser.add_argument("--per_project", type=int, default=7)
        parser.add_argument("--featured", action="store_true")

    def handle(self, *args, **opts):
        zip_path = Path(opts["zip"]).resolve()
        if not zip_path.exists():
            self.stderr.write("ZIP no encontrado")
            return

        per_project = opts["per_project"]
        base_title = opts["base_title"]
        featured = opts["featured"]

        with zipfile.ZipFile(zip_path, "r") as z:
            images = [
                name for name in z.namelist()
                if Path(name).suffix.lower() in ALLOWED_EXTS
            ]

            images.sort()

            total = len(images)
            if total == 0:
                self.stderr.write("No se encontraron imágenes")
                return

            project_count = 0

            for i in range(0, total, per_project):
                chunk = images[i:i + per_project]
                project_count += 1

                project = Project.objects.create(
                    title=f"{base_title} {project_count}",
                    description="Instalación realizada por FCOCLIMATIZACION.",
                    featured=featured,
                    project_type="local",
                    region="RM",
                )

                for order, name in enumerate(chunk):
                    data = z.read(name)
                    filename = f"{project.id}_{order}_{Path(name).name}"
                    image_file = ContentFile(data, name=filename)

                    pi = ProjectImage(
                        project=project,
                        order=order
                    )
                    pi.image.save(filename, image_file, save=True)

                self.stdout.write(f"Creado: {project.title} ({len(chunk)} fotos)")

        self.stdout.write(self.style.SUCCESS("Importación completada."))