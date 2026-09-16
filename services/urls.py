from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("servicios/", views.servicios_index, name="index"),
    path("servicios/<slug:slug>/", views.servicio_detalle, name="detail"),
]
