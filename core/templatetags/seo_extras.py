"""Filtro para volcar un dict como JSON-LD en la plantilla."""
import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Dentro de <script> el autoescape de Django convierte las comillas en &quot;
# y el JSON queda ilegible para Google (paso con el FAQ hasta el 22-09-2026).
# Por eso se marca seguro. Lo que SI hay que escapar es <, > y &, para que un
# texto con "</script>" no pueda cerrar la etiqueta: se escriben como <...,
# que sigue siendo el mismo JSON.
_ESCAPES = {ord("<"): "\\u003c", ord(">"): "\\u003e", ord("&"): "\\u0026"}


@register.filter
def como_json(valor):
    return mark_safe(json.dumps(valor, ensure_ascii=False).translate(_ESCAPES))


@register.filter
def miles(valor):
    """12000 -> "12.000", como se escriben los BTU en Chile (core/btu.py)."""
    from core.btu import miles as _miles
    return _miles(int(valor))
