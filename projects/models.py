from django.db import models

PROJECT_TYPE_CHOICES = [
    ("casa", "Casa"),
    ("depto", "Departamento"),
    ("local", "Local/Oficina"),
]

class Project(models.Model):
    title = models.CharField("Título", max_length=120)
    comuna = models.CharField("Comuna", max_length=80, blank=True)
    # Sin default: "RM" por omision hacia que el sitio afirmara la region de
    # un trabajo que nadie completo. Vacio = no se dice nada.
    region = models.CharField("Región", max_length=80, blank=True)
    project_type = models.CharField("Tipo", max_length=20, choices=PROJECT_TYPE_CHOICES, default="casa")
    brand = models.CharField("Marca", max_length=60, blank=True)
    btu = models.PositiveIntegerField("BTU", blank=True, null=True)

    description = models.TextField("Descripción", blank=True)
    featured = models.BooleanField("Destacado", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


def project_image_path(instance, filename):
    # media/projects/<project_id>/<filename>
    return f"projects/{instance.project_id}/{filename}"


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=project_image_path)
    alt = models.CharField("Texto alternativo", max_length=140, blank=True)
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Imagen - {self.project.title}"
