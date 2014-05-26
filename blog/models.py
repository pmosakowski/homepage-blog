from datetime import datetime, timezone, timedelta

from django.db import models
from django.contrib.auth.models import User
import re

class Post(models.Model):
    author = models.ForeignKey(User)

    title = models.CharField(max_length=512)
    content = models.TextField()
    link = models.CharField(max_length=512)

    submission_date = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField()
    modification_date = models.DateTimeField(auto_now=True)

    tags = models.CharField(max_length=512)
    category = models.CharField(max_length=512)

def title_to_link(title):
    #to lowercase
    title = title.lower()
    # strip quotes
    title = re.sub(r"['\"]+","",title)
    # convert all characters except aplhanum to dashes
    title = re.sub(r"[^a-z0-9]+","-",title)
    # remove dashes at beginning and end
    title = re.sub(r"^-+|-+$","",title)
    # remove double dashes
    title = re.sub(r"--+","-",title)
    # continuous whitespace to dash
    title = re.sub(r"\s+","-",title)
    return title

# model tests go here
from django.test import TestCase

class PostModelTest(TestCase):
    def setUp(self):
        self.post1 = Post()
        self.post1.author = User.objects.create_user('mrauthor',
                'author@writers.com', 'pass')
        self.post1.title = "A post title"
        self.post1.content = "Some content"
        self.post1.link = "a-post-title"
        self.post1.publication_date = datetime.now(timezone(timedelta()))

        self.post1.tags = "programming linux"
        self.post1.category = "Tutorial"

    def test_can_save_post_models(self):

        self.assertEqual(Post.objects.all().count(), 0)
        self.post1.full_clean()
        self.post1.save()
        self.assertEqual(Post.objects.all().count(), 1)

    def test_can_retrieve_post_models(self):

        self.post1.full_clean()
        self.post1.save()
        posts = Post.objects.all()

        self.assertIn("A post title", (post.title for post in posts))
        self.assertIn("Some content", (post.content for post in posts))

    def test_can_transform_title_into_link(self):
        self.assertEqual("some-link", title_to_link("Some link!"))
        self.assertEqual("other-link", title_to_link("-other Link!-"))
        self.assertEqual("some-link", title_to_link("Some--link!&"))
        self.assertEqual("link-number-four",
                title_to_link("Link-number Four."))
        self.assertEqual("fifth-link", title_to_link("fifth link!--"))
        self.assertEqual("first-second-thing-link",
                title_to_link("First & second thing link!"))
        self.assertEqual("this-is-the-6th-link-on-our-page",
                title_to_link("This is the 6th link on our page."))
        self.assertEqual("link-to-our-womens-mens-football-circles",
                title_to_link("Link to our Women's & Men's football circles?"))
        self.assertEqual("these-toys-arent-boys",
                title_to_link("These toys aren't boys'."))
        self.assertEqual("we-will-never-forget-says-pm",
                title_to_link("'We will never forget' - says PM."))
