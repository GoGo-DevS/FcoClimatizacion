from django.http import Http404, HttpResponse
from django.shortcuts import render

from core import btu, seo, zonas
from projects.models import Project
from projects.utils import is_segmented_title
from services import catalogo


PREGUNTAS_HOME = [
    ("¿Qué incluye una instalación estándar?",
     "Montaje de la unidad interior y exterior, conexión, canalización, prueba de "
     "funcionamiento y recomendaciones básicas de uso."),
    ("¿Cada cuánto conviene hacer la mantención?",
     "Una vez al año como mínimo, y dos veces al año si el equipo se usa todo el día "
     "o está en un lugar con mucho polvo."),
    ("¿Hacen diagnóstico antes de cotizar una reparación?",
     "Sí. Primero se revisa el equipo y se te dice qué tiene; recién ahí se cotiza."),
    ("¿En qué zonas atienden?",
     f"Nuestra base está en {seo.ZONA}. {seo.COBERTURA_NACIONAL}"),
    ("¿Emiten factura?",
     "Sí, los trabajos se entregan con factura y con garantía."),
]


def _destacados(limite=6):
    """Los trabajos del portafolio, intercalando instalaciones y mantenciones.

    Tomando los 6 primeros por fecha salian las 6 mantenciones seguidas, y la
    pagina daba a entender que solo hacen mantencion.

    DENTRO de cada grupo manda `Project.orden` (Meta.ordering), que Francisco
    edita desde el panel. Antes mandaba la fecha, asi que la portada abria con
    la foto mas antigua de cada tipo: la sala de clases oscura y una pared
    donde no se ve ningun equipo, mientras el split abierto con los filtros a
    la vista -- la unica que muestra en que consiste una mantencion -- quedaba
    fuera.
    """
    # Solo trabajos del portafolio: los titulos sueltos no se publican.
    publicables = [
        p for p in Project.objects.filter(featured=True).prefetch_related("images")
        if is_segmented_title(p.title)
    ]
    instalaciones = [p for p in publicables if p.title.startswith("Instalación")]
    mantenciones = [p for p in publicables if p.title.startswith("Mantención")]
    destacados = []
    for i in range((limite + 1) // 2):
        if i < len(instalaciones):
            destacados.append(instalaciones[i])
        if i < len(mantenciones):
            destacados.append(mantenciones[i])
    return (destacados or publicables)[:limite]


def home(request):
    destacados = _destacados()
    return render(request, "core/home.html", {
        "featured_projects": destacados,
        "servicios": catalogo.SERVICIOS,
        "preguntas": PREGUNTAS_HOME,
        # Pudahuel y no Ciudad de los Valles: el sector tiene su propia pagina
        # (core/zonas.py), y dos paginas con el mismo titulo compiten entre si.
        "meta_title": "Aire acondicionado en Pudahuel | FCO Climatización",
        "meta_description": seo.DESCRIPCION_CORTA,
        "canonical": f"{seo.DOMINIO}/",
        "schema_extra": [seo.preguntas_schema(PREGUNTAS_HOME)],
        "zonas": [(z, zonas.ruta(z)) for z in zonas.ZONAS],
    })


def zona(request, slug):
    """La pagina de un sector: "aire acondicionado en Ciudad de los Valles"."""
    datos = zonas.zona(slug)
    if datos is None:
        raise Http404("Zona no encontrada")
    ruta = zonas.ruta(datos)
    url = f"{seo.DOMINIO}{ruta}"
    return render(request, "core/zona.html", {
        "z": datos,
        "servicios": catalogo.SERVICIOS,
        # Un bloque por intencion (Maipu desde el 03-11-2026), con el icono de
        # su servicio. Copias: el dict de core/zonas.py no se toca.
        "bloques": [dict(b, icono=catalogo.servicio(b["slug"])["icono"])
                    for b in datos.get("servicios_zona", [])],
        "trabajos": _destacados(),
        # Las demas comunas, para quien esta cerca pero no en el sector.
        "otras_comunas": zonas.enlazar([c for c in seo.COMUNAS if c != datos["comuna"]]),
        "meta_title": datos["titulo_seo"],
        "meta_description": datos["meta"],
        "canonical": url,
        "schema_extra": [
            zonas.zona_schema(datos, url),
            # El FAQ marcado es EL MISMO que se ve en la pagina.
            seo.preguntas_schema(datos["preguntas"]),
            # La miga es el H1 de la pagina a la que lleva.
            seo.migas_schema([("Inicio", "/"), (datos["h1"], ruta)]),
        ],
    })


def cuantos_btu(request):
    """La guia de capacidad: "¿Cuántos BTU necesito?" (core/btu.py)."""
    ruta = "/cuantos-btu-necesito/"
    preguntas = btu.preguntas()
    return render(request, "core/btu.html", {
        "resumen_texto": btu.resumen_texto(),
        "tamanos": btu.TAMANOS,
        "tabla_m2": btu.tabla_por_m2(),
        "tabla_equipo": btu.tabla_por_equipo(),
        "preguntas": preguntas,
        # Lo que sigue despues de saber la capacidad: guia -> servicios.
        "siguientes": [catalogo.servicio("instalacion-aire-acondicionado"),
                       catalogo.servicio("venta-equipos-climatizacion")],
        # Busqueda nacional e informativa: sin comuna en el titulo.
        "meta_title": "¿Cuántos BTU necesito? Tabla por metros cuadrados | FCO",
        "meta_description": btu.meta(),
        "canonical": f"{seo.DOMINIO}{ruta}",
        "schema_extra": [
            # El FAQ marcado es EL MISMO que se ve en la pagina.
            seo.preguntas_schema(preguntas),
            seo.migas_schema([("Inicio", "/"), ("¿Cuántos BTU necesito?", ruta)]),
        ],
    })


def links(request):
    """GoGoDevS Tree: la pagina que va en la biografia de Instagram.

    Quien llega desde la bio viene a elegir UN camino. Por eso va sin menu ni
    pie: le ofrecerian los mismos caminos dos veces.
    """
    return render(request, "core/links.html", {
        "servicios": catalogo.SERVICIOS,
        "zonas_links": [(z, zonas.ruta(z)) for z in zonas.ZONAS],
        "trabajos": _destacados(),
        "meta_title": "FCO Climatización | Aire acondicionado en Ciudad de los Valles",
        "meta_description": (
            "Cotiza por WhatsApp la instalación, mantención o reparación de tu aire "
            "acondicionado. Ciudad de los Valles, Pudahuel y alrededores."),
        "canonical": f"{seo.DOMINIO}/links/",
    })


def robots(request):
    """robots.txt con el sitemap declarado."""
    lineas = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /cotizar/",   # redirige a WhatsApp: no es contenido
        "",
        f"Sitemap: {seo.DOMINIO}/sitemap.xml",
        "",
    ]
    return HttpResponse(chr(10).join(lineas), content_type="text/plain")
