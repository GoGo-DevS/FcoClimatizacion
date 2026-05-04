from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Project
from .utils import is_segmented_title, pick_cover_image


def _segmented_projects_queryset():
    return (
        Project.objects
        .filter(
            Q(title__startswith="Instalacion ")
            | Q(title__startswith="Mantencion ")
            | Q(title__startswith="Trabajo realizado ")
        )
        .order_by("-created_at")
        .prefetch_related("images")
    )


def projects_list(request):
    projects_qs = _segmented_projects_queryset()
    segmented_projects = [p for p in projects_qs if is_segmented_title(p.title)]
    paginator = Paginator(segmented_projects, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    for project in page_obj:
        project.images_list = list(project.images.all())
        project.has_images = len(project.images_list) > 0
        project.cover_image = pick_cover_image(project)

    return render(
        request,
        "projects/projects_list.html",
        {
            "projects": page_obj,
            "page_obj": page_obj,
        },
    )


def project_detail(request, project_id):
    projects_qs = _segmented_projects_queryset()
    project = get_object_or_404(projects_qs, id=project_id)

    if not is_segmented_title(project.title):
        raise Http404("Proyecto no disponible")

    project.images_list = list(project.images.all())
    project.has_images = len(project.images_list) > 0
    project.cover_image = pick_cover_image(project)

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
        },
    )
