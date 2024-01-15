from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from social_network.core.models import Post, PostLike

class PostRelatedViewTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        self.post = Post.objects.create(body="Test body", title= "test title", author_id=user.id)
        self.post_id = str(self.post.id)

    def test_get_posts(self):
        url = reverse('posts')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post_id, response.json()[0]["id"])

    def test_create_post(self):
        url = reverse('posts')
        data = {
            "body": "Test from new user",
            "title": "test"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_post_without_body(self):
        url = reverse('posts')
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_and_dislike_post(self):
        """
        Tests likes and dislikes endpoints at the same time
        """
        like_url = reverse('post_likes', kwargs={"post_id":self.post_id})
        dislike_url = reverse('post_dislikes', kwargs={"post_id":self.post_id})

        # like the post to be able to dislike it later
        response = self.client.post(like_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check that both tables got updated
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.likes_number, 1)

        post_like = PostLike.objects.get(post_id=self.post.id)
        self.assertIsNotNone(post_like)

        # dislike the post
        response = self.client.delete(dislike_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check that both tables got updated
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.likes_number, 0)

        post_like = PostLike.objects.filter(post_id=self.post.id)
        self.assertEqual(post_like.count(), 0)

    def test_invalid_dislike__never_liked_post(self):
        url = reverse('post_dislikes', kwargs={"post_id":self.post_id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


