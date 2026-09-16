from .base import *
import os

DEBUG = True

# "testserver" es el host que usa el cliente de pruebas de Django: sin el,
# cada prueba que pide una URL responde 400 y parece un error de la vista.
_DEV_DEFAULT_ALLOWED_HOSTS = ["127.0.0.1", "localhost", "192.168.1.4", "testserver"]
_ENV_ALLOWED_HOSTS = [host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if host.strip()]
ALLOWED_HOSTS = list(dict.fromkeys(_DEV_DEFAULT_ALLOWED_HOSTS + _ENV_ALLOWED_HOSTS))

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# En desarrollo y en las pruebas no hay manifiesto de estaticos (no se corre
# collectstatic), y con el backend de produccion cualquier {% static %} revienta
# con "Missing staticfiles manifest entry".
STORAGES = {
    **STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
