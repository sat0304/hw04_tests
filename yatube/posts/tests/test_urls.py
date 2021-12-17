from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    """ Тест страниц сайта."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.auth = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.auth,
            text='Тестовый_текст',
        )

    def setUp(self):
        """Клиент неавторизован."""
        self.guest_client = Client()
        """Клиент авторизован."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author = Client()
        self.authorized_author.force_login(self.auth)

    def test_url_exists_at_desired_location_auth(self):
        """URL-адрес существует для автора поста."""
        templates_url_names = {
            '/': 200,
            f'/group/{self.group.slug}/': 200,
            f'/profile/{self.post.author}/': 200,
            f'/posts/{self.post.pk}/': 200,
            f'/posts/{self.post.pk}/edit/': 200,
            '/create/': 200,
            'unexist.html': 404,
        }
        for template, status in templates_url_names.items():
            with self.subTest(status=status):
                response = self.authorized_author.get(template)
                self.assertEqual(response.status_code, status)

    def test_url_exists_at_desired_location_user(self):
        """URL-адрес существует для зарегистрированного."""
        templates_url_names = {
            '/': 200,
            f'/group/{self.group.slug}/': 200,
            f'/profile/{self.post.author}/': 200,
            f'/posts/{self.post.pk}/': 200,
            f'/posts/{self.post.pk}/edit/': 302,
            '/create/': 200,
            'unexist.html': 404,
        }
        for template, status in templates_url_names.items():
            with self.subTest(status=status):
                response = self.authorized_client.get(template)
                self.assertEqual(response.status_code, status)

    def test_url_exists_at_desired_location_not_auth(self):
        """URL-адрес существует для незарегистрированного."""
        templates_url_names = {
            '/': 200,
            f'/group/{self.group.slug}/': 200,
            f'/profile/{self.post.author}/': 200,
            f'/posts/{self.post.pk}/': 200,
            f'/posts/{self.post.pk}/edit/': 302,
            '/create/': 302,
            'unexist.html': 404,
        }
        for template, status in templates_url_names.items():
            with self.subTest(status=status):
                response = self.guest_client.get(template)
                self.assertEqual(response.status_code, status)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.post.author}/',
            'posts/post_detail.html': f'/posts/{self.post.pk}/',
            'posts/create_post.html'or 'posts/update_post.html':
                f'/posts/{self.post.pk}/edit/',
            'posts/create_post.html': '/create/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
