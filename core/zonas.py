"""Una pagina por ZONA: lo que responde a "aire acondicionado <sector>".

POR QUE EXISTE (19-10-2026)
---------------------------
Francisco vive y tiene su base en Ciudad de los Valles, y quiere que quien
busque ahi un tecnico de aire acondicionado lo encuentre a el. Hasta hoy el
sector se nombraba en la portada y en los titulos, pero NINGUNA pagina era
sobre Ciudad de los Valles: la portada habla de los cuatro servicios, y cada
servicio habla de su servicio. Google responde una busqueda local con la
pagina que trata de ese lugar, y esa pagina no existia.

Cada zona es un dato de esta lista, no una plantilla copiada: cuando Francisco
confirme otra comuna (Maipu es la que mas se busca segun el autocompletado),
se agrega aca y la pagina, el sitemap, el pie y las migas salen solos.

REGLA DEL CONTENIDO, la de todo el repo: no se afirma nada que el cliente no
haya dicho. Ni tiempos de llegada, ni precios, ni cantidad de trabajos en el
sector. Lo que se dice del lugar es publico (que es un sector de Pudahuel junto
a la Ruta 68, de casas) y lo que se dice del oficio es general.
"""
from core import seo

ZONAS = [
    {
        "slug": "ciudad-de-los-valles",
        "nombre": "Ciudad de los Valles",
        "comuna": "Pudahuel",
        # 60 caracteres como maximo: Google corta ahi.
        "titulo_seo": "Aire acondicionado en Ciudad de los Valles, Pudahuel | FCO",
        "meta": (
            "Técnico de aire acondicionado en Ciudad de los Valles, Pudahuel: "
            "instalación, mantención y reparación de equipos split. Con factura y "
            "garantía."
        ),
        "h1": "Aire acondicionado en Ciudad de los Valles",
        "bajada": (
            "Instalación, mantención y reparación de equipos split en Ciudad de los "
            "Valles, Pudahuel. Nuestra base está acá, en el mismo sector."
        ),
        "intro": [
            "FCO Climatización trabaja desde Ciudad de los Valles. Para quien vive "
            "en el sector, eso significa coordinar la visita con un técnico que ya "
            "conoce las casas y los condominios de la zona, sin pedirle a alguien "
            "que cruce Santiago.",
            "Instalamos equipos nuevos, hacemos la mantención de los que ya tienes y "
            "revisamos los que dejaron de enfriar. Todos los trabajos se entregan "
            "probados, con factura y con garantía.",
        ],
        "secciones": [
            {
                "titulo": "Instalar un split en una casa de Ciudad de los Valles",
                "parrafos": [
                    "En una casa lo que más define la instalación es dónde va la "
                    "unidad exterior y por dónde pasa la cañería. Antes de cotizar "
                    "se revisan estos puntos en la visita:",
                ],
                "puntos": [
                    "Si la unidad exterior va en el patio, en la fachada o en el "
                    "techo, y que quede con ventilación y a mano para la mantención",
                    "El recorrido de la cañería entre las dos unidades, que es lo que "
                    "más mueve el costo de la instalación",
                    "Hacia dónde se va el agua del drenaje",
                    "La conexión eléctrica que va a usar el equipo",
                    "En un condominio, si hay reglas sobre dónde pueden ir las "
                    "unidades exteriores: conviene preguntarlo antes de la visita",
                ],
            },
            {
                "titulo": "Mantención antes del verano",
                "parrafos": [
                    "Los veranos de Santiago pasan los 30 °C, y es justo cuando "
                    "todos los equipos se encienden a la vez que aparecen las "
                    "fallas: filtros tapados, drenajes que gotean, equipos que "
                    "enfrían menos que el año pasado. Una mantención en primavera "
                    "deja el equipo listo antes de que se necesite.",
                    "Lo habitual es una mantención al año, y dos si el equipo se usa "
                    "todo el día o está en un lugar con mucho polvo.",
                ],
            },
        ],
        "preguntas": [
            ("¿Atienden en Ciudad de los Valles?",
             "Sí. Ciudad de los Valles es nuestra base y nuestra zona principal. "
             "Escríbenos por WhatsApp con lo que necesitas y coordinamos la visita."),
            ("¿Qué servicios hacen en Ciudad de los Valles?",
             "Instalación de aire acondicionado, mantención y limpieza, reparación "
             "con diagnóstico previo y venta de equipos con instalación."),
            ("¿Instalan en condominios del sector?",
             "Sí. Antes de la visita conviene revisar si el condominio tiene reglas "
             "sobre dónde pueden ir las unidades exteriores, para planificar la "
             "instalación con eso."),
            ("¿Cuánto cuesta instalar un aire acondicionado en Ciudad de los Valles?",
             "Depende del equipo, del largo de la cañería, de dónde va la unidad "
             "exterior y de la conexión eléctrica. Se cotiza después de ver el lugar, "
             "y la cotización te llega con el detalle antes de hacer el trabajo."),
            ("¿Emiten factura?",
             "Sí, los trabajos se entregan con factura y con garantía."),
        ],
    },
]

_POR_SLUG = {z["slug"]: z for z in ZONAS}


def zona(slug):
    return _POR_SLUG.get(slug)


def ruta(z):
    """La URL de una zona. Fija y con la keyword: nunca `?zona=`."""
    return f"/aire-acondicionado-{z['slug']}/"


def lugar_schema(z):
    """El sector como `Place` dentro de su comuna.

    Ciudad de los Valles no es una comuna, es un sector de Pudahuel: declararlo
    como `City` seria falso. `containedInPlace` es lo que le dice a Google
    donde queda.
    """
    return {
        "@type": "Place",
        "name": z["nombre"],
        "containedInPlace": {"@type": "City", "name": z["comuna"],
                             "addressRegion": "Región Metropolitana",
                             "addressCountry": "CL"},
    }


def zona_schema(z, url):
    """Los servicios ofrecidos EN esa zona."""
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Instalación, mantención y reparación de aire acondicionado",
        "name": z["h1"],
        "description": z["meta"],
        "url": url,
        "provider": {"@type": "HVACBusiness", "name": seo.NOMBRE, "url": seo.DOMINIO},
        "areaServed": lugar_schema(z),
    }
