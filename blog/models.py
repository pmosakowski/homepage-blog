from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=512)
    content = models.TextField()

# model tests go here
from django.test import TestCase

class PostModelTest(TestCase):
    def setUp(self):
        self.post1 = Post()
        self.post1.title = "A post title"
        self.post1.content = "Some content"

    def test_can_save_post_models(self):

        self.assertEqual(Post.objects.all().count(), 0)

        self.post1.save()

        self.assertEqual(Post.objects.all().count(), 1)

    def test_can_retrieve_post_models(self):

        self.post1.save()
        posts = Post.objects.all()

        self.assertIn("A post title", (post.title for post in posts))
        self.assertIn("Some content", (post.content for post in posts))
