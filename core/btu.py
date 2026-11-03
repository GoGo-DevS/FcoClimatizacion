"""La guia "¿Cuántos BTU necesito?" (/cuantos-btu-necesito/).

POR QUE EXISTE (03-11-2026)
---------------------------
En el autocompletado de Google (Chile) la capacidad es un grupo grande y
propio: "cuantos btu necesito para 20 / 25 / 30 / 40 / 50 / 60 metros
cuadrados", "para un cuarto de 3x3 / 4x4 / 5x5", "12000 / 9000 / 18000 /
24000 btu para cuantos metros cuadrados", "tabla btu por metro cuadrado",
"calculadora btu". La portada tenia la calculadora, pero ninguna pagina
respondia esas preguntas, y el sitio no aparecia para ninguna.

La SERP chilena de esas busquedas (revisada el 03-11) la ocupan instaladores
chicos como FCO (prothermic.cl, ventoclima.cl, climaencasa.cl, rdelectric.cl,
climatizacionrancagua.cl), no el retail: es una busqueda que se puede ganar.

LA TABLA NO SE ESCRIBE A MANO: sale de la MISMA formula que la calculadora
(static/js/capacidad.js), y una prueba corre el script con node sobre cada
celda (core/tests_btu.py). Si alguien cambia la formula en un lado y no en el
otro, la prueba falla. La formula es la que publicaba el sitio original: 600
BTU por m2, +15 % con sol directo, +20 % con muchas personas o equipos, y se
redondea al tamano comercial siguiente.

Es una referencia general del oficio, no una promesa: la capacidad final se
confirma en la visita. Sin precios (Francisco no los ha confirmado).
"""

TAMANOS = [9000, 12000, 18000, 24000, 30000, 36000, 48000]
USOS = ("normal", "caluroso", "muchas_personas")

# Las piezas que mas se buscan (autocompletado), con su etiqueta.
FILAS_M2 = [
    (9, "pieza de 3 x 3 m"),
    (12, ""),
    (15, ""),
    (16, "pieza de 4 x 4 m"),
    (20, ""),
    (25, "pieza de 5 x 5 m"),
    (30, ""),
    (35, ""),
    (40, ""),
    (50, ""),
    (60, ""),
]
# Los equipos de "12000 btu para cuantos metros cuadrados".
EQUIPOS = [9000, 12000, 18000, 24000, 30000, 36000]

BTU_POR_FRIGORIA = 3.968      # 1 frigoria/h = 1 kcal/h = 3,968 BTU/h
KW_POR_BTU = 0.00029307107    # 1 BTU/h = 0,293 W


def estimar_btu(m2, uso="normal"):
    """Igual que estimarBTU() de capacidad.js, operacion por operacion, para
    que los decimales den lo mismo (Python y JS usan el mismo double)."""
    btu = m2 * 600
    if uso == "caluroso":
        btu *= 1.15
    if uso == "muchas_personas":
        btu *= 1.2
    for tamano in TAMANOS:
        if btu <= tamano:
            return tamano
    return TAMANOS[-1]


def m2_maximos(equipo, uso="normal"):
    """Los m2 enteros mas grandes para los que la formula recomienda ESE
    equipo o uno menor: "12.000 BTU para cuantos metros cuadrados"."""
    maximo = 0
    for m2 in range(1, 201):
        if estimar_btu(m2, uso) <= equipo:
            maximo = m2
    return maximo


def miles(n):
    """12000 -> "12.000", como se escribe en Chile."""
    return f"{n:,}".replace(",", ".")


def frigorias(btu):
    """Aproximadas a la decena: 12.000 BTU -> "3.020"."""
    return miles(int(round(btu / BTU_POR_FRIGORIA, -1)))


def kw(btu):
    """Con coma decimal: 12.000 BTU -> "3,5"."""
    return f"{btu * KW_POR_BTU:.1f}".replace(".", ",")


def tabla_por_m2():
    return [
        {"m2": m2, "etiqueta": etiqueta,
         "btu": {uso: estimar_btu(m2, uso) for uso in USOS}}
        for m2, etiqueta in FILAS_M2
    ]


def tabla_por_equipo():
    return [
        {"btu": e, "m2": {uso: m2_maximos(e, uso) for uso in USOS},
         "frigorias": frigorias(e), "kw": kw(e)}
        for e in EQUIPOS
    ]


def _recomendacion(m2):
    """Texto de una respuesta: la cifra normal y, si cambia, la de sol o
    muchas personas. Sale de la formula, nunca escrito a mano."""
    normal = estimar_btu(m2, "normal")
    sol = estimar_btu(m2, "caluroso")
    personas = estimar_btu(m2, "muchas_personas")
    if normal == sol == personas:
        return (f"Unos {miles(normal)} BTU, y alcanzan incluso si el ambiente recibe "
                "sol directo o se juntan muchas personas.")
    if sol == personas:
        return (f"Unos {miles(normal)} BTU en un ambiente normal. Si recibe sol "
                f"directo o se juntan muchas personas, conviene {miles(sol)} BTU.")
    return (f"Unos {miles(normal)} BTU en un ambiente normal, {miles(sol)} BTU si "
            f"recibe sol directo y {miles(personas)} BTU si se juntan muchas personas.")


def resumen():
    """La respuesta corta que va arriba de todo y en la meta."""
    return [(e, m2_maximos(e)) for e in (9000, 12000, 18000, 24000)]


def resumen_texto():
    """"9.000 BTU alcanzan hasta 15 m², 12.000 BTU hasta 20 m², ..." """
    partes = [f"{miles(e)} BTU hasta {m2} m²" for e, m2 in resumen()]
    partes[0] = partes[0].replace(" hasta", " alcanzan hasta", 1)
    return ", ".join(partes[:-1]) + " y " + partes[-1]


def meta():
    """La descripcion de la pagina: la respuesta misma, en 160 caracteres."""
    partes = [f"{miles(e)} BTU hasta {m2} m²" for e, m2 in resumen()]
    return ("Tabla de BTU por metro cuadrado: " + ", ".join(partes[:-1]) + " y "
            + partes[-1] + ". Con calculadora.")


def preguntas():
    """FAQ visible y marcada (FAQPage). Las cifras salen de la formula."""
    doce = 12000
    return [
        ("¿Cuántos BTU necesito para 20 m²?", _recomendacion(20)),
        ("¿Para cuántos metros cuadrados sirve un aire acondicionado de 12.000 BTU?",
         f"Hasta unos {m2_maximos(doce)} m² en un ambiente normal, "
         f"{m2_maximos(doce, 'caluroso')} m² si recibe sol directo y "
         f"{m2_maximos(doce, 'muchas_personas')} m² si se juntan muchas personas "
         "o equipos encendidos."),
        ("¿Cuántos BTU necesito para una pieza de 4x4?",
         "Una pieza de 4 x 4 m tiene 16 m². " + _recomendacion(16)),
        ("¿Cuántos BTU necesito para 40 m²?", _recomendacion(40)),
        ("¿Cuántas frigorías son 12.000 BTU?",
         f"Unas {frigorias(doce)} frigorías, o {kw(doce)} kW. Una frigoría equivale "
         "a unos 3,97 BTU."),
        ("¿Cómo se confirma la capacidad?",
         "En la visita técnica: se miran la altura del techo, la orientación, la "
         "aislación y el recorrido de la cañería. La tabla y la calculadora son una "
         "referencia para partir."),
    ]
