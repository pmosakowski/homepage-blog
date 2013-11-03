from django.test import TestCase
import re

from django.core.urlresolvers import resolve
from django.core.context_processors import csrf

from django.http import HttpRequest
from django.template.loader import render_to_string

from blog.views import blog_main, new_post
from blog.forms import AddNewPostForm

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

    def test_blog_view_displays_post(self):
        post = {'title': "A title", 'content': "Some content"}
        posts = [post]

        expected_html = render_to_string('blog/main.html', {'posts' : posts})

        self.assertIn(post['title'], expected_html)
        self.assertIn(post['content'], expected_html)

class NewPostTest(TestCase):

    def test_new_post_url_resolves_to_new_post_view(self):
        found = resolve('/blog/new-post')

        self.assertEqual(found.func, new_post)

    def test_new_post_view_returns_correct_html(self):
        response = self.client.get('/blog/new-post')

        # use same context as previous request
        expected_html = render_to_string('blog/new-post.html',response.context)

        self.assertEqual(response.content.decode(), expected_html)
        self.assertIn('type="submit"', expected_html)

    def test_new_post_view_inherits_from_blog_template(self):
        response = self.client.get('/blog/new-post')
        
        self.assertTemplateUsed(response, 'blog/main.html')

    def test_new_post_view_returns_a_form(self):
        response = self.client.get('/blog/new-post')
        
        self.assertContains(response, '<form ',
                status_code=200)


    def test_new_post_form_returns_correct_fields(self):
        form = AddNewPostForm()
        
        self.assertIn('id_post_title',form.as_p())
        self.assertIn('id_post_content',form.as_p())

    def test_new_post_view_displays_POST_data(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title'] = 'A new post title'
        request.POST['post_content'] = 'Some post content here.'

        expected_html = render_to_string('blog/new-post.html',
                            {'form' : AddNewPostForm(request.POST)})

        self.assertIn('A new post title', expected_html)
        self.assertIn('Some post content here.', expected_html)
    
    def test_new_post_view_can_process_submissions(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title'] = 'A new post title'
        request.POST['post_content'] = 'Some post content here.'

        response = new_post(request)

        post = {'title': "A title", 'content': "Some content"}
        posts = [post]

        expected_html = render_to_string('blog/main.html', {'posts': posts})

        self.assertEqual(response.content.decode(), expected_html)
