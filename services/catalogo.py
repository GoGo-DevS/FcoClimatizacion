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

07-10-2026 — TITULOS DE MAS DE 80 CARACTERES. Google corta cerca de los 60, asi
que lo que se veia en el resultado terminaba a media comuna. Ahora cada titulo
cabe en 60 y la zona completa va en el H1, la descripcion, la seccion "Dónde
trabajamos" y la primera pregunta. Instalacion estaba en la posicion 41 siendo
el servicio principal: se le agrego contenido que responde lo que se pregunta
antes de instalar (todo general del oficio, nada inventado sobre la empresa).
"""
from core import seo

SERVICIOS = [
    {
        "slug": "instalacion-aire-acondicionado",
        "icono": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="5" width="18" height="7" rx="1.6"/><path d="M6.5 9h11M8 15.5c0 1.2-1 1.5-1 2.8M12 15.5c0 1.5-1 1.8-1 3.2M16 15.5c0 1.2-1 1.5-1 2.8"/></svg>',
        "nombre": "Instalación de aire acondicionado",
        "titulo_seo": "Instalación de aire acondicionado en Pudahuel | FCO",
        "meta": (
            "Instalación de aire acondicionado split en Ciudad de los Valles, "
            "Pudahuel, Lampa y Maipú. Visita técnica, vacío del circuito, prueba, "
            "factura y garantía."
        ),
        "encabezado": "Instalación de aire acondicionado en Ciudad de los Valles y Pudahuel",
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
            ("¿Cuánto cuesta instalar un aire acondicionado?",
             "Depende del equipo, del largo de la cañería entre las dos unidades, de "
             "dónde va la unidad exterior y de la conexión eléctrica. Por eso se "
             "cotiza después de ver el lugar, y la cotización te llega con el detalle "
             "antes de hacer el trabajo."),
        ],
        "secciones": [
            {
                "titulo": "Lo que se revisa en la visita, antes de instalar",
                "parrafos": [
                    "Una instalación se decide antes de sacar el equipo de la caja. "
                    "En la visita se miran estos puntos, porque son los que después "
                    "definen si el equipo enfría bien y si se puede mantener:",
                ],
                "puntos": [
                    "Dónde va la unidad interior, para que reparta el aire en el "
                    "ambiente sin darte directo",
                    "Dónde va la unidad exterior: con ventilación y en un lugar donde "
                    "se pueda llegar para la mantención",
                    "Por dónde pasa la cañería entre las dos unidades y cuánto mide el "
                    "recorrido",
                    "Hacia dónde se va el agua del drenaje, para que el equipo no gotee "
                    "dentro de la casa",
                    "La conexión eléctrica que va a usar el equipo",
                ],
            },
            {
                "titulo": "Por qué importa el vacío del circuito",
                "parrafos": [
                    "Antes de liberar el gas, el circuito de cañerías se vacía para "
                    "sacarle el aire y la humedad. Si ese paso se salta, el equipo "
                    "enfría menos y el compresor trabaja forzado. Es una de las "
                    "diferencias entre una instalación bien hecha y una que solo deja "
                    "el equipo colgado en la pared.",
                ],
            },
        ],
        "relacionados": ["mantencion-aire-acondicionado", "venta-equipos-climatizacion"],
    },
    {
        "slug": "mantencion-aire-acondicionado",
        "icono": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5c3 3.7 5 6.3 5 8.8a5 5 0 0 1-10 0c0-2.5 2-5.1 5-8.8Z"/><path d="M9.5 12.8a2.6 2.6 0 0 0 2.6 2.6"/></svg>',
        "nombre": "Mantención de aire acondicionado",
        "titulo_seo": "Mantención de aire acondicionado en Pudahuel | FCO",
        "meta": (
            "Mantención y limpieza de aire acondicionado en Ciudad de los Valles y "
            "Pudahuel: filtros, unidad interior y exterior, drenaje y prueba. Con "
            "factura."
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
        "icono": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15.2 3.4a5 5 0 0 0-5.6 7.9l-6 6a1.6 1.6 0 0 0 0 2.3l.8.8a1.6 1.6 0 0 0 2.3 0l6-6a5 5 0 0 0 7.9-5.6l-3 3-2.4-.6-.6-2.4 3-3Z"/></svg>',
        "nombre": "Reparación de aire acondicionado",
        "titulo_seo": "Reparación de aire acondicionado en Pudahuel | FCO",
        "meta": (
            "Reparación de aire acondicionado en Ciudad de los Valles y Pudahuel: "
            "diagnóstico en terreno, gas, drenaje y sistema eléctrico. Factura y "
            "garantía."
        ),
        "encabezado": "Reparación de aire acondicionado en Ciudad de los Valles y Pudahuel",
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
        "secciones": [
            {
                "titulo": "Antes de escribirnos: tres cosas que puedes revisar tú",
                "parrafos": [
                    "Algunas fallas no son del equipo. Vale la pena descartarlas "
                    "antes de agendar una visita:",
                ],
                "puntos": [
                    "Que el control tenga pilas y esté en modo frío o calor, no en "
                    "ventilación",
                    "Que el filtro de la unidad interior no esté tapado de polvo: un "
                    "filtro sucio hace que el equipo enfríe menos",
                    "Que el equipo tenga corriente: revisa el automático del tablero",
                ],
                "cierre": (
                    "Si después de eso sigue igual, escríbenos con la marca del equipo "
                    "y, si aparece, el código de error que muestra la pantalla o el "
                    "control. Con eso llegamos a la visita sabiendo qué buscar."
                ),
            },
        ],
        "relacionados": ["mantencion-aire-acondicionado", "venta-equipos-climatizacion"],
    },
    {
        "slug": "venta-equipos-climatizacion",
        "icono": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3.6 12.6 11 5.2a2 2 0 0 1 1.4-.6l5 .1a2 2 0 0 1 2 2l.1 5a2 2 0 0 1-.6 1.4l-7.4 7.4a2 2 0 0 1-2.8 0l-5.1-5.1a2 2 0 0 1 0-2.8Z"/><circle cx="15.8" cy="8.2" r="1.3"/></svg>',
        "nombre": "Venta de equipos de climatización",
        "titulo_seo": "Venta de aire acondicionado con instalación en Pudahuel",
        "meta": (
            "Venta de aire acondicionado con instalación en Ciudad de los Valles y "
            "Pudahuel. Te ayudamos a elegir la capacidad correcta. Factura y "
            "garantía."
        ),
        "encabezado": "Venta de aire acondicionado con instalación en Ciudad de los Valles y Pudahuel",
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
            ("¿Puedo comprar el equipo por mi cuenta?",
             "Sí. Si ya lo tienes o prefieres comprarlo tú, lo instalamos igual. "
             "Cotizarlo con nosotros sirve para no equivocarte de capacidad."),
        ],
        "secciones": [
            {
                "titulo": "Cómo se elige la capacidad del equipo",
                "parrafos": [
                    "La capacidad se mide en BTU y depende de los metros cuadrados del "
                    "ambiente, la altura del techo, la orientación y la aislación. Un "
                    "equipo chico para el ambiente trabaja siempre al máximo y no "
                    "alcanza a enfriar; uno demasiado grande se prende y se apaga a "
                    "cada rato. Por eso se calcula antes de comprar, no después.",
                    "En la portada hay una calculadora que da una referencia inicial, "
                    "y la capacidad final la confirmamos contigo según el lugar.",
                ],
            },
        ],
        "relacionados": ["instalacion-aire-acondicionado", "mantencion-aire-acondicionado"],
    },
]

# Como se pregunta por la zona en cada servicio.
_ACCION = {
    "instalacion-aire-acondicionado": "¿Instalan aire acondicionado en",
    "mantencion-aire-acondicionado": "¿Hacen mantención de aire acondicionado en",
    "reparacion-aire-acondicionado": "¿Reparan aire acondicionado en",
    "venta-equipos-climatizacion": "¿Venden e instalan aire acondicionado en",
}


def _pregunta_zona(servicio):
    """La pregunta que se hace antes de escribir: "¿llegas hasta mi casa?".

    Sale de core/seo.COMUNAS, igual que el resto del sitio: si la lista cambia,
    la respuesta cambia sola y no queda una pagina que la contradiga. Va en el
    FAQ VISIBLE, asi que tambien puede ir en el FAQPage.
    """
    resto = seo.COMUNAS
    return (
        f"{_ACCION[servicio['slug']]} {seo.ZONA_PRINCIPAL}?",
        f"Sí. {seo.ZONA_PRINCIPAL} es nuestra zona principal, y también atendemos "
        f"en {', '.join(resto[:-1])} y {resto[-1]}. Si estás en otra comuna, "
        "escríbenos y te confirmamos antes de agendar.",
    )


for _s in SERVICIOS:
    _s["preguntas"] = [_pregunta_zona(_s)] + _s["preguntas"]
    _s.setdefault("secciones", [])

_POR_SLUG = {s["slug"]: s for s in SERVICIOS}


def servicio(slug):
    return _POR_SLUG.get(slug)


def relacionados_de(datos):
    return [_POR_SLUG[s] for s in datos.get("relacionados", []) if s in _POR_SLUG]
