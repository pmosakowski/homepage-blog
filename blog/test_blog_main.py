from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils import timezone as dtz

from django.contrib.auth.models import User

from .views import blog_main
from .models import Post, title_to_link

class BlogTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user('mrauthor',
                'author@writers.com', 'pass')

    def test_blog_url_resolves_to_blog_view(self):
        found = resolve('/blog')

        self.assertEqual(found.func, blog_main)

    def test_blog_url_returns_correct_html(self):
        request = HttpRequest()
        response = blog_main(request)

        expected_html = render_to_string('blog/main.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_blog_view_inherits_from_base_template(self):
        response = self.client.get('/blog')

        self.assertTemplateUsed(response, 'mainpage/base.html')

    def test_blog_view_uses_post_template(self):
        # need to add a post otherwise the template won't be used
        Post.objects.create(author=self.author,
                            title='A new post title.',
                            content='Some post content here.',
                            publish=True,
        )
        response = self.client.get('/blog')

        self.assertTemplateUsed(response, 'blog/post.html')

    def test_blog_view_has_new_post_link(self):
        response = self.client.get('/blog')

        self.assertContains(response, '<a href="/blog/new-post">New post',
                status_code=200, html=True)

    def test_blog_view_can_display_posts(self):
        post = {
                'title': "A title", 
                'content': "Some content",
                'publication_date': dtz.datetime(2015,3,15,15,20,0),
                'author': {'first_name':'James','last_name':'Brown'},
                'category': 'No pain, no gain',
        }
        posts = [post]

        expected_html = render_to_string('blog/main.html', {'posts' : posts})

        self.assertIn(post['title'], expected_html)
        self.assertIn(post['content'], expected_html)
        self.assertIn(post['publication_date'].strftime('%Y-%m-%d'), expected_html)
        self.assertIn(post['author']['first_name'], expected_html)
        self.assertIn(post['author']['last_name'], expected_html)
        self.assertIn(post['category'], expected_html)

    def test_blog_view_doesnt_display_unpublished_posts(self):
        Post.objects.create(author=self.author,
                            title='A new post title.',
                            content='Some post content here.',
                            category='Some category',
                            publication_date=dtz.now(),
                            publish=False,
        )

        response = blog_main(HttpRequest())

        self.assertNotContains(response, 'A new post title')

    def test_blog_view_doesnt_display_future_published_posts(self):
        Post.objects.create(author=self.author,
                            title='A new post title.',
                            content='Some post content here.',
                            category='Some category',
                            publication_date=(dtz.now() + dtz.timedelta(days=1)),
                            publish=True,
        )

        response = blog_main(HttpRequest())

        self.assertNotContains(response, 'A new post title')

    def test_blog_view_can_display_saved_posts(self):
        Post.objects.create(author=self.author,
                            title='A new post title.',
                            content='Some post content here.',
                            category='Some category',
                            publish=True,
        )

        response = blog_main(HttpRequest())

        self.assertContains(response,'A new post title.')
        self.assertContains(response,'Some post content here.')
        self.assertContains(response,'Some category')

    def test_blog_view_displays_links_to_posts(self):
        Post.objects.create(author=self.author,
                            title='A new post title.',
                            content='Some post content here.',
                            link=title_to_link('A new post title.'),
                            publish=True,
        )

        response = blog_main(HttpRequest())

        self.assertContains(response,"<a href=\"/blog/a-new-post-title/\"> \
                <h1>A new post title.</h1></a>",html=True)
