import django.utils.timezone as dtz;
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Post, Category, title_to_link

class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category(
                name = 'Tutorial'
        )

        self.post1 = Post()
        self.post1.author = User.objects.create_user('mrauthor',
                'author@writers.com', 'pass')
        self.post1.title = "A post title"
        self.post1.content = "Some content"
        self.post1.link = "a-post-title"
        self.post1.publication_date = dtz.now()

        self.post1.tags = "programming linux"

    def test_can_save_post_models(self):
        # no posts or categories in the database
        self.assertEqual(Post.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

        self.post1.category = Category.get('Tutorial')
        self.post1.full_clean()
        self.post1.save()
        # was new post created
        self.assertEqual(Post.objects.all().count(), 1)
        # was new category created
        self.assertEqual(Category.objects.all().count(), 1)

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

    # if post is set to be published the publication date will get automatically filled in if it's empty
    def test_auto_publication_date(self):
        Post.objects.create(
            author = User.objects.create_user('tiago',
                'author@writers.com', 'pass'),
            title = "Some title, not important",
            content = "A verys short article",
            link = title_to_link("Some title, not important"),
            publication_date = None,
            publish = True,
            tags = "test model django",
            category = Category.get("programming"),
        )

        post = Post.objects.get(title='Some title, not important')
        self.assertIsNotNone(post)
        self.assertIsNotNone(post.publication_date)
    
    # if post isn't set to be published the publication date will remain empty
    def test_no_auto_publication_date(self):
        Post.objects.create(
            author = User.objects.create_user('tiago',
                'author@writers.com', 'pass'),
            title = "Some title, not important",
            content = "A verys short article",
            link = title_to_link("Some title, not important"),
            publication_date = None,
            publish = False,
            tags = "test model django",
            category = Category.get("programming"),
        )

        post = Post.objects.get(title='Some title, not important')
        self.assertIsNotNone(post)
        self.assertIsNone(post.publication_date)

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category(
                name = 'Random',
        )

    def test_can_save_category_models(self):
        self.assertEquals(0, Category.objects.all().count())
        self.category.save()
        self.assertEquals(1, Category.objects.all().count())

    def test_retrieve_instead_of_duplicating_categories(self):
        self.assertEquals(0, Category.objects.all().count())

        cat1 = Category.get('Tutorial')
        self.assertEquals(1, Category.objects.all().count())

        cat2 = Category.get('Programming')
        self.assertEquals(2, Category.objects.all().count())

        cat1 = Category.get('Tutorial')
        self.assertEquals(2, Category.objects.all().count())
