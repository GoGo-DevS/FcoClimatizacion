from django.urls import path
from .views import project_detail, projects_list

app_name = "projects"

urlpatterns = [
    path("trabajos/", projects_list, name="list"),
    path("trabajos/<int:project_id>/", project_detail, name="detail"),
]
