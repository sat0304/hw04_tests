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
            group=cls.group,
        )
        cls.group1 = Group.objects.create(
            title='Тестовая_группа_1',
            slug='test_slug_1',
            description='Тестовое_описание_1',
        )
        cls.post1 = Post.objects.create(
            author=cls.auth,
            text='Тестовый_текст_1',
            group=cls.group1,
        )

    def setUp(self):
        #self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_author = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author.force_login(self.auth)

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

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        test_slug = response.context['page_obj'][0]
        index_text = test_slug.text
        self.assertEqual(index_text,'Тестовый_текст_1')
    
    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group1.slug}
            )
        )
        test_post = response.context['page_obj'][0]
        index_text = test_post.text
        self.assertEqual(index_text, 'Тестовый_текст_1')

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.post.author}
            )
        )
        test_post = response.context['page_obj'][0]
        index_text = test_post.text
        self.assertEqual(index_text, 'Тестовый_текст_1')

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}
            )
        )
        post_counted = Post.objects.filter(author=self.auth).count()
        context_fields = {
            'author':self.auth,
            'post_count': post_counted,
            'title_post': 'Пост ',
        }
        for value, expected in context_fields.items():
            with self.subTest(value=value):
                context_field = response.context[value]
                self.assertEqual(context_field, expected)

    def test_edit_post_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_author.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post1.pk}
            )
        )
        #print (self.post1.pk)
        context_fields = {
            'post_id': self.post1.pk,
            'is_edit': True,
        }
        for value, expected in context_fields.items():
            with self.subTest(value=value):
                context_field = response.context[value]
                self.assertEqual(context_field, expected)

    def test_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
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

    def test_post_exist_on_home_page(self):
        """Пост появился на главной странице."""
        response = self.authorized_author.get(reverse('posts:index'))
        test_slug = response.content[self.post1.text]
        index_text = test_slug.text
        self.assertEqual(index_text,'Тестовый_текст_1')
