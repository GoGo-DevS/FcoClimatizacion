"""Deja en la portada las fotos que muestran el trabajo, no las primeras que se subieron.

POR QUE
-------
La home muestra 6 de los 12 trabajos publicados, intercalando instalaciones y
mantenciones -- eso esta bien y tiene su razon: tomando los 6 primeros por fecha
salian 6 mantenciones seguidas y parecia que solo hacen eso. Pero DENTRO de cada
grupo tomaba los tres mas antiguos, y mirando las 12 fotos juntas:

  . la primera de todas era la sala de clases -- oscura, con estanterias, sillas
    y cortinas, y el equipo chico y perdido entre los tubos fluorescentes;
  . otra NO MUESTRA NINGUN EQUIPO: es una pared con una canaleta;
  . una tercera trae una marca de agua de Instagram encima.

Y quedaban fuera las tres mejores: el split ABIERTO con los filtros a la vista
(lo unico que muestra en que consiste una mantencion), la unidad exterior con su
soporte y canalizacion, y dos instalaciones limpias.

POR TITULO, NO POR ID
---------------------
Los importadores del build BORRAN y RECREAN los trabajos en cada despliegue, asi
que los ids cambian. Lo que no cambia es el titulo: "(03)" sigue siendo el (03)
despues de reimportar, y por eso `_segmented_import` ya rescata por titulo lo
que edita el cliente. El `orden` viaja en ese mismo rescate.

Corre en el build y es idempotente: si ya esta ordenado, no escribe. Despues el
orden lo maneja Francisco desde el panel -- el campo "Orden" se edita en la
lista de trabajos, sin abrir cada ficha -- y sus cambios NO se pisan, porque el
comando solo toca lo que todavia tiene el valor por defecto.
"""
from django.core.management.base import BaseCommand

from projects.models import Project

# titulo -> (orden, por que)
# Las fotos se miraron una por una en una hoja de contacto el 04-10-2026.
ORDEN = {
    "Instalación de aire acondicionado (04)": (10, "split limpio sobre pared lisa"),
    "Mantención de aire acondicionado (03)":  (20, "el equipo ABIERTO, con los filtros a la vista"),
    "Instalación de aire acondicionado (03)": (30, "split sobre la puerta, se ve el ambiente"),
    "Mantención de aire acondicionado (04)":  (40, "unidad exterior con soporte y canalizacion"),
    "Instalación de aire acondicionado (06)": (50, "split en pared clara"),
    "Mantención de aire acondicionado (06)":  (60, "split blanco nitido"),
    # El resto sigue publicado en /trabajos/, pero fuera de la portada.
    "Mantención de aire acondicionado (01)":  (70, "Francisco trabajando; vertical y entorno cargado"),
    "Mantención de aire acondicionado (05)":  (80, "split sobre vano"),
    "Mantención de aire acondicionado (02)":  (90, "living con luz amarillenta"),
    "Instalación de aire acondicionado (07)": (100, "sala de clases: oscura y desordenada"),
    "Instalación de aire acondicionado (05)": (110, "NO se ve ningun equipo, solo una pared"),
    "Instalación de aire acondicionado (02)": (120, "trae marca de agua de Instagram"),
}

POR_DEFECTO = 100   # el default del campo: "nadie lo ha tocado"


class Command(BaseCommand):
    help = "Ordena el portafolio para que la portada abra con las mejores fotos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirmar", action="store_true",
            help="Escribe de verdad. Sin esto es un ensayo y no toca nada.")
        parser.add_argument(
            "--forzar", action="store_true",
            help="Reordena TAMBIEN los que Francisco ya movio. Por defecto no se tocan.")

    def handle(self, *args, **opciones):
        confirmar, forzar = opciones["confirmar"], opciones["forzar"]

        cambios, respetados, sin_encontrar = [], [], []
        for titulo, (orden, motivo) in sorted(ORDEN.items(), key=lambda x: x[1][0]):
            p = Project.objects.filter(title=titulo).first()
            if p is None:
                sin_encontrar.append(titulo)
                continue
            if p.orden == orden:
                continue
            # Si ya no tiene el valor por defecto, lo movio alguien: no se pisa.
            if p.orden != POR_DEFECTO and not forzar:
                respetados.append((titulo, p.orden))
                continue
            cambios.append((p, orden, motivo))

        for titulo, actual in respetados:
            self.stdout.write(f"  se respeta  {titulo} (en {actual}, lo movio el cliente)")
        for titulo in sin_encontrar:
            self.stdout.write(f"  no existe   {titulo}")

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
        else:
            self.stdout.write(self.style.WARNING(
                f"\nENSAYO: {len(cambios)} cambios. Con --confirmar se aplican."))
