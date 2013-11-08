from django.db import models
import re

class Post(models.Model):
    title = models.CharField(max_length=512)
    content = models.TextField()
    link = models.CharField(max_length=512)

def title_to_link(title):
    #to lowercase
    title = title.lower()
    # continuous whitespace to dash
    title = re.sub(r"\s+","-",title)
    # strip all characters except aplhanum & dashes
    title = re.sub(r"[^a-z-]+","",title)
    return title

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

    def test_can_transform_title_into_link(self):
        self.assertEqual("some-link", title_to_link("Some link!"))
