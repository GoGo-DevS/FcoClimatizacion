from django import template

from projects.utils import is_segmented_title, pick_cover_image

register = template.Library()


@register.filter
def safe_cover(project):
    if project is None:
        return None

    if getattr(project, "_safe_cover_ready", False):
        return getattr(project, "_safe_cover_image", None)

    cover = getattr(project, "cover_image", None)
    if cover is None:
        cover = pick_cover_image(project)

    project._safe_cover_image = cover
    project._safe_cover_ready = True
    return cover


@register.filter
def is_segmented_project(project):
    if project is None:
        return False
    return is_segmented_title(getattr(project, "title", ""))
