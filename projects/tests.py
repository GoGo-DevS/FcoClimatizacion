from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from projects.utils import is_segmented_title


class SegmentationTests(TestCase):
    def test_is_segmented_title(self):
        self.assertTrue(is_segmented_title("Instalacion residencial - RM (01)"))
        self.assertTrue(is_segmented_title("Mantencion preventiva - Valparaiso (06)"))
        self.assertTrue(is_segmented_title("Trabajo realizado - Biobio (03)"))
        self.assertFalse(is_segmented_title("Mantencion de aire acondicionado (01)"))
        self.assertFalse(is_segmented_title("Centro Educacional Gaspar Cabrales"))

    def test_projects_list_shows_only_segmented_titles(self):
        Project.objects.create(title="Instalacion comercial - RM (01)", featured=True, region="RM")
        Project.objects.create(title="Mantencion de aire acondicionado (01)", featured=True, region="RM")

        response = self.client.get(reverse("projects:list"))

        self.assertContains(response, "Instalacion comercial - RM (01)")
        self.assertNotContains(response, "Mantencion de aire acondicionado (01)")
