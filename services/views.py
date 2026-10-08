"""Una pagina por servicio: lo que responde a "mantencion de aire acondicionado"."""
from django.http import Http404
from django.shortcuts import render

from core import seo
from projects.ficha import FAMILIA_DE_SERVICIO, ficha, trabajos_de_familia
from projects.utils import pick_cover_image

from . import catalogo

# Una foto REAL del cliente por servicio. Sin stock: las fotos son de sus
# propios trabajos.
IMAGEN_POR_SERVICIO = {
    "instalacion-aire-acondicionado": "tecnico-instalando.webp",
    "mantencion-aire-acondicionado": "mantencion-limpieza.webp",
    "reparacion-aire-acondicionado": "medicion-temperatura.webp",
    "venta-equipos-climatizacion": "unidad-exterior.webp",
}


def servicios_index(request):
    return render(request, "services/services_list.html", {
        "servicios": catalogo.SERVICIOS,
        "meta_title": "Servicios de climatización | FCO Climatización",
        "meta_description": (
            "Instalación, mantención, reparación y venta de aire acondicionado en "
            "Ciudad de los Valles, Pudahuel, Lampa y Maipú. Factura y garantía."),
        "canonical": f"{seo.DOMINIO}/servicios/",
        "schema_extra": [seo.migas_schema([("Inicio", "/"), ("Servicios", "/servicios/")])],
    })


def servicio_detalle(request, slug):
    datos = catalogo.servicio(slug)
    if datos is None:
        raise Http404("Servicio no encontrado")
    url = f"{seo.DOMINIO}/servicios/{slug}/"

    # Los trabajos del portafolio de este servicio. Es el enlace que les
    # faltaba: 7 de 13 fichas estaban "descubiertas, sin indexar", y ninguna
    # pagina importante del sitio las enlazaba fuera del listado paginado.
    familia = FAMILIA_DE_SERVICIO.get(slug)
    trabajos = trabajos_de_familia(familia, limite=8) if familia else []
    for t in trabajos:
        t.cover_image = pick_cover_image(t)
        t.ficha = ficha(t)

    return render(request, "services/service_detail.html", {
        "s": datos,
        "trabajos": trabajos,
        "imagen": IMAGEN_POR_SERVICIO.get(slug, "tecnico-instalando.webp"),
        "relacionados": catalogo.relacionados_de(datos),
        "meta_title": datos["titulo_seo"],
        "meta_description": datos["meta"],
        "canonical": url,
        "schema_extra": [
            seo.servicio_schema(datos["nombre"], datos["meta"], url),
            # El FAQ marcado es EL MISMO que se ve en la pagina: si se marcara
            # una pregunta que no esta visible, Google lo trata como engano.
            seo.preguntas_schema(datos["preguntas"]),
            seo.migas_schema([("Inicio", "/"), ("Servicios", "/servicios/"),
                              (datos["nombre"], f"/servicios/{slug}/")]),
        ],
    })
