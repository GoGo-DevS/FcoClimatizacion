from django.shortcuts import render
from projects.models import Project

def home(request):
    featured_projects = (
        Project.objects
        .filter(featured=True)
        .prefetch_related("images")[:4]
    )
    return render(request, "core/home.html", {"featured_projects": featured_projects})