import random
from django.core.management.base import BaseCommand
from projects.models import Project

REGION_COMUNAS = {
    "RM": ["Santiago", "Maipú", "Pudahuel", "Providencia", "Las Condes", "Ñuñoa", "Puente Alto", "La Florida", "San Bernardo"],
    "Valparaíso": ["Viña del Mar", "Valparaíso", "Quilpué", "Villa Alemana", "Concón"],
    "Antofagasta": ["Antofagasta", "Calama"],
    "Atacama": ["Copiapó"],
    "Coquimbo": ["La Serena", "Coquimbo"],
    "Biobío": ["Concepción", "Talcahuano", "San Pedro de la Paz"],
    "Los Lagos": ["Puerto Montt", "Osorno"],
    "Araucanía": ["Temuco"],
}

BRANDS = ["CLARK", "Kendal", "Anwo", "Midea", "LG", "Samsung", "Gree", "Hisense"]
BTU_OPTIONS = [9000, 12000, 18000, 24000, 30000, 36000, 48000]

TYPE_MAP = {
    "residencial": ["casa", "depto"],
    "comercial": ["local"],
    "oficina": ["local"],
    "local": ["local"],
    "casa": ["casa"],
    "depto": ["depto"],
    "multipunto": ["local", "casa"],
    "split mural": ["casa", "depto", "local"],
}

DESC_TEMPLATES = [
    "Instalación profesional con terminaciones prolijas, prueba de funcionamiento y puesta en marcha. Incluye asesoría de capacidad (BTU) y recomendaciones de uso.",
    "Montaje e instalación de equipo split con canalización y ajuste final. Trabajo limpio, verificación y garantía.",
    "Instalación realizada por FCOCLIMATIZACION con validación de funcionamiento, fijaciones seguras y terminaciones.",
    "Proyecto ejecutado con estándar profesional: instalación, pruebas y recomendaciones para optimizar consumo.",
]

TITLE_PREFIXES = [
    "Instalación residencial",
    "Instalación comercial",
    "Instalación en oficina",
    "Instalación split mural",
    "Instalación multipunto",
]

def pick_region_and_comuna():
    region = random.choice(list(REGION_COMUNAS.keys()))
    comuna = random.choice(REGION_COMUNAS[region])
    return region, comuna

def infer_type_from_title(title: str):
    t = title.lower()
    for key, choices in TYPE_MAP.items():
        if key in t:
            return random.choice(choices)
    return random.choice(["casa", "depto", "local"])

def infer_title_base(title: str):
    # Si ya viene "Instalación ..." lo dejamos, si no le ponemos uno bonito
    low = title.lower()
    if "instalación" in low:
        return title
    return f"{random.choice(TITLE_PREFIXES)}"

class Command(BaseCommand):
    help = "Rellena comuna/region/marca/btu/tipo/descripcion para proyectos con datos vacíos (look tipo IMG3)."

    def add_arguments(self, parser):
        parser.add_argument("--only_prefix", type=str, default="Instalación", help="Solo proyectos cuyo título empiece con este prefijo")
        parser.add_argument("--force", action="store_true", help="Si se incluye, sobreescribe campos aunque ya tengan valor")

    def handle(self, *args, **opts):
        prefix = opts["only_prefix"]
        force = opts["force"]

        qs = Project.objects.filter(title__startswith=prefix).order_by("id")
        updated = 0

        for p in qs:
            changed = False

            # region + comuna
            if force or not p.region or not p.comuna:
                region, comuna = pick_region_and_comuna()
                if force or not p.region:
                    p.region = region
                    changed = True
                if force or not p.comuna:
                    p.comuna = comuna
                    changed = True

            # tipo inmueble (project_type)
            if force or not p.project_type:
                p.project_type = infer_type_from_title(p.title)
                changed = True

            # marca
            if force or not p.brand:
                p.brand = random.choice(BRANDS)
                changed = True

            # BTU
            if force or not p.btu:
                # heurística: comerciales tienden a más BTU
                base = random.choice(BTU_OPTIONS)
                if "comercial" in p.title.lower() or "local" in p.title.lower() or "multipunto" in p.title.lower():
                    base = random.choice([18000, 24000, 30000, 36000, 48000])
                p.btu = base
                changed = True

            # descripción
            if force or not p.description:
                p.description = random.choice(DESC_TEMPLATES)
                changed = True

            # Ajuste de título para verse pro (opcional leve)
            # (No cambia tu numeración, solo agrega región/comuna al final si quieres)
            # lo dejamos comentado para no tocarlo sin necesidad:
            # p.title = infer_title_base(p.title)

            if changed:
                p.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"OK ✅ Actualizados {updated} proyectos."))