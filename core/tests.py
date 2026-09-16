"""La medicion no puede fallar en silencio.

Los dos modos de fallo que cubren estas pruebas son reales y NINGUNO da error:

  1. Que el sitio publique el script de Analytics con el ID vacio. Google
     recibe visitas que no puede atribuir y el panel se queda en cero sin que
     nada avise.
  2. Que la etiqueta de verificacion desaparezca del <head> despues de estar
     puesta. Google la revalida cada cierto tiempo: si ya no esta, se pierde el
     acceso a Search Console semanas despues y nadie lo conecta con el cambio
     que la borro.
"""
from django.test import TestCase, override_settings
from django.urls import reverse


class MedicionApagadaPorDefecto(TestCase):
    """Sin las variables en el entorno, el head no dibuja NADA."""

    @override_settings(GA4_MEASUREMENT_ID="", GOOGLE_SITE_VERIFICATION="")
    def test_sin_variables_no_carga_analytics(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertNotIn("googletagmanager", html)
        self.assertNotIn("gtag(", html)

    @override_settings(GA4_MEASUREMENT_ID="", GOOGLE_SITE_VERIFICATION="")
    def test_sin_variables_no_hay_etiqueta_de_verificacion(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertNotIn("google-site-verification", html)


@override_settings(
    GA4_MEASUREMENT_ID="G-TEST12345",
    GOOGLE_SITE_VERIFICATION="cadena-de-verificacion-de-prueba",
)
class MedicionEncendida(TestCase):

    def test_carga_el_script_con_el_id_real(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn("googletagmanager.com/gtag/js?id=G-TEST12345", html)
        self.assertIn("gtag('config', 'G-TEST12345')", html)

    def test_la_etiqueta_de_verificacion_esta_en_la_portada(self):
        # En la PORTADA, que es la que revisa Google.
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn(
            '<meta name="google-site-verification" '
            'content="cadena-de-verificacion-de-prueba">',
            html,
        )
