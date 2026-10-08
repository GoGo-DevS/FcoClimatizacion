"""Lo que cada ficha de trabajo le dice a Google, sacado SOLO de sus datos.

POR QUE EXISTE (07-10-2026)
---------------------------
Search Console dejo 7 de las 13 fichas en "Descubierta, actualmente sin
indexar", y las que entraron salen en la posicion 12. La causa es que eran
iguales entre si: mismo titulo salvo el numero, la MISMA meta description en
todas las instalaciones (la descripcion generica de `fill_metadata`), ningun
enlace al servicio y ninguno a otros trabajos. Para Google eran la misma pagina
repetida.

LA REGLA, la de todo el repo: no se afirma nada que el trabajo no tenga. Si
Francisco no cargo la comuna, el titulo NO dice una comuna. La zona de
cobertura del negocio se puede decir (es del negocio, no del trabajo), pero
nunca como si fuera el lugar de ese trabajo.

Se resuelve aca y no en el modelo a proposito: el build BORRA Y RECREA los
trabajos en cada deploy (ver `_segmented_import`). Todo lo que se calcula en
la vista sobrevive solo; un campo nuevo habria que rescatarlo a mano.
"""
import re

from django.urls import reverse

from core import seo

from .utils import is_segmented_title

LIMITE_TITULO = 60
LIMITE_META = 155
MARCA = "FCO Climatización"

# familia -> (nombre que se publica, participio para la descripcion)
FAMILIAS = {
    "instalacion": ("Instalación de aire acondicionado", "realizada"),
    "mantencion": ("Mantención de aire acondicionado", "realizada"),
    "trabajo": ("Trabajo de climatización", "realizado"),
}

# Que servicio explica cada familia. "trabajo" no tiene uno: no se sabe que fue.
SERVICIO_DE_FAMILIA = {
    "instalacion": "instalacion-aire-acondicionado",
    "mantencion": "mantencion-aire-acondicionado",
}

# Que trabajos se muestran en cada pagina de servicio. Venta va con las
# instalaciones porque es "venta CON instalacion": lo que se ve en la foto es la
# instalacion. Reparacion no tiene trabajos propios en el portafolio y no se le
# cuelgan los de otra familia: seria mostrar algo que no es una reparacion.
FAMILIA_DE_SERVICIO = {
    "instalacion-aire-acondicionado": "instalacion",
    "mantencion-aire-acondicionado": "mantencion",
    "venta-equipos-climatizacion": "instalacion",
}

_NUMERO = re.compile(r"\((\d{2})\)\s*$")


def familia_de(titulo):
    t = (titulo or "").strip().lower()
    if t.startswith(("instalación", "instalacion")):
        return "instalacion"
    if t.startswith(("mantención", "mantencion")):
        return "mantencion"
    return "trabajo"


def numero_de(titulo):
    m = _NUMERO.search(titulo or "")
    return m.group(1) if m else ""


def _miles(n):
    return f"{n:,}".replace(",", ".")


def _recortar(texto, limite):
    """Corta en una palabra completa y marca el corte. Nunca a media palabra."""
    texto = " ".join((texto or "").split())
    if len(texto) <= limite:
        return texto
    corte = texto[: limite - 1].rsplit(" ", 1)[0].rstrip(",.;:")
    return corte + "…"


def _descripcion_propia(project):
    """La descripcion SOLO si la escribio alguien para ESTE trabajo.

    La generica de `fill_metadata` es la misma en todas las fichas de la
    familia: usarla de meta description es justo lo que las hacia duplicadas.
    """
    from .management.commands.fill_metadata import DESCRIPCION_POR_FAMILIA

    texto = (project.description or "").strip()
    if not texto or texto in DESCRIPCION_POR_FAMILIA.values():
        return ""
    return texto


def _titulo(nombre, numero, comuna):
    sufijo = f" ({numero})" if numero else ""
    candidatos = []
    if comuna:
        candidatos += [
            f"{nombre} en {comuna}{sufijo} | {MARCA}",
            f"{nombre} en {comuna}{sufijo}",
            f"{nombre} en {comuna}",
        ]
    candidatos += [f"{nombre}{sufijo} | {MARCA}", f"{nombre}{sufijo}"]
    for c in candidatos:
        if len(c) <= LIMITE_TITULO:
            return c
    return _recortar(candidatos[-1], LIMITE_TITULO)


def ficha(project):
    """Titulo, H1, descripcion y servicio de un trabajo. Nada inventado."""
    familia = familia_de(project.title)
    nombre, participio = FAMILIAS[familia]
    numero = numero_de(project.title)
    comuna = (project.comuna or "").strip()
    marca_equipo = (project.brand or "").strip()

    h1 = f"{nombre} en {comuna}" if comuna else nombre
    if numero:
        h1 += f", trabajo {numero}"

    # Lo que se sabe del equipo, si alguien lo cargo.
    equipo = ""
    if marca_equipo and project.btu:
        equipo = f"Equipo {marca_equipo} de {_miles(project.btu)} BTU."
    elif marca_equipo:
        equipo = f"Equipo {marca_equipo}."
    elif project.btu:
        equipo = f"Equipo de {_miles(project.btu)} BTU."

    propia = _descripcion_propia(project)
    if propia:
        meta = _recortar(propia, LIMITE_META)
    else:
        n_fotos = len(getattr(project, "images_list", None) or project.images.all())
        donde = f" en {comuna}" if comuna else ""
        trabajo = f" del trabajo {numero}" if numero else ""
        fotos = (f"{n_fotos} fotos{trabajo}" if n_fotos != 1 else f"1 foto{trabajo}")
        partes = [f"{nombre} {participio} por {MARCA}{donde}: {fotos}."]
        if equipo:
            partes.append(equipo)
        # Sin comuna del trabajo se dice donde atiende el NEGOCIO, con sujeto
        # propio ("Atendemos"), para que no se lea como el lugar de este trabajo.
        extras = [] if comuna else [f"Atendemos en {seo.ZONA_CORTA}."]
        extras.append("Cotiza uno igual por WhatsApp.")
        for extra in extras:
            if len(" ".join(partes + [extra])) <= LIMITE_META:
                partes.append(extra)
        meta = _recortar(" ".join(partes), LIMITE_META)

    slug = SERVICIO_DE_FAMILIA.get(familia)
    return {
        "familia": familia,
        "etiqueta": {"instalacion": "Instalación", "mantencion": "Mantención"}.get(familia, "Trabajo"),
        "nombre": nombre,
        "numero": numero,
        "titulo_seo": _titulo(nombre, numero, comuna),
        "h1": h1,
        "meta": meta,
        "equipo": equipo,
        "servicio_slug": slug,
        "servicio_url": reverse("services:detail", args=[slug]) if slug else "",
    }


def trabajos_de_familia(familia, excluir_id=None, limite=None):
    """Los trabajos publicados de una familia, en el orden del portafolio
    (`Project.orden`, que decide Francisco desde el panel)."""
    from .models import Project

    trabajos = [
        p for p in Project.objects.prefetch_related("images")
        if is_segmented_title(p.title) and familia_de(p.title) == familia
        and p.id != excluir_id
    ]
    return trabajos[:limite] if limite else trabajos
