import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


TEXT_EXTENSIONS = {".html", ".css", ".js", ".py"}
SCAN_DIRS = ["templates", "static", "projects", "core", "leads", "config"]

MOJIBAKE_RE = re.compile(r"(?:\u00C3[\u0080-\u00BF]|\u00C2[\u0080-\u00BF]|\u00E2[\u0080-\u00BF]{2})")


class Command(BaseCommand):
    help = "Verifica que archivos de templates/static/codigo sean UTF-8 valido y sin mojibake comun."

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)
        non_utf8 = []
        mojibake = []
        bom_files = []

        for scan_dir in SCAN_DIRS:
            root = base_dir / scan_dir
            if not root.exists():
                continue

            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix.lower() not in TEXT_EXTENSIONS:
                    continue

                raw = path.read_bytes()
                if raw.startswith(b"\xef\xbb\xbf"):
                    bom_files.append(path)

                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError:
                    non_utf8.append(path)
                    continue

                if MOJIBAKE_RE.search(text):
                    mojibake.append(path)

        if non_utf8 or mojibake:
            lines = ["verify_utf8 detecto problemas:"]
            if non_utf8:
                lines.append(" - Archivos no UTF-8:")
                lines.extend([f"   * {p}" for p in non_utf8])
            if mojibake:
                lines.append(" - Archivos con secuencias mojibake:")
                lines.extend([f"   * {p}" for p in mojibake])
            if bom_files:
                lines.append(" - Archivos con BOM (recomendado remover):")
                lines.extend([f"   * {p}" for p in bom_files])
            raise CommandError("\n".join(lines))

        if bom_files:
            self.stdout.write("OK UTF-8 sin mojibake. Nota: hay archivos con BOM:")
            for path in bom_files:
                self.stdout.write(f" - {path}")
            return

        self.stdout.write(self.style.SUCCESS("OK: UTF-8 valido y sin secuencias mojibake."))
