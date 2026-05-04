from django.db import models

PREFERENCE_CHOICES = [
    ("whatsapp", "WhatsApp"),
    ("email", "Email"),
    ("both", "Ambos"),
]

SERVICE_CHOICES = [
    ("instalacion", "Instalación"),
    ("venta", "Venta de aire acondicionado"),
    ("reparacion", "Reparación"),
    ("mantencion", "Mantenimiento"),
]

PROPERTY_CHOICES = [
    ("casa", "Casa"),
    ("depto", "Departamento"),
    ("local", "Local/Oficina"),
]

STATUS_CHOICES = [
    ("nuevo", "Nuevo"),
    ("contactado", "Contactado"),
    ("agendado", "Agendado"),
    ("cerrado", "Cerrado"),
    ("perdido", "Perdido"),
]

COMUNA_CHOICES = [
    ("Santiago", "Santiago"),
    ("Maipú", "Maipú"),
    ("Pudahuel", "Pudahuel"),
    ("Providencia", "Providencia"),
    ("Las Condes", "Las Condes"),
]

class Lead(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    full_name = models.CharField("Nombre", max_length=120)
    phone = models.CharField("Teléfono", max_length=30)
    email = models.EmailField("Email", blank=True)

    comuna = models.CharField("Comuna", max_length=60, choices=COMUNA_CHOICES)
    property_type = models.CharField("Tipo de inmueble", max_length=20, choices=PROPERTY_CHOICES)

    service = models.CharField("Servicio", max_length=20, choices=SERVICE_CHOICES)
    area_m2 = models.PositiveIntegerField("Metros² aprox", blank=True, null=True)

    message = models.TextField("Mensaje", blank=True)
    contact_preference = models.CharField("Preferencia de contacto", max_length=10, choices=PREFERENCE_CHOICES, default="both")
    status = models.CharField("Estado", max_length=12, choices=STATUS_CHOICES, default="nuevo")

    def __str__(self):
        return f"{self.full_name} - {self.get_service_display()} ({self.comuna})"
