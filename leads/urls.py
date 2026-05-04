from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path("cotizar/", views.quote_request, name="quote"),
    path("cotizar/exito/", views.quote_success, name="quote_success"),
]
