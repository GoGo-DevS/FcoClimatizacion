"""Filtro para volcar un dict como JSON-LD en la plantilla."""
import json

from django import template

register = template.Library()


@register.filter
def como_json(valor):
    return json.dumps(valor, ensure_ascii=False)
