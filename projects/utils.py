import os
import re
from functools import lru_cache

from PIL import Image

SEGMENTED_TITLE_RE = re.compile(
    r"^(Instalacion .+ - [A-Za-z]+ \(\d{2}\)|Mantencion .+ - [A-Za-z]+ \(\d{2}\)|Trabajo realizado - [A-Za-z]+ \(\d{2}\))$"
)


def has_instagram_overlay(image_path: str) -> bool:
    """
    Heuristic:
    - scans the bottom 30%
    - detects common orange stickers or strong saturated blocks
    """
    try:
        img = Image.open(image_path).convert("RGB")
        w, h = img.size
        crop = img.crop((0, int(h * 0.70), w, h)).resize((96, 48))
        pixels = crop.getdata()

        orange = 0
        strong = 0
        total = crop.width * crop.height

        for r, g, b in pixels:
            if r > 180 and g > 70 and b < 100:
                orange += 1

            if max(r, g, b) - min(r, g, b) > 140 and r > 120:
                strong += 1

        orange_ratio = orange / max(total, 1)
        strong_ratio = strong / max(total, 1)
        return orange_ratio > 0.05 or strong_ratio > 0.10
    except Exception:
        return False


def has_face_like_region(image_path: str) -> bool:
    """
    Lightweight skin-tone heuristic to avoid human-face covers.
    This is intentionally conservative and only used for cover selection.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        w, h = img.size
        if w < 40 or h < 40:
            return False

        upper = img.crop((0, 0, w, int(h * 0.75)))
        small = upper.resize((96, 96))

        def skin_ratio(pixels):
            skin = 0
            total = len(pixels)
            for r, g, b in pixels:
                max_c = max(r, g, b)
                min_c = min(r, g, b)

                is_skin = (
                    r > 95 and g > 40 and b > 20 and
                    (max_c - min_c) > 15 and
                    abs(r - g) > 15 and
                    r > g and r > b
                )
                if is_skin:
                    skin += 1
            return skin / max(total, 1)

        overall_ratio = skin_ratio(small.getdata())
        if overall_ratio < 0.18:
            return False

        center = small.crop((small.width // 4, small.height // 8, (small.width * 3) // 4, small.height))
        center_ratio = skin_ratio(center.getdata())
        return center_ratio > 0.20
    except Exception:
        return False


@lru_cache(maxsize=4096)
def _is_unwanted_cover_cached(image_path: str, modified_time: float) -> bool:
    return has_instagram_overlay(image_path) or has_face_like_region(image_path)


def is_unwanted_cover(image_path: str) -> bool:
    try:
        modified_time = os.path.getmtime(image_path)
    except OSError:
        return False

    return _is_unwanted_cover_cached(image_path, modified_time)


def pick_cover_image(project):
    images = list(project.images.all())
    if not images:
        return None

    for image in images:
        if not is_unwanted_cover(image.image.path):
            return image

    return None


def is_segmented_title(title: str) -> bool:
    return bool(SEGMENTED_TITLE_RE.match((title or "").strip()))
