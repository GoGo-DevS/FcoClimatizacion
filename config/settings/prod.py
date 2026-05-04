from .base import *
from django.core.exceptions import ImproperlyConfigured

DEBUG = False

if SECRET_KEY == "dev-only-change-me":
    raise ImproperlyConfigured("DJANGO_SECRET_KEY or SECRET_KEY must be set in production.")

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
X_FRAME_OPTIONS = "DENY"

MEDIA_URL = "/static/media/"
if (BASE_DIR / "media").exists():
    STATICFILES_DIRS = [BASE_DIR / "static", ("media", BASE_DIR / "media")]
