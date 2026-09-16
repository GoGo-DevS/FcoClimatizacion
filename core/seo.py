"""Los datos del negocio y el SEO, en UN solo lugar.

Antes cada plantilla repetia el titulo y el telefono a mano, y no habia meta
description, canonical, Open Graph ni datos estructurados. Un sitio sin eso:

  . se comparte por WhatsApp sin imagen ni texto (solo la URL pelada),
  . Google elige el resumen por su cuenta, tomando cualquier frase de la pagina,
  . no puede salir en el bloque de mapa ni con horario, porque nadie le dijo que
    esto es un negocio local que atiende una zona.

REGLA QUE SE RESPETA ACA: no se afirma nada que el cliente no haya dicho. El
sitio ya declaraba "cobertura en RM y comunas cercanas", "factura y garantia" y
su WhatsApp; eso se conserva. NO se inventan direccion, horario, anios de
experiencia, precios ni cantidad de trabajos, porque son datos que un cliente
puede desmentir y que Google penaliza si no calzan con la realidad.
"""
from django.conf import settings

NOMBRE = "FCO Climatización"
DOMINIO = "https://fcoclimatizacion.cl"
DESCRIPCION_CORTA = (
    "Instalación, mantención y reparación de aire acondicionado en la Región "
    "Metropolitana y comunas cercanas. Trabajos con factura y garantía."
)

# Lo que el sitio ya afirmaba antes de esta tanda. No se agrega nada nuevo.
ZONA = "Región Metropolitana y comunas cercanas"


def whatsapp_url(texto="Hola, quiero cotizar aire acondicionado."):
    from urllib.parse import quote
    numero = settings.WHATSAPP_PHONE.replace("+", "").replace(" ", "")
    return f"https://wa.me/{numero}?text={quote(texto)}"


def datos_del_negocio(request=None):
    """JSON-LD de negocio local. Es lo que permite salir con mapa y teléfono.

    Se usa `HVACBusiness`, que es el tipo exacto para climatización: decirle a
    Google "esto es una empresa de aire acondicionado" y no un genérico.
    """
    telefono = settings.WHATSAPP_PHONE
    return {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "name": NOMBRE,
        "description": DESCRIPCION_CORTA,
        "url": DOMINIO,
        "telephone": telefono,
        "areaServed": {"@type": "AdministrativeArea", "name": ZONA},
        "address": {"@type": "PostalAddress", "addressRegion": "Región Metropolitana",
                    "addressCountry": "CL"},
        "priceRange": "$$",
        "sameAs": ["https://www.instagram.com/fcoclimatizacion/"],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": nombre}}
            for nombre in ("Instalación de aire acondicionado",
                           "Mantención de aire acondicionado",
                           "Reparación de aire acondicionado",
                           "Venta de equipos de climatización")
        ],
    }


def servicio_schema(nombre, descripcion, url):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": nombre,
        "description": descripcion,
        "url": url,
        "provider": {"@type": "HVACBusiness", "name": NOMBRE, "url": DOMINIO},
        "areaServed": {"@type": "AdministrativeArea", "name": ZONA},
    }


def preguntas_schema(preguntas):
    """FAQPage. Solo con preguntas que están EN la página: si el dato no se ve,
    Google lo trata como marcado engañoso."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": p,
             "acceptedAnswer": {"@type": "Answer", "text": r}}
            for p, r in preguntas
        ],
    }


def migas_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": nombre,
             "item": f"{DOMINIO}{ruta}"}
            for i, (nombre, ruta) in enumerate(items, start=1)
        ],
    }
