"""Sitemap del sitio. Sin esto, Google descubre las paginas solo por enlaces."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from projects.models import Project
from projects.utils import is_segmented_title
from core import zonas
from services import catalogo


class PaginasFijas(Sitemap):
    priority = 1.0
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return ["home", "services:index", "projects:list"]

    def location(self, item):
        return reverse(item) if ":" in item else reverse(item)


class Servicios(Sitemap):
    priority = 0.9
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return catalogo.SERVICIOS

    def location(self, item):
        return reverse("services:detail", args=[item["slug"]])


class Zonas(Sitemap):
    # Igual que los servicios: es una pagina comercial, la que responde a
    # "aire acondicionado <sector>".
    priority = 0.9
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return zonas.ZONAS

    def location(self, item):
        return zonas.ruta(item)


class Trabajos(Sitemap):
    priority = 0.5
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        # Solo los del portafolio: un trabajo con titulo suelto no deberia estar
        # publicado y menos ofrecido a Google.
        return [p for p in Project.objects.all() if is_segmented_title(p.title)]

    def location(self, item):
        return reverse("projects:detail", args=[item.id])

    def lastmod(self, item):
        return item.created_at


SITEMAPS = {"paginas": PaginasFijas(), "servicios": Servicios(), "zonas": Zonas(), "trabajos": Trabajos()}
