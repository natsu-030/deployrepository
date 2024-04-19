from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Like

# Create your tests here.
class DiaryIntegrationTests(TestCase):
    def setUp(self):
        # ユーザーを作成
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.client.login(username='testuser', password='12345')

        # 投稿を作成
        self.post = Post.objects.create(
            user=self.user,
            title='Test Post',
            efforts='Test Efforts',
            encouragement='Keep going!',
            is_public=True
        )

    def test_post_creation_and_retrieval(self):
        # 投稿作成ページへのアクセス
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)

        # 新しい投稿を作成
        response = self.client.post(reverse('post_new'), {
            'title': 'Another Test Post',
            'efforts': 'More Efforts',
            'encouragement': 'You can do it!',
            'is_public': True
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(title='Another Test Post').exists())

        # 投稿リストページの確認
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Another Test Post', response.content.decode())

    def test_like_post_functionality(self):
        # 投稿へのいいね
        response = self.client.post(reverse('toggle_like', args=[self.post.id]), follow=True)
        self.assertTrue(Like.objects.filter(post=self.post, user=self.user).exists())

        # いいねを削除
        response = self.client.post(reverse('toggle_like', args=[self.post.id]), follow=True)
        self.assertFalse(Like.objects.filter(post=self.post, user=self.user).exists())

    def test_post_deletion(self):
        # 投稿を削除
        post_id = self.post.id
        response = self.client.post(reverse('post_delete', args=[post_id]), follow=True)
        self.assertFalse(Post.objects.filter(id=post_id).exists())
