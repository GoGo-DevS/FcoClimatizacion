"""Importa las fotos de trabajos desde los ZIP del cliente.

QUE CAMBIO Y POR QUE (16-09-2026)
---------------------------------
La version anterior INVENTABA los datos de cada trabajo:

    region = random.choice(REGIONS)          # "Antofagasta", "Biobio"...
    kind   = random.choice(INSTALLATION_KINDS)

Asi, el sitio publicaba "Mantencion limpieza - Coquimbo (07)" sobre una foto
que pudo ser en Nunoa, y `fill_metadata` le agregaba comuna, marca y BTU
tambien al azar. Es publicar datos falsos en el sitio de un cliente: si alguien
pregunta por ese trabajo de Antofagasta, no existe.

Ahora el titulo es DETERMINISTA y solo dice lo que de verdad sabemos: si la foto
viene de `instalaciones.zip` es una instalacion, y si viene de
`mantenciones.zip` es una mantencion. La comuna, la marca y los BTU quedan
VACIOS hasta que el cliente los complete desde el panel.

Tampoco se publica cualquier imagen: se descartan las capturas de pantalla (ver
`es_captura_de_pantalla`), porque las fotos venian mezcladas con pantallazos de
Instagram y de la galeria del telefono.
"""
import math
import zipfile
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image

from projects.models import Project, ProjectImage

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

# Una foto de telefono es 3:4 o 9:16 (1.78). Una CAPTURA de la pantalla completa
# de un telefono moderno es mas larga (720x1600 = 2.22), porque incluye la barra
# de estado y la de navegacion. Con este corte se van los pantallazos de
# Instagram sin tocar las fotos verticales normales.
RATIO_CAPTURA = 1.95

FAMILIAS = {
    "instalacion": "Instalación de aire acondicionado",
    "mantencion": "Mantención de aire acondicionado",
    "cliente": "Trabajo realizado",
}


def es_captura_de_pantalla(datos: bytes) -> bool:
    """True si la imagen parece un pantallazo y no una foto del trabajo."""
    try:
        with Image.open(BytesIO(datos)) as img:
            ancho, alto = img.size
    except Exception:
        return False
    if not ancho or not alto:
        return False
    largo, corto = max(ancho, alto), min(ancho, alto)
    return (largo / corto) >= RATIO_CAPTURA


def _collect_images(zip_path: Path):
    """Los nombres de las fotos publicables, en orden estable."""
    names = []
    descartadas = 0
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        for name in sorted(zip_file.namelist()):
            if Path(name).suffix.lower() not in ALLOWED_EXTS:
                continue
            if es_captura_de_pantalla(zip_file.read(name)):
                descartadas += 1
                continue
            names.append(name)
    return names, descartadas


def _build_chunks(total_images: int, per_project: int, base_projects: int):
    if total_images <= 0:
        return []

    baseline_capacity = per_project * base_projects
    baseline_images = min(total_images, baseline_capacity)
    baseline_count = min(base_projects, math.ceil(baseline_images / per_project))

    chunks = []
    for idx in range(baseline_count):
        start = idx * per_project
        end = min(start + per_project, total_images)
        chunks.append((start, end))

    if total_images > baseline_capacity:
        chunks.append((baseline_capacity, total_images))

    return chunks


def _build_title(family: str, index: int):
    """Determinista y sin inventar nada: la familia y el número."""
    return f'{FAMILIAS.get(family, FAMILIAS["cliente"])} ({index:02d})'


def _family_prefix(family: str):
    return FAMILIAS.get(family, FAMILIAS["cliente"])


def import_segmented_zip(*, zip_path: Path, family: str, per_project: int, base_projects: int, clear_existing: bool):
    zip_path = zip_path.resolve()
    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP no encontrado: {zip_path}")

    image_names, descartadas = _collect_images(zip_path)
    if not image_names:
        return {
            "created": 0,
            "total_images": 0,
            "removed_projects": 0,
            "descartadas": descartadas,
            "chunks": [],
        }

    prefix = _family_prefix(family)
    removed_projects = 0
    if clear_existing:
        # Tambien se borran los titulos VIEJOS ("Instalacion split mural - RM
        # (03)"). Sin esto, al cambiar el formato del titulo los trabajos
        # antiguos -- los que traen la region inventada -- se quedan publicados
        # para siempre al lado de los nuevos.
        legacy = {"instalacion": "Instalacion ", "mantencion": "Mantencion ",
                  "cliente": "Trabajo realizado"}[family if family in FAMILIAS else "cliente"]
        previous = Project.objects.filter(title__startswith=prefix)
        previous |= Project.objects.filter(title__startswith=legacy)
        removed_projects = previous.count()
        previous.delete()

    chunks = _build_chunks(len(image_names), per_project, base_projects)
    created = 0

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        for idx, (start, end) in enumerate(chunks, start=1):
            project = Project.objects.create(
                title=_build_title(family, idx),
                featured=True,
                # Sin descripcion inventada: la escribe el cliente en el panel.
                description="",
                region="",
                comuna="",
                project_type="local" if family == "mantencion" else "casa",
            )
            for order, name in enumerate(image_names[start:end]):
                data = zip_file.read(name)
                filename = f"{project.id}_{order}_{Path(name).name}"
                image_file = ContentFile(data, name=filename)
                project_image = ProjectImage(
                    project=project,
                    order=order,
                    # El alt describe lo que hay en la foto sin inventar lugar.
                    alt=f"{prefix} realizada por FCO Climatización",
                )
                project_image.image.save(filename, image_file, save=True)

            created += 1

    return {
        "created": created,
        "total_images": len(image_names),
        "removed_projects": removed_projects,
        "descartadas": descartadas,
        "chunks": chunks,
    }
