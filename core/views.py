from django.http import HttpResponse
from django.shortcuts import render

from core import seo
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
     "Región Metropolitana y comunas cercanas. Si estás fuera, escríbenos y te "
     "confirmamos antes de agendar."),
    ("¿Emiten factura?",
     "Sí, los trabajos se entregan con factura y con garantía."),
]


def home(request):
    # Solo trabajos del portafolio: los titulos sueltos no se publican.
    publicables = [
        p for p in Project.objects.filter(featured=True).prefetch_related("images")
        if is_segmented_title(p.title)
    ]
    # Se INTERCALAN instalaciones y mantenciones. Tomando los 6 primeros por
    # fecha salian las 6 mantenciones seguidas, y la portada daba a entender que
    # solo hacen mantencion.
    instalaciones = [p for p in publicables if p.title.startswith("Instalación")]
    mantenciones = [p for p in publicables if p.title.startswith("Mantención")]
    destacados = []
    for i in range(3):
        if i < len(instalaciones):
            destacados.append(instalaciones[i])
        if i < len(mantenciones):
            destacados.append(mantenciones[i])
    destacados = (destacados or publicables)[:6]
    return render(request, "core/home.html", {
        "featured_projects": destacados,
        "servicios": catalogo.SERVICIOS,
        "preguntas": PREGUNTAS_HOME,
        "meta_title": "Aire acondicionado en Santiago: instalación y mantención | FCO Climatización",
        "meta_description": seo.DESCRIPCION_CORTA,
        "canonical": f"{seo.DOMINIO}/",
        "schema_extra": [seo.preguntas_schema(PREGUNTAS_HOME)],
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
