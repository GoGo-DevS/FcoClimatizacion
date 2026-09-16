import json

from django.conf import settings

from . import seo


def site_settings(request):
    return {
        "WHATSAPP_PHONE": settings.WHATSAPP_PHONE,
        "WHATSAPP_PHONE_CLEAN": settings.WHATSAPP_PHONE.replace("+", "").replace(" ", ""),
        # El JSON-LD del negocio va en TODAS las paginas: si viviera en cada
        # vista, la primera que se olvide queda sin datos estructurados.
        "schema_negocio": json.dumps(seo.datos_del_negocio(request), ensure_ascii=False),
        # Vacios mientras no esten cargados en Render: el <head> no dibuja ni la
        # etiqueta de verificacion ni el script de Analytics.
        "GA4_MEASUREMENT_ID": settings.GA4_MEASUREMENT_ID,
        "GOOGLE_SITE_VERIFICATION": settings.GOOGLE_SITE_VERIFICATION,
    }
