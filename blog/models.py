from django.db import models

class Post(models.Model):
    pass


# model tests go here
from django.test import TestCase

class PostModelTest(TestCase):
    def setUp(self):
        self.post1 = Post()
        self.post1.title = "A post title"
        self.post1.content = "Some content"

    def test_can_save_post_models(self):

        self.assertEqual(len(Post.objects.all()), 0)

        self.post1.save()

        self.assertEqual(len(Post.objects.all()), 1)


