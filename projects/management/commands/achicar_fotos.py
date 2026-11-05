"""Achica las fotos del portafolio antes del collectstatic.

04-11-2026: las fotos salen de instalaciones.zip y mantenciones.zip tal como
llegaron por WhatsApp. La auditoria SEO encontro 45 fotos de mas de 150 KB en
19 paginas; /trabajos/3/ pesaba 1,9 MB. Google mide la velocidad en celular y
una ficha que tarda en cargar se va para abajo.

Se achica EN SU LUGAR, con el mismo nombre y la misma extension: la ruta que
guarda la base no cambia, asi que no hay migracion de datos ni enlace roto.
Los originales siguen enteros dentro de los zips del repo (regla 12: nada en
una sola copia).

Es idempotente: una foto que ya pesa menos del tope no se toca, asi que corre
en cada deploy sin volver a comprimir lo comprimido.
"""
import io
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image, ImageOps

TOPE_BYTES = 150 * 1024
LADO_MAXIMO = 1600
# Si con la calidad no alcanza, se baja el lado: una ficha se ve a 800-1000 px.
LADOS = (LADO_MAXIMO, 1280, 1024)
CALIDADES = (82, 76, 70, 64)
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp"}


def achicar(ruta: Path) -> tuple[int, int] | None:
    """(antes, despues) en bytes si la foto se achico; None si no hacia falta."""
    antes = ruta.stat().st_size
    if antes <= TOPE_BYTES:
        return None
    with Image.open(ruta) as original:
        original = ImageOps.exif_transpose(original)
        formato = {".png": "PNG", ".webp": "WEBP"}.get(ruta.suffix.lower(), "JPEG")
        if formato == "JPEG" and original.mode != "RGB":
            original = original.convert("RGB")
        mejor = None
        for lado in LADOS:
            img = original.copy()
            img.thumbnail((lado, lado))
            for calidad in CALIDADES:
                buf = io.BytesIO()
                opciones = {"optimize": True}
                if formato != "PNG":
                    opciones["quality"] = calidad
                if formato == "JPEG":
                    opciones["progressive"] = True
                img.save(buf, formato, **opciones)
                mejor = buf.getvalue()
                if len(mejor) <= TOPE_BYTES or formato == "PNG":
                    break
            if len(mejor) <= TOPE_BYTES or formato == "PNG":
                break
    if len(mejor) >= antes:
        return None
    ruta.write_bytes(mejor)
    return antes, len(mejor)


class Command(BaseCommand):
    help = "Achica en su lugar las fotos de media/ que pesan mas de 150 KB."

    def handle(self, *args, **options):
        raiz = Path(settings.MEDIA_ROOT)
        if not raiz.exists():
            self.stdout.write("Sin carpeta media: nada que achicar.")
            return
        n, total_antes, total_despues = 0, 0, 0
        for ruta in sorted(raiz.rglob("*")):
            if ruta.suffix.lower() not in EXTENSIONES or not ruta.is_file():
                continue
            try:
                resultado = achicar(ruta)
            except Exception as exc:  # una foto rota no puede tumbar el deploy
                self.stderr.write(f"No se pudo achicar {ruta.name}: {exc}")
                continue
            if resultado:
                n += 1
                total_antes += resultado[0]
                total_despues += resultado[1]
        self.stdout.write(
            f"Fotos achicadas: {n} ({total_antes // 1024} KB -> {total_despues // 1024} KB)")
