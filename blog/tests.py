from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.timezone import datetime

# session support is necessary for logging in
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog.views import blog_main, new_post, view_post
from blog.forms import AddNewPostForm
from blog.models import Post, title_to_link

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

    def test_blog_view_has_new_post_link(self):
        response = self.client.get('/blog')

        self.assertContains(response, '<a href="/blog/new-post">New post',
                status_code=200, html=True)

    def test_blog_view_can_display_posts(self):
        post = {'title': "A title", 'content': "Some content"}
        posts = [post]

        expected_html = render_to_string('blog/main.html', {'posts' : posts})

        self.assertIn(post['title'], expected_html)
        self.assertIn(post['content'], expected_html)

    def test_blog_view_can_display_saved_posts(self):
        Post.objects.create(author=self.author,
                            title='A new post title.',
                            content='Some post content here.')

        response = blog_main(HttpRequest())

        self.assertContains(response,'A new post title.')
        self.assertContains(response,'Some post content here.')

    def test_blog_view_displays_links_to_posts(self):
        Post.objects.create(author=self.author,
                            title='A new post title.',
                            content='Some post content here.',
                            link=title_to_link('A new post title.'))

        response = blog_main(HttpRequest())

        self.assertContains(response,"<a href=\"/blog/a-new-post-title/\"> \
                <h1>A new post title.</h1></a>",html=True)

class NewPostAuthenticationTest(TestCase):
    def test_cannot_post_without_logging_in(self):
        response = self.client.get('/blog/new-post')

        self.assertRedirects(response,'/login?next=/blog/new-post',status_code=302)

        # we are not logged in and should get redirected
class NewPostTest(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        # create user and log in
        User.objects.create_user('John Silver','j.silver@gmail.com','grog')
        self.user_credentials = {'username':'John Silver','password': 'grog'}
        self.user = authenticate(**self.user_credentials)
        self.request.user = self.user
        # post data for submission
        self.post_data = {
            'post_title': 'A new post title!!',
            'post_content': 'Some post content here.',
            'post_publication_date': datetime(2012,6,15,17,0,0),
            'post_tags': 'programming web',
            'post_category': 'Tutorials'
        }

    def test_new_post_url_resolves_to_new_post_view(self):
        found = resolve('/blog/new-post')

        self.assertEqual(found.func, new_post)

    def test_new_post_view_returns_correct_html(self):
        self.client.login(**self.user_credentials)
        response = self.client.get('/blog/new-post')

        # use same context as previous request
        expected_html = render_to_string('blog/new-post.html',response.context)

        self.assertEqual(response.content.decode(), expected_html)

    def test_new_post_view_inherits_from_blog_template(self):
        self.client.login(**self.user_credentials)
        response = self.client.get('/blog/new-post')

        self.assertTemplateUsed(response, 'blog/main.html')

    def test_new_post_view_returns_a_form(self):
        expected_html = render_to_string('blog/new-post.html',
                                {'form': AddNewPostForm()})

        self.assertIn('<form ', expected_html)
        self.assertIn('type="submit"', expected_html)

    def test_new_post_form_returns_correct_fields(self):
        form = AddNewPostForm()

        self.assertIn('id_post_title', form.as_p())
        self.assertIn('id_post_content', form.as_p())
        self.assertIn('id_post_publication_date', form.as_p())
        self.assertIn('id_post_tags', form.as_p())
        self.assertIn('id_post_category', form.as_p())

    def test_new_post_view_displays_POST_data(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST.update(self.post_data)

        expected_html = render_to_string('blog/new-post.html',
                            {'form' : AddNewPostForm(request.POST)})

        self.assertIn(self.post_data['post_title'], expected_html)
        self.assertIn(self.post_data['post_content'], expected_html)

    def test_new_post_view_redirects_on_submission(self):
        self.client.login(**self.user_credentials)
        response = self.client.post('/blog/new-post', self.post_data)

        # do we redirect to /blog ?
        self.assertEqual(302, response.status_code)
        self.assertRegex(response._headers.get('location')[1],
                r"^https?://[-\w]*/blog$")

    def test_new_post_view_saves_posts(self):
        self.request.method = 'POST'
        self.request.POST.update(self.post_data)

        self.assertEqual(Post.objects.all().count(), 0)
        new_post(self.request)
        self.assertEqual(Post.objects.all().count(), 1)

    def test_new_post_view_doesnt_save_empty_posts(self):
        self.request.method = 'POST'
        self.request.POST['post_title'] = ''
        self.request.POST['post_content'] = ''

        self.assertEqual(Post.objects.all().count(), 0)
        new_post(self.request)
        self.assertEqual(Post.objects.all().count(), 0)

class PostViewTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user('mrauthor',
                    'author@writers.com', 'pass')
        self.post_object = Post(title='A new post title!!',
                author = self.author,
                content = 'Some post content here.',
                link = title_to_link('A new post title!!'),
                publication_date = datetime(2012,6,15,17,0,0),
                tags = 'programming web',
                category = 'tutorials'
        )

    def test_post_is_assigned_a_link_name(self):
        self.post_object.save()

        post = Post.objects.all()[0]
        self.assertEqual(post.link, 'a-new-post-title')

    def test_post_url_resolves_to_post_view(self):
        self.post_object.save()

        found = resolve('/blog/%s/' % self.post_object.link)

        self.assertEqual(found.func, view_post)

    def test_blog_url_returns_correct_html(self):
        self.post_object.save()

        request = HttpRequest()
        response = view_post(request, self.post_object.link)

        expected_html = render_to_string('blog/view-post.html', {'post': self.post_object})
        self.assertEqual(response.content.decode(), expected_html)

    def test_post_view_inherits_view_template(self):
        self.post_object.save()

        response = self.client.get('/blog/a-new-post-title/')
        self.assertTemplateUsed(response, 'blog/main.html')

    def test_post_has_an_individual_link(self):
        self.post_object.save()

        response = self.client.get('/blog/a-new-post-title/')
        self.assertIn('A new post title!!', response.content.decode())

    def test_post_displays_publication_date(self):
        self.post_object.save()

        response = self.client.get('/blog/a-new-post-title/')
        self.assertIn('2012', response.content.decode())

class NewPostFormTest(TestCase):
    def setUp(self):
        self.post_data = {
            'post_title': 'A new post title!!',
            'post_content': 'Some post content here.',
            'post_publication_date': datetime(2012,6,15,17,0,0),
            'post_tags': 'programming web',
            'post_category': 'Tutorials'
        }

    def test_validation(self):
        form = AddNewPostForm(self.post_data)
        #self.assertEqual(True,form.is_valid())
        
        form.is_valid()
        self.assertEqual(True,{}==form.errors)
