from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from models import Group, Post


User = get_user_model()

class PostURLTests(TestCase):
    """ Тест страниц сайта."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый_текст',
        )

    def setUp(self):
        """Клиент неавторизован."""
        self.guest_client = Client()
        """Клиент авторизован."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': '/',
            'group_list.html': '/added/',
            'deals/task_list.html': '/task/',
            'deals/task_detail.html': '/task/test-slug/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
