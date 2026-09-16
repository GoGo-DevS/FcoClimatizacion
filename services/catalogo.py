"""Los cuatro servicios, con su página propia.

POR QUE EXISTE ESTO
-------------------
El sitio era UNA sola página con 431 palabras. Quien busca "mantención de aire
acondicionado en Santiago" no encuentra una página que hable de eso: encuentra
una home que menciona cuatro servicios en cuatro tarjetas de dos líneas. Una
página por servicio es lo que permite responder esa búsqueda, y de paso es lo
que el visitante quiere leer antes de escribir por WhatsApp.

REGLA DEL CONTENIDO: todo lo que se afirma acá es lo que HACE el servicio, no
promesas sobre la empresa. No hay años de experiencia, ni cantidad de clientes,
ni plazos, ni precios: nada de eso lo confirmó el cliente, y un dato inventado
en un sitio comercial termina en un reclamo. Lo que el sitio ya decía —factura,
garantía, cobertura en la Región Metropolitana y comunas cercanas— se conserva.

El contenido vive en código, igual que el resto del sitio: no hay panel que
mantener y desplegar no pone nada en riesgo.
"""

SERVICIOS = [
    {
        "slug": "instalacion-aire-acondicionado",
        "nombre": "Instalación de aire acondicionado",
        "titulo_seo": "Instalación de aire acondicionado en Santiago | FCO Climatización",
        "meta": (
            "Instalación de aire acondicionado split en casas, oficinas y locales "
            "de la Región Metropolitana. Canalización, prueba de funcionamiento, "
            "factura y garantía. Cotiza por WhatsApp."
        ),
        "encabezado": "Instalación de aire acondicionado",
        "bajada": (
            "Instalamos equipos split en casas, departamentos, oficinas y locales. "
            "Dejamos el equipo funcionando y probado, no solo colgado en la pared."
        ),
        "incluye": [
            "Visita para definir dónde va cada unidad y por dónde pasa la cañería",
            "Montaje de la unidad interior y de la unidad exterior",
            "Canalización, vacío del circuito y conexión eléctrica del equipo",
            "Prueba de funcionamiento en frío y en calor antes de retirarnos",
            "Recomendaciones de uso y cuidado del equipo",
            "Factura y garantía del trabajo",
        ],
        "para_quien": [
            "Casas y departamentos que quieren climatizar uno o varios ambientes",
            "Oficinas y locales comerciales",
            "Equipos recién comprados que llegaron sin instalación",
        ],
        "preguntas": [
            ("¿Qué incluye una instalación estándar?",
             "Montaje de la unidad interior y exterior, conexión, canalización, vacío "
             "del circuito, prueba de funcionamiento y recomendaciones de uso."),
            ("¿Necesito comprar yo el equipo?",
             "Puedes comprarlo por tu cuenta y nosotros lo instalamos, o pedirnos el "
             "equipo y la instalación juntos."),
            ("¿Cuánta capacidad necesito?",
             "Depende de los metros cuadrados del ambiente, la altura, la orientación y "
             "la aislación. En la portada hay una calculadora que da una referencia "
             "inicial, y el cálculo exacto lo hacemos en la visita técnica."),
            ("¿Hacen la instalación en altura o en fachada?",
             "Sí, siempre que existan las condiciones de seguridad para trabajar. Se "
             "revisa en la visita antes de cotizar."),
        ],
        "relacionados": ["mantencion-aire-acondicionado", "venta-equipos-climatizacion"],
    },
    {
        "slug": "mantencion-aire-acondicionado",
        "nombre": "Mantención de aire acondicionado",
        "titulo_seo": "Mantención de aire acondicionado | Limpieza de split | FCO Climatización",
        "meta": (
            "Mantención y limpieza de aire acondicionado split: filtros, unidad "
            "interior y exterior, y prueba de funcionamiento. Región Metropolitana "
            "y comunas cercanas."
        ),
        "encabezado": "Mantención y limpieza de aire acondicionado",
        "bajada": (
            "Un equipo sin mantención enfría menos, gasta más y termina fallando "
            "justo cuando más lo necesitas. La mantención es lo que lo evita."
        ),
        "incluye": [
            "Limpieza de filtros de la unidad interior",
            "Limpieza de la unidad interior con protección del muro y el piso",
            "Revisión y limpieza de la unidad exterior",
            "Revisión de drenaje, para que no gotee",
            "Medición de temperatura y prueba de funcionamiento",
            "Informe de lo que se revisó, con factura y garantía del trabajo",
        ],
        "para_quien": [
            "Equipos que enfrían menos que antes o botan agua",
            "Casas, oficinas y locales que quieren dejar el equipo listo para el verano",
            "Empresas que necesitan mantención periódica con respaldo formal",
        ],
        "preguntas": [
            ("¿Cada cuánto conviene hacer la mantención?",
             "Lo habitual es una vez al año, y dos veces al año si el equipo se usa "
             "todo el día o está en un lugar con mucho polvo."),
            ("¿Mi equipo bota agua, eso se arregla en la mantención?",
             "Muchas veces sí: el goteo suele ser drenaje tapado o filtros sucios. Si "
             "resulta ser otra cosa, te lo decimos en el momento."),
            ("¿Cuánto se demora?",
             "Depende del estado del equipo y de cuántos haya. Al cotizar te damos una "
             "estimación para que organices tu día."),
            ("¿Atienden empresas con varios equipos?",
             "Sí. Coordinamos la visita y entregamos el servicio con factura."),
        ],
        "relacionados": ["reparacion-aire-acondicionado", "instalacion-aire-acondicionado"],
    },
    {
        "slug": "reparacion-aire-acondicionado",
        "nombre": "Reparación de aire acondicionado",
        "titulo_seo": "Reparación de aire acondicionado | Diagnóstico | FCO Climatización",
        "meta": (
            "Reparación de aire acondicionado: diagnóstico del equipo, revisión de "
            "gas, drenaje y sistema eléctrico. Región Metropolitana y comunas "
            "cercanas, con factura y garantía."
        ),
        "encabezado": "Reparación y diagnóstico",
        "bajada": (
            "Primero se revisa el equipo y se te dice qué tiene. Recién ahí se "
            "cotiza la reparación, para que sepas qué estás pagando."
        ),
        "incluye": [
            "Diagnóstico del equipo en terreno",
            "Revisión del sistema eléctrico y del control",
            "Revisión de drenaje y de filtros",
            "Revisión de presiones y carga de gas cuando corresponde",
            "Informe de lo encontrado antes de reparar",
            "Factura y garantía del trabajo realizado",
        ],
        "para_quien": [
            "Equipos que no encienden, no enfrían o se apagan solos",
            "Equipos que gotean o hacen ruido",
            "Equipos que muestran un código de error en el control",
        ],
        "preguntas": [
            ("¿Cobran el diagnóstico?",
             "Se cotiza según el caso. Antes de ir te decimos cómo se cobra la visita, "
             "para que no haya sorpresas."),
            ("¿Reparan cualquier marca?",
             "Trabajamos con las marcas habituales del mercado chileno. Cuéntanos qué "
             "equipo tienes y te confirmamos antes de ir."),
            ("¿Cuándo conviene reparar y cuándo cambiar el equipo?",
             "Depende de la falla, de la antigüedad y del costo de la reparación. Con "
             "el diagnóstico en la mano te decimos qué conviene, aunque la respuesta "
             "sea no repararlo."),
        ],
        "relacionados": ["mantencion-aire-acondicionado", "venta-equipos-climatizacion"],
    },
    {
        "slug": "venta-equipos-climatizacion",
        "nombre": "Venta de equipos de climatización",
        "titulo_seo": "Venta de aire acondicionado con instalación | FCO Climatización",
        "meta": (
            "Venta de equipos de aire acondicionado con instalación incluida. Te "
            "ayudamos a elegir la capacidad correcta según el ambiente. Factura y "
            "garantía."
        ),
        "encabezado": "Venta de equipos con instalación",
        "bajada": (
            "Te ayudamos a elegir el equipo que corresponde al ambiente, y lo "
            "dejamos instalado y funcionando."
        ),
        "incluye": [
            "Recomendación de capacidad según el ambiente y el uso",
            "Equipo y instalación cotizados juntos, sin sorpresas después",
            "Instalación completa con prueba de funcionamiento",
            "Factura y garantía",
        ],
        "para_quien": [
            "Quien todavía no compra el equipo y no sabe cuál le sirve",
            "Casas, oficinas y locales que quieren equipo e instalación en un solo trato",
        ],
        "preguntas": [
            ("¿Qué equipo me conviene?",
             "Depende de los metros cuadrados, la altura del techo, la orientación y la "
             "aislación. Usa la calculadora de la portada como referencia y lo "
             "confirmamos contigo."),
            ("¿El precio incluye la instalación?",
             "Se cotiza todo junto: equipo e instalación. Así sabes el total antes de "
             "decidir."),
        ],
        "relacionados": ["instalacion-aire-acondicionado", "mantencion-aire-acondicionado"],
    },
]

_POR_SLUG = {s["slug"]: s for s in SERVICIOS}


def servicio(slug):
    return _POR_SLUG.get(slug)


def relacionados_de(datos):
    return [_POR_SLUG[s] for s in datos.get("relacionados", []) if s in _POR_SLUG]
