from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from core import views as core_views
from core.sitemaps import SITEMAPS

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core_views.home, name="home"),
    path("", include("leads.urls")),
    path("", include("projects.urls")),
    path("", include("services.urls")),
    # SEO: sin sitemap Google descubre las paginas solo por enlaces, y sin
    # robots.txt cada rastreador decide por su cuenta que mirar.
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path("robots.txt", core_views.robots, name="robots"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
