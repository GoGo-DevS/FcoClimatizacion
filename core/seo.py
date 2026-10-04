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
    "Instalación, mantención y reparación de aire acondicionado en Ciudad de los "
    "Valles, Pudahuel, Lampa, Quilicura y alrededores. Con factura y garantía."
)

# LAS COMUNAS, que es lo que de verdad busca la gente.
#
# Antes esto decia "Region Metropolitana y comunas cercanas": con eso el sitio
# compite contra toda la region y no gana ninguna comuna. Quien tiene el equipo
# malo no busca "aire acondicionado Region Metropolitana", busca "aire
# acondicionado Ciudad de los Valles" o "... Pudahuel", y quiere saber antes de
# escribir si el tecnico llega hasta su casa.
#
# CIUDAD DE LOS VALLES es el sector que Francisco pidio expresamente (es parte
# de Pudahuel). El resto son las comunas que lo rodean, todas a menos de media
# hora. ESTA LISTA LA CONFIRMA FRANCISCO: publicar una comuna a la que no llega
# le trae pedidos que tiene que rechazar, que es peor que no aparecer.
ZONA_PRINCIPAL = "Ciudad de los Valles"
COMUNAS = [
    "Pudahuel",        # incluye Ciudad de los Valles
    "Lampa",
    "Quilicura",
    "Renca",
    "Cerro Navia",
    "Maipú",
    "Colina",
    "Estación Central",
]

# El texto corrido se arma de la lista: no hay dos lugares que puedan decir
# cosas distintas.
# Ciudad de los Valles se nombra aparte de Pudahuel aunque sea parte de ella,
# porque es asi como la busca su gente.
_LUGARES = [ZONA_PRINCIPAL] + COMUNAS
ZONA = ", ".join(_LUGARES[:-1]) + " y " + _LUGARES[-1]
ZONA_CORTA = f"{ZONA_PRINCIPAL}, {COMUNAS[0]} y alrededores"


def whatsapp_url(texto="Hola, quiero cotizar aire acondicionado."):
    from urllib.parse import quote
    numero = settings.WHATSAPP_PHONE.replace("+", "").replace(" ", "")
    return f"https://wa.me/{numero}?text={quote(texto)}"


def area_servida():
    """Las comunas como lista de `City`.

    Un solo `AdministrativeArea` que dice "Region Metropolitana y comunas
    cercanas" no le sirve a Google para nada: no puede cruzarlo con la comuna
    de quien busca. Una lista de ciudades con nombre si.
    """
    return [{"@type": "City", "name": c, "addressRegion": "Región Metropolitana",
             "addressCountry": "CL"} for c in COMUNAS]


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
        "areaServed": area_servida(),
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
        "areaServed": area_servida(),
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
