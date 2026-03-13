from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post, Comment


class PostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_hacker', password='password123')
        self.another_user = User.objects.create_user(username='thief', password='password123')
        self.post = Post.objects.create(title='Test', text='Text', author=self.user)

    def test_get_posts_list(self):
        """1. Проверка получения списка постов"""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Post.objects.count())

    def test_create_post_authenticated(self):
        """2. Проверка создания поста авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        initial_count = Post.objects.count()
        response = self.client.post('/api/posts/', {'title': 'New', 'text': 'Text'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), initial_count + 1)

    def test_create_post_unauthenticated(self):
        """3. Проверка защиты: аноним НЕ должен создать пост"""
        initial_count = Post.objects.count()
        response = self.client.post('/api/posts/', {'title': 'New', 'text': 'Text'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), initial_count)

    def test_lightweight_method(self):
        """4. Проверка легковесной ручки"""
        response = self.client.get('/api/posts/lightweight/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_item = response.data[0]
        if isinstance(first_item, dict):
            self.assertIn('title', first_item)
            self.assertNotIn('text', first_item)
        else:
            self.assertEqual(len(first_item), 2)

    def test_post_like(self):
        """5. Проверка экшена лайка"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'liked')

    def test_get_single_post(self):
        """6. Получение одного конкретного поста по ID"""
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test')

    def test_update_post_by_author(self):
        """7. Автор может редактировать свой пост (PATCH)"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/posts/{self.post.id}/', {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_update_post_by_another_user(self):
        """8. Чужой юзер получает ошибку 403 при попытке редактирования"""
        self.client.force_authenticate(user=self.another_user)
        response = self.client.patch(f'/api/posts/{self.post.id}/', {'title': 'Hacked Title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_by_author(self):
        """9. Автор может удалить свой пост"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_post_unlike(self):
        """10. Повторный клик снимает лайк (unliked)"""
        self.client.force_authenticate(user=self.user)
        self.client.post(f'/api/posts/{self.post.id}/like/')
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'unliked')


class CommentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='comment_user', password='password123')
        self.another_user = User.objects.create_user(username='comment_thief', password='password123')
        self.post = Post.objects.create(title='Post for Comment', text='Text', author=self.user)
        self.comment = Comment.objects.create(post=self.post, author=self.user, text='First comment')

    def test_create_comment_authenticated(self):
        """11. Создание комментария авторизованным юзером"""
        self.client.force_authenticate(user=self.user)
        initial_count = Comment.objects.count()
        response = self.client.post('/api/comments/', {'text': 'New', 'post_id': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), initial_count + 1)

    def test_create_comment_unauthenticated(self):
        """12. Аноним не может создать комментарий"""
        initial_count = Comment.objects.count()
        response = self.client.post('/api/comments/', {'text': 'Hacker', 'post_id': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), initial_count)

    def test_comment_like(self):
        """13. Проверка лайка на комментарий"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/comments/{self.comment.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'liked')

    def test_delete_comment_by_another_user(self):
        """14. Чужой юзер получает ошибку 403 при удалении чужого комментария"""
        self.client.force_authenticate(user=self.another_user)
        response = self.client.delete(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_tester', password='password123')

    def test_names_only_method(self):
        """15. Легковесная ручка пользователей"""
        response = self.client.get('/api/users/names_only/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_item = response.data[0]
        if isinstance(first_item, dict):
            self.assertIn('username', first_item)
            self.assertNotIn('password', first_item)
        else:
            self.assertEqual(len(first_item), 2)