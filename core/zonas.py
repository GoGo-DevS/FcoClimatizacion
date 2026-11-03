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
    {
        # 19-10-2026: Diego confirmo que Francisco llega a Maipu.
        #
        # 03-11-2026: la pagina nombraba los servicios pero no RESPONDIA las
        # busquedas. El autocompletado de Google (Chile) para "aire
        # acondicionado maipu" sugiere, en este orden: mantencion, instalacion,
        # recarga, reparacion y tecnico ("servicio tecnico aire acondicionado
        # en maipu"). Cada una tiene ahora su bloque con la palabra exacta en el
        # H2 y un enlace a la pagina del servicio. "Recarga" y "reparacion" en
        # Maipu tambien se buscan para autos: el bloque lo aclara.
        # Nada inventado: ni trabajos en Maipu, ni precios, ni plazos.
        "slug": "maipu",
        "nombre": "Maipú",
        "comuna": "Maipú",
        "es_comuna": True,
        # Mantencion e instalacion son las dos primeras sugerencias; tecnico va
        # en el H1 y reparacion y recarga en la meta.
        "titulo_seo": "Mantención e instalación de aire acondicionado en Maipú",
        "meta": (
            "Técnico de aire acondicionado en Maipú: mantención antes del verano, "
            "instalación de split, reparación con diagnóstico y recarga de gas. "
            "Con factura."
        ),
        "h1": "Técnico de aire acondicionado en Maipú",
        "bajada": (
            "Mantención, instalación, reparación y recarga de gas de equipos split "
            "en Maipú, para casas, departamentos, oficinas y locales."
        ),
        "intro": [
            "Atendemos Maipú desde nuestra base en Ciudad de los Valles, en la comuna "
            "vecina de Pudahuel. Coordinamos la visita por WhatsApp y llegamos con lo "
            "necesario para el trabajo que se conversó.",
            "Hacemos instalaciones nuevas, mantención de equipos que ya tienes y "
            "reparación con diagnóstico previo. Todo se entrega probado, con factura "
            "y con garantía.",
        ],
        # Un bloque por intencion de busqueda, en el orden del autocompletado.
        # `slug` es el servicio que responde a fondo: el bloque lo enlaza.
        "servicios_zona": [
            {
                "slug": "mantencion-aire-acondicionado",
                "titulo": "Mantención de aire acondicionado en Maipú",
                "parrafos": [
                    "Antes del verano conviene dejar el equipo limpio y probado. Uno "
                    "que pasó meses apagado junta polvo en los filtros y en la unidad "
                    "exterior, y enfría menos justo cuando más se necesita.",
                    "La mantención incluye la limpieza de los filtros y de las dos "
                    "unidades, la revisión del drenaje y una prueba de funcionamiento, "
                    "con un informe de lo revisado. Para coordinarla, cuéntanos cuántos "
                    "equipos son y dónde está cada unidad exterior: en el patio, el "
                    "techo, la logia o la fachada.",
                ],
                "enlaces": [
                    ("Qué incluye la mantención y limpieza",
                     "/servicios/mantencion-aire-acondicionado/"),
                ],
            },
            {
                "slug": "instalacion-aire-acondicionado",
                "titulo": "Instalación de aire acondicionado en Maipú",
                "parrafos": [
                    "En Maipú hay casas en villas y condominios, y cada vez más "
                    "edificios. Si es casa, lo que más pesa es el recorrido de la "
                    "cañería hasta la unidad exterior; si es departamento, lo primero "
                    "es lo que permite el edificio. Antes de la visita a un "
                    "departamento conviene tener claro esto:",
                ],
                "puntos": [
                    "Si el edificio permite unidades exteriores en el balcón, la logia "
                    "o la fachada: lo define el reglamento de copropiedad, y conviene "
                    "preguntarlo a la administración",
                    "Por dónde puede pasar la cañería sin romper más de lo necesario",
                    "Hacia dónde va el agua del drenaje, para que no caiga al balcón "
                    "de abajo",
                    "Si el enchufe o el circuito eléctrico aguantan el equipo",
                ],
                "cierre": (
                    "Si todavía no tienes el equipo, la capacidad depende de los metros "
                    "cuadrados de la pieza: con la tabla de BTU la calculas, y te "
                    "cotizamos el equipo junto con la instalación."
                ),
                "enlaces": [
                    ("Qué incluye la instalación", "/servicios/instalacion-aire-acondicionado/"),
                    ("Cuántos BTU necesitas", "/cuantos-btu-necesito/"),
                    ("Equipo e instalación juntos", "/servicios/venta-equipos-climatizacion/"),
                ],
            },
            {
                "slug": "reparacion-aire-acondicionado",
                "titulo": "Servicio técnico y reparación de aire acondicionado en Maipú",
                "parrafos": [
                    "Un equipo que dejó de enfriar no siempre está perdido. Muchas "
                    "veces es un filtro tapado, el drenaje o una falla eléctrica que "
                    "se arregla en la visita. Otras veces la reparación cuesta casi "
                    "lo mismo que un equipo nuevo.",
                    "Por eso primero se hace el diagnóstico y se te dice qué tiene el "
                    "equipo. Con eso en la mano decides tú, y te decimos qué conviene "
                    "aunque la respuesta sea no repararlo.",
                    "Al escribirnos, cuéntanos la marca del equipo y qué hace: no "
                    "enciende, no enfría, gotea, hace ruido o muestra un código en la "
                    "pantalla.",
                ],
                "enlaces": [
                    ("Cómo trabajamos una reparación", "/servicios/reparacion-aire-acondicionado/"),
                ],
            },
            {
                "slug": "reparacion-aire-acondicionado",
                "titulo": "Recarga de gas de aire acondicionado en Maipú",
                "parrafos": [
                    "Un split trabaja con el gas en un circuito cerrado y no lo consume "
                    "al funcionar. Si al equipo le falta gas, hay una fuga en alguna "
                    "parte, y cargarlo sin encontrarla es pagar por un gas que se va a "
                    "volver a escapar.",
                    "Por eso la recarga va después del diagnóstico: se busca la fuga, "
                    "se repara y recién ahí se carga el equipo.",
                    "Hablamos de equipos split de casas, departamentos, oficinas y "
                    "locales. La recarga del aire acondicionado del auto la hace un "
                    "taller automotriz.",
                ],
                "enlaces": [
                    ("Ver la reparación y la carga de gas",
                     "/servicios/reparacion-aire-acondicionado/"),
                ],
            },
        ],
        # Lo que era "secciones" (departamentos, reparar o cambiar) quedo dentro
        # de los bloques de instalacion y servicio tecnico.
        "secciones": [],
        "preguntas": [
            ("¿Atienden en Maipú?",
             "Sí. Atendemos Maipú desde nuestra base en Ciudad de los Valles, "
             "Pudahuel. Escríbenos por WhatsApp y coordinamos la visita."),
            ("¿Tienen servicio técnico de aire acondicionado en Maipú?",
             "Sí. Revisamos el equipo en terreno, te decimos qué tiene y recién ahí "
             "se cotiza la reparación."),
            ("¿Hacen mantención de aire acondicionado en Maipú?",
             "Sí: limpieza de filtros, unidad interior y exterior, revisión del "
             "drenaje y prueba de funcionamiento, con informe de lo revisado."),
            ("¿Instalan aire acondicionado en departamentos de Maipú?",
             "Sí. Antes conviene preguntarle a la administración dónde permite el "
             "reglamento poner la unidad exterior, para planificar la instalación "
             "con eso."),
            ("¿Hacen recarga de gas de aire acondicionado en Maipú?",
             "Sí, en equipos split y después del diagnóstico: si al equipo le falta "
             "gas es porque tiene una fuga, y primero se repara."),
            ("¿Cuánto cuesta instalar un aire acondicionado en Maipú?",
             "Depende del equipo, del largo de la cañería, de dónde va la unidad "
             "exterior y de la conexión eléctrica. Se cotiza después de ver el lugar, "
             "con el detalle antes de hacer el trabajo."),
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


def enlazar(nombres):
    """[(nombre, ruta o None)]: cada comuna con su pagina, si la tiene.

    Las listas de comunas del sitio enlazan solas a la pagina de la comuna en
    cuanto existe. Sin pagina, el nombre va sin enlace: nunca a un 404.
    """
    rutas = {z["nombre"]: ruta(z) for z in ZONAS}
    return [(n, rutas.get(n)) for n in nombres]


def lugar_schema(z):
    """El sector como `Place` dentro de su comuna.

    Ciudad de los Valles no es una comuna, es un sector de Pudahuel: declararlo
    como `City` seria falso. `containedInPlace` es lo que le dice a Google
    donde queda.
    Una zona que ES comuna (Maipu) va como `City`.
    """
    if z.get("es_comuna"):
        return {"@type": "City", "name": z["nombre"],
                "addressRegion": "Región Metropolitana", "addressCountry": "CL"}
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
