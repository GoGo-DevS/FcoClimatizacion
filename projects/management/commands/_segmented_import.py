import math
import random
import zipfile
from pathlib import Path

from django.core.files.base import ContentFile

from projects.models import Project, ProjectImage

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

REGIONS = [
    "RM",
    "Valparaiso",
    "Antofagasta",
    "Coquimbo",
    "Biobio",
]

INSTALLATION_KINDS = [
    "residencial",
    "comercial",
    "oficina",
    "split mural",
    "multipunto",
]

MAINTENANCE_KINDS = [
    "preventiva",
    "correctiva",
    "limpieza",
    "filtro",
    "puesta a punto",
]


def _collect_images(zip_path: Path):
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        names = [
            name for name in zip_file.namelist()
            if Path(name).suffix.lower() in ALLOWED_EXTS
        ]
        names.sort()
    return names


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
    region = random.choice(REGIONS)
    if family == "instalacion":
        kind = random.choice(INSTALLATION_KINDS)
        return f"Instalacion {kind} - {region} ({index:02d})"
    if family == "mantencion":
        kind = random.choice(MAINTENANCE_KINDS)
        return f"Mantencion {kind} - {region} ({index:02d})"
    return f"Trabajo realizado - {region} ({index:02d})"


def _family_prefix(family: str):
    if family == "instalacion":
        return "Instalacion "
    if family == "mantencion":
        return "Mantencion "
    return "Trabajo realizado "


def import_segmented_zip(*, zip_path: Path, family: str, per_project: int, base_projects: int, clear_existing: bool):
    zip_path = zip_path.resolve()
    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP no encontrado: {zip_path}")

    image_names = _collect_images(zip_path)
    if not image_names:
        return {
            "created": 0,
            "total_images": 0,
            "removed_projects": 0,
            "chunks": [],
        }

    prefix = _family_prefix(family)
    removed_projects = 0
    if clear_existing:
        previous = Project.objects.filter(title__startswith=prefix)
        removed_projects = previous.count()
        previous.delete()

    chunks = _build_chunks(len(image_names), per_project, base_projects)
    created = 0

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        for idx, (start, end) in enumerate(chunks, start=1):
            project = Project.objects.create(
                title=_build_title(family, idx),
                featured=True,
                description="Pendiente de metadata.",
                region="RM",
                project_type="local",
            )
            for order, name in enumerate(image_names[start:end]):
                data = zip_file.read(name)
                filename = f"{project.id}_{order}_{Path(name).name}"
                image_file = ContentFile(data, name=filename)
                project_image = ProjectImage(project=project, order=order)
                project_image.image.save(filename, image_file, save=True)

            created += 1

    return {
        "created": created,
        "total_images": len(image_names),
        "removed_projects": removed_projects,
        "chunks": chunks,
    }
