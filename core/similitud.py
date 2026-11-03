"""Cuanto texto comparten dos paginas del sitio (lo usan las pruebas).

Regla del metodo SEO (03-11-2026): nada de paginas casi iguales. En Punto
Parcelas tres paginas eran 96 % identicas (misma grilla, otro H1) y Google las
trato como una sola. Una pagina nueva tiene que responder su propia pregunta.

Se compara solo el <main> (el menu y el pie se repiten en todo el sitio a
proposito) en tramos de 5 palabras: la parte de los tramos de una pagina que
tambien aparecen en la otra.
"""
import html as html_lib
import re

_TAG = re.compile(r"<[^>]+>")
_BLOQUES_FUERA = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)


def texto_principal(html):
    """El texto visible dentro de <main>, en minusculas y sin etiquetas."""
    if "<main" in html:
        html = html.split("<main", 1)[1].split("</main>", 1)[0]
    html = _BLOQUES_FUERA.sub(" ", html)
    texto = html_lib.unescape(_TAG.sub(" ", html)).lower()
    return re.findall(r"\w+", texto)


def tramos(palabras, n=5):
    return {" ".join(palabras[i:i + n]) for i in range(len(palabras) - n + 1)}


def parte_copiada(html_nueva, html_otra, n=5):
    """Que fraccion de los tramos de `html_nueva` aparece tambien en `html_otra`
    (0 = nada en comun, 1 = todo su texto esta en la otra)."""
    a = tramos(texto_principal(html_nueva), n)
    b = tramos(texto_principal(html_otra), n)
    return len(a & b) / len(a) if a else 0.0
