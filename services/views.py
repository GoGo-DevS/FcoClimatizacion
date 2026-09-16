"""Una pagina por servicio: lo que responde a "mantencion de aire acondicionado"."""
from django.http import Http404
from django.shortcuts import render

from core import seo

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
            "la Región Metropolitana y comunas cercanas. Factura y garantía."),
        "canonical": f"{seo.DOMINIO}/servicios/",
        "schema_extra": [seo.migas_schema([("Inicio", "/"), ("Servicios", "/servicios/")])],
    })


def servicio_detalle(request, slug):
    datos = catalogo.servicio(slug)
    if datos is None:
        raise Http404("Servicio no encontrado")
    url = f"{seo.DOMINIO}/servicios/{slug}/"
    return render(request, "services/service_detail.html", {
        "s": datos,
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
