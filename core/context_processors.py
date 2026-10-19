import json

from django.conf import settings

from . import seo, zonas


def site_settings(request):
    return {
        "WHATSAPP_PHONE": settings.WHATSAPP_PHONE,
        # La cobertura sale de core/seo.COMUNAS y llega a TODAS las plantillas.
        # Si viviera en la vista de la home, el pie y las paginas de servicio
        # seguirian diciendo "comunas cercanas" y el sitio se contradiria solo.
        "zona": seo.ZONA,
        "zona_corta": seo.ZONA_CORTA,
        "zona_principal": seo.ZONA_PRINCIPAL,
        "comunas": seo.COMUNAS,
        # La pagina del sector principal: el pie, la portada y cada servicio
        # la enlazan, que es como Google sabe que es la pagina importante.
        "url_zona_principal": zonas.ruta(zonas.ZONAS[0]),
        "comunas_enlazadas": zonas.enlazar(seo.COMUNAS),
        "zonas_pie": [(z["h1"], zonas.ruta(z)) for z in zonas.ZONAS],
        "cobertura_nacional": seo.COBERTURA_NACIONAL,
        "WHATSAPP_PHONE_CLEAN": settings.WHATSAPP_PHONE.replace("+", "").replace(" ", ""),
        # El JSON-LD del negocio va en TODAS las paginas: si viviera en cada
        # vista, la primera que se olvide queda sin datos estructurados.
        "schema_negocio": json.dumps(seo.datos_del_negocio(request), ensure_ascii=False),
        # Vacios mientras no esten cargados en Render: el <head> no dibuja ni la
        # etiqueta de verificacion ni el script de Analytics.
        "GA4_MEASUREMENT_ID": settings.GA4_MEASUREMENT_ID,
        "GOOGLE_SITE_VERIFICATION": settings.GOOGLE_SITE_VERIFICATION,
    }
