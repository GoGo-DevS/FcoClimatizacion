from django.test import TestCase


class CreditoGoGoDevS(TestCase):
    """07-10-2026: el pie no decia quien hizo el sitio."""

    def test_el_pie_enlaza_a_gogodevs(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Sitio desarrollado por <a href="https://www.gogodevs.cl/"', r.content.decode())
