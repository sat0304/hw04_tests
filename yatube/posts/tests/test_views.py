from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
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
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'posts/index.html': 
                reverse('posts:index'),
            'posts/group_list.html': 
                reverse('posts:group_list', kwargs={'slug': self.group.slug}
            ),
            'posts/profile.html':
                reverse('posts:profile', kwargs={'username': self.post.author}
            ),
            'posts/post_detail.html': 
                reverse('posts:post_detail', kwargs={'post_id': self.post.pk}
            ),
            'posts/create_post.html': 
                reverse('posts:post_edit', kwargs={'post_id': self.post.pk}
            ),
            'posts/create_post.html': 
                reverse('posts:post_create'),
            
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
    
    def test_task_list_page_list_is_1(self):
        # Удостоверимся, что на страницу со списком заданий передаётся
        # ожидаемое количество объектов
        
        response = self.authorized_client.get(reverse('deals:task_list'))
        self.assertEqual(response.context['object_list'].count(), 1)

    # Проверяем, что словарь context страницы /task
    # в первом элементе списка object_list содержит ожидаемые значения
    def test_task_list_page_show_correct_context(self):
        """Шаблон task_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('deals:task_list'))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['object_list'][0]
        task_title_0 = first_object.title
        task_text_0 = first_object.text
        task_slug_0 = first_object.slug
        self.assertEqual(task_title_0, 'Заголовок')
        self.assertEqual(task_text_0, 'Текст')
        self.assertEqual(task_slug_0, 'test-slug')

    # Проверяем, что словарь context страницы task/test-slug
    # содержит ожидаемые значения
    def test_task_detail_pages_show_correct_context(self):
        """Шаблон task_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('deals:task_detail', kwargs={'slug': 'test-slug'})
            )
        self.assertEqual(response.context['task'].title, 'Заголовок')
        self.assertEqual(response.context['task'].text, 'Текст')
        self.assertEqual(response.context['task'].slug, 'test-slug')

    def test_initial_value(self):
        """Предустановленнное значение формы."""
        response = self.guest_client.get(reverse('deals:home'))
        title_inital = response.context['form'].fields['title'].initial
        self.assertEqual(title_inital, 'Значение по-умолчанию')
