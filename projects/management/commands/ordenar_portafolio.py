"""Deja en la portada las fotos que muestran el trabajo, no las primeras que se subieron.

POR QUE
-------
La home muestra 6 de los 12 trabajos publicados, intercalando instalaciones y
mantenciones -- eso esta bien y tiene su razon: tomando los 6 primeros por fecha
salian 6 mantenciones seguidas y parecia que solo hacen eso. Pero DENTRO de cada
grupo tomaba los tres mas antiguos, y mirando las 12 juntas:

  . la primera de todas era la sala de clases -- oscura, con estanterias, sillas
    y cortinas, y el equipo chico y perdido arriba;
  . otra NO MUESTRA NINGUN EQUIPO: es una pared con una canaleta;
  . una tercera trae una marca de agua de Instagram encima.

Y quedaban fuera las tres mejores: el split ABIERTO con los filtros a la vista
(lo unico que muestra en que consiste una mantencion), la unidad exterior con su
soporte y canalizacion, y dos instalaciones limpias.

ESTO SE CORRE UNA VEZ. Despues el orden lo maneja Francisco desde el panel: el
campo "Orden" se edita en la lista de trabajos, sin abrir cada ficha.

GUARDA: antes de escribir comprueba que cada id siga siendo el trabajo que se
reviso. Si no calza -- otra base, otro ambiente, trabajos borrados -- no toca
nada y lo dice. Ordenar por un id que ya es otra foto seria peor que no hacerlo.
"""
from django.core.management.base import BaseCommand

from projects.models import Project

# id -> (titulo que debe tener, orden, por que)
# Los ids salieron de /trabajos/ en produccion el 04-10-2026, y las fotos se
# miraron una por una en una hoja de contacto.
ORDEN = {
    4:  ("Instalación de aire acondicionado (04)", 10, "split limpio sobre pared lisa, bien encuadrado"),
    10: ("Mantención de aire acondicionado (03)",  20, "el equipo ABIERTO con los filtros a la vista"),
    3:  ("Instalación de aire acondicionado (03)", 30, "split sobre la puerta, se ve el ambiente"),
    11: ("Mantención de aire acondicionado (04)",  40, "unidad exterior con soporte y canalizacion"),
    6:  ("Instalación de aire acondicionado (06)", 50, "split en pared clara"),
    13: ("Mantención de aire acondicionado (06)",  60, "split blanco nitido"),
    # El resto queda detras, en /trabajos/ pero fuera de la portada.
    8:  ("Mantención de aire acondicionado (01)",  70, "Francisco trabajando; vertical, entorno cargado"),
    12: ("Mantención de aire acondicionado (05)",  80, "split sobre vano"),
    9:  ("Mantención de aire acondicionado (02)",  90, "living con luz amarillenta"),
    7:  ("Instalación de aire acondicionado (07)", 100, "sala de clases: oscura y desordenada"),
    5:  ("Instalación de aire acondicionado (05)", 110, "NO se ve ningun equipo, solo una pared"),
    2:  ("Instalación de aire acondicionado (02)", 120, "trae marca de agua de Instagram"),
}


class Command(BaseCommand):
    help = "Ordena el portafolio para que la portada abra con las mejores fotos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirmar", action="store_true",
            help="Escribe de verdad. Sin esto es un ensayo y no toca nada.")

    def handle(self, *args, **opciones):
        confirmar = opciones["confirmar"]
        encontrados = Project.objects.in_bulk(ORDEN.keys())

        faltan, no_calzan, cambios = [], [], []
        for pk, (titulo, orden, motivo) in sorted(ORDEN.items(), key=lambda x: x[1][1]):
            p = encontrados.get(pk)
            if p is None:
                faltan.append(pk)
                continue
            if p.title != titulo:
                no_calzan.append((pk, titulo, p.title))
                continue
            if p.orden != orden:
                cambios.append((p, orden, motivo))

        if faltan or no_calzan:
            self.stdout.write(self.style.ERROR(
                "NO SE TOCO NADA: los ids de esta base no son los que se revisaron."))
            for pk in faltan:
                self.stdout.write(f"  id {pk}: no existe")
            for pk, esperado, real in no_calzan:
                self.stdout.write(f"  id {pk}: se esperaba «{esperado}» y es «{real}»")
            self.stdout.write(
                "\nEl orden se revisó mirando las fotos una por una. Aplicarlo sobre\n"
                "otros trabajos pondría cualquier foto en la portada.")
            return

        if not cambios:
            self.stdout.write(self.style.SUCCESS("Ya estaba ordenado: no hay nada que cambiar."))
            return

        for p, orden, motivo in cambios:
            self.stdout.write(f"  {p.orden:>4} -> {orden:>4}  {p.title}   ({motivo})")
            if confirmar:
                p.orden = orden
                p.save(update_fields=["orden"])

        if confirmar:
            self.stdout.write(self.style.SUCCESS(f"\n{len(cambios)} trabajos reordenados."))
            self.stdout.write("De aquí en adelante lo cambia Francisco desde el panel.")
        else:
            self.stdout.write(self.style.WARNING(
                f"\nENSAYO: {len(cambios)} cambios. Con --confirmar se aplican."))
