from datetime import datetime, timezone, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Post, title_to_link


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

    # test if the publication date will get automatically filled in if it's empty
    def test_auto_publication_date(self):
        Post.objects.create(
            author = User.objects.create_user('tiago',
                'author@writers.com', 'pass'),
            title = "Some title, not important",
            content = "A verys short article",
            link = title_to_link("Some title, not important"),
            publication_date = None,
            tags = "test model django",
            category = "programming",
        )

        post = Post.objects.get(title='Some title, not important')
        self.assertIsNotNone(post)
        self.assertIsNotNone(post.publication_date)
