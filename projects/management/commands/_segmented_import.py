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
    """True si la imagen parece un pantallazo y no una foto del trabajo.

    Dos señales, porque con una sola se colaban capturas:

    1. LA PROPORCION. Una pantalla completa de telefono es 720x1600 (2.22);
       una foto de camara es 3:4 o 9:16 (1.78).
    2. LAS FRANJAS. Recortada o no, una captura de Instagram casi siempre
       conserva una banda plana arriba (barra de estado) o abajo (barra de
       navegacion): una franja de color casi uniforme, muy oscura o muy clara.
       Una foto real no tiene bandas planas en los bordes.
    """
    try:
        with Image.open(BytesIO(datos)) as img:
            ancho, alto = img.size
            gris = img.convert("L")
            franja_alto = max(2, int(alto * 0.045))
            arriba = gris.crop((0, 0, ancho, franja_alto))
            abajo = gris.crop((0, alto - franja_alto, ancho, alto))
    except Exception:
        return False
    if not ancho or not alto:
        return False

    # La proporcion solo delata a las VERTICALES: una captura de telefono es
    # vertical y alargada. Una foto horizontal muy ancha es una panoramica, y
    # con la regla aplicada a las dos orientaciones se descartaban 5 fotos
    # buenas de salas de clase tomadas en panoramica.
    if alto > ancho and (alto / ancho) >= RATIO_CAPTURA:
        return True

    def franja_negra(franja):
        datos_franja = list(franja.getdata())
        if not datos_franja:
            return False
        media = sum(datos_franja) / len(datos_franja)
        varianza = sum((v - media) ** 2 for v in datos_franja) / len(datos_franja)
        return varianza < 90 and media < 42

    # Se exige NEGRO arriba Y abajo: es la barra de estado y la de navegacion.
    #
    # ⚠️ La primera version tambien aceptaba franjas MUY CLARAS, y eso descarto
    # 5 fotos buenas de salas de clase: el techo blanco arriba y el piso claro
    # abajo pasaban por "franja plana". Con solo lo oscuro, esas 5 vuelven.
    return franja_negra(arriba) and franja_negra(abajo)


def es_collage(datos: bytes) -> bool:
    """True si la imagen es un COLLAGE armado en el teléfono.

    En el material del cliente hay mosaicos de 20 fotitos con separaciones
    blancas. Publicados en el portafolio se ven como un error: en la tarjeta no
    se distingue ninguno de los trabajos.

    La señal es la REJILLA: varias filas completas casi blancas Y varias
    columnas completas casi blancas, separadas entre si. Una pared blanca puede
    dar filas claras, pero no da tambien columnas claras repartidas.
    """
    try:
        with Image.open(BytesIO(datos)) as img:
            gris = img.convert("L").resize((160, 160))
    except Exception:
        return False

    pixeles = gris.load()

    def lineas_claras(es_fila):
        claras = []
        for i in range(160):
            valores = sorted(pixeles[j, i] if es_fila else pixeles[i, j] for j in range(160))
            # Percentil 5 y no el minimo: en el collage las separaciones traen
            # algun pixel oscuro del borde de una foto, y con min() no se
            # detectaba ninguna linea.
            if valores[8] > 225:
                claras.append(i)
        # Se agrupan las contiguas: una franja gruesa es UNA separacion, no diez.
        grupos = 0
        anterior = -5
        for i in claras:
            if i - anterior > 2:
                grupos += 1
            anterior = i
        return grupos

    # Dos separaciones en cada sentido ya son una rejilla de 3x3 fotos. Con
    # tres no se detectaba ninguno de los tres collages reales del material.
    return lineas_claras(True) >= 2 and lineas_claras(False) >= 2


def _collect_images(zip_path: Path):
    """Los nombres de las fotos publicables, en orden estable."""
    names = []
    descartadas = 0
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        for name in sorted(zip_file.namelist()):
            if Path(name).suffix.lower() not in ALLOWED_EXTS:
                continue
            datos = zip_file.read(name)
            if es_captura_de_pantalla(datos) or es_collage(datos):
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

    # LO QUE EL CLIENTE ESCRIBIO NO SE PIERDE EN EL DESPLIEGUE.
    #
    # El build vuelve a importar los ZIP en CADA deploy, porque el disco de
    # Render es efimero y las fotos hay que volver a subirlas. Con eso, todo lo
    # que el cliente completara desde el panel -- la comuna del trabajo, la
    # marca, los BTU, su descripcion -- se borraba en el despliegue siguiente,
    # sin aviso. Es el mismo error que ya costo caro en otro proyecto con un
    # seed que corria en cada build.
    #
    # Se puede rescatar porque el titulo es DETERMINISTA: el trabajo (03) sigue
    # siendo el (03) despues de reimportar.
    guardado = {
        p.title: {
            "comuna": p.comuna, "region": p.region, "brand": p.brand,
            "btu": p.btu, "description": p.description,
            "project_type": p.project_type, "featured": p.featured,
        }
        for p in Project.objects.filter(title__startswith=prefix)
    }

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

    restaurados = 0
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        for idx, (start, end) in enumerate(chunks, start=1):
            titulo = _build_title(family, idx)
            campos = {
                "featured": True,
                # Sin descripcion inventada: la escribe el cliente en el panel.
                "description": "",
                "region": "",
                "comuna": "",
                "project_type": "local" if family == "mantencion" else "casa",
            }
            if titulo in guardado:
                campos.update(guardado[titulo])
                restaurados += 1
            project = Project.objects.create(title=titulo, **campos)
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
        "restaurados": restaurados,
        "chunks": chunks,
    }
