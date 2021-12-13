from django.test import Client, TestCase


class StaticURLTests(TestCase):
    """ Тест страниц сайта."""

    def setUp(self):
        """Клиент неавторизован."""
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

