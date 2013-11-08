from django.test import TestCase
import re

from django.core.urlresolvers import resolve
from django.core.context_processors import csrf

from django.http import HttpRequest
from django.template.loader import render_to_string

from blog.views import blog_main, new_post, view_post
from blog.forms import AddNewPostForm
from blog.models import Post, title_to_link

class BlogTest(TestCase):

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
        Post.objects.create(title='A new post title.',
                            content='Some post content here.')

        response = blog_main(HttpRequest())
        
        self.assertContains(response,'A new post title.')
        self.assertContains(response,'Some post content here.')


class NewPostTest(TestCase):
    def setUp(self):
        self.post_data = {
            'post_title': 'A new post title!!',
            'post_content': 'Some post content here.'
        }

    def test_new_post_url_resolves_to_new_post_view(self):
        found = resolve('/blog/new-post')

        self.assertEqual(found.func, new_post)

    def test_new_post_view_returns_correct_html(self):
        response = self.client.get('/blog/new-post')

        # use same context as previous request
        expected_html = render_to_string('blog/new-post.html',response.context)

        self.assertEqual(response.content.decode(), expected_html)

    def test_new_post_view_inherits_from_blog_template(self):
        response = self.client.get('/blog/new-post')
        
        self.assertTemplateUsed(response, 'blog/main.html')

    def test_new_post_view_returns_a_form(self):
        expected_html = render_to_string('blog/new-post.html', 
                                {'form': AddNewPostForm()})
        
        self.assertIn('<form ', expected_html)
        self.assertIn('type="submit"', expected_html)

    def test_new_post_form_returns_correct_fields(self):
        form = AddNewPostForm()
        
        self.assertIn('id_post_title',form.as_p())
        self.assertIn('id_post_content',form.as_p())

    def test_new_post_view_displays_POST_data(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST.update(self.post_data)

        expected_html = render_to_string('blog/new-post.html',
                            {'form' : AddNewPostForm(request.POST)})

        self.assertIn(self.post_data['post_title'], expected_html)
        self.assertIn(self.post_data['post_content'], expected_html)
   
    def test_new_post_view_redirects_on_submission(self):
        
        response = self.client.post('/blog/new-post', self.post_data)
        
        # do we redirect to /blog ?
        self.assertEqual(302, response.status_code)
        self.assertRegex(response._headers.get('location')[1],
                r"^https?://[-\w]*/blog$")

    def test_new_post_view_saves_posts(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST.update(self.post_data)
        
        self.assertEqual(Post.objects.all().count(), 0)
        new_post(request)
        self.assertEqual(Post.objects.all().count(), 1)

    def test_new_post_view_doesnt_save_empty_posts(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title'] = ''
        request.POST['post_content'] = ''

        self.assertEqual(Post.objects.all().count(), 0)
        new_post(request)
        self.assertEqual(Post.objects.all().count(), 0)

class PostViewTest(TestCase):
    def setUp(self):
        self.post_data = {
            'post_title': 'A new post title!!',
            'post_content': 'Some post content here.'
        }
        
        self.post_object = Post(title=self.post_data['post_title'],
                content=self.post_data['post_content'],
                link=title_to_link(self.post_data['post_title']))


    def test_post_is_assigned_a_link_name(self):
        self.post_object.save()        

        post = Post.objects.all()[0]
        self.assertEqual(post.link, 'a-new-post-title')

    def test_post_url_resolves_to_post_view(self):
        self.post_object.save()

        found = resolve('/blog/%s/' % self.post_object.link)

        self.assertEqual(found.func, view_post)

    def test_blog_url_returns_correct_html(self):
        post = {'title': 'Some link!', 'content': 'Some content.','link':
                title_to_link('Some link!')}
        Post.objects.create(**post)

        request = HttpRequest() 
        response = view_post(request,title_to_link('Some link!')) 

        expected_html = render_to_string('blog/view-post.html', {'post':post})
        self.assertEqual(response.content.decode(), expected_html)

    def test_post_view_inherits_view_template(self):
        self.post_object.save()

        response = self.client.get('/blog/a-new-post-title/')
        self.assertTemplateUsed(response, 'blog/main.html')

    def test_post_has_an_individual_link(self):
        self.post_object.save()

        response = self.client.get('/blog/a-new-post-title/')
        self.assertIn('A new post title!!', response.content.decode())
