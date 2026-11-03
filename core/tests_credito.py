from django.test import TestCase

# 02-11-2026, consejo de Jorge Urzua (SEO): el enlace a gogodevs.cl lleva la
# palabra clave como texto, no la marca. La marca queda fuera del enlace.
CREDITO = (
    '<a href="https://www.gogodevs.cl/" target="_blank" rel="noopener"{clase}>'
    'Desarrollo web en Chile</a> por GoGoDevS'
)


class CreditoGoGoDevS(TestCase):
    """07-10-2026: el pie no decia quien hizo el sitio."""

    def test_el_pie_enlaza_a_gogodevs_con_la_palabra_clave(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn(CREDITO.format(clase=' class="text-muted"'), html)
        self.assertNotIn('Sitio desarrollado por', html)

    def test_el_tree_enlaza_a_gogodevs_con_la_palabra_clave(self):
        r = self.client.get('/links/')
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn(CREDITO.format(clase=''), html)
        self.assertNotIn('Sitio desarrollado por', html)
