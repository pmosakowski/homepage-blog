from django.test import TestCase
import re

from django.core.urlresolvers import resolve
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

class NewPostTest(TestCase):

    def test_new_post_url_resolves_to_new_post_view(self):
        found = resolve('/blog/new-post')

        self.assertEqual(found.func, new_post)

    def test_new_post_view_returns_correct_html(self):
        response = self.client.get('/blog/new-post')
       
        form = AddNewPostForm()
        expected_html = render_to_string('blog/new-post.html', {'form': form})
        self.assertEqual(response.content.decode(), expected_html)

    def test_new_post_view_inherits_from_blog_template(self):
        response = self.client.get('/blog/new-post')
        
        self.assertTemplateUsed(response, 'blog/main.html')

    def test_new_post_view_returns_a_form(self):
        response = self.client.get('/blog/new-post')
        
        self.assertContains(response, '<form ',
                status_code=200)


    def test_new_post_form_returns_correct_fields(self):
        form = AddNewPostForm()

        title = re.compile('.*id_post_title.*')
        contents = re.compile('.*id_post_content.*')
        
        self.assertRegex(form.as_p(),title)
        self.assertRegex(form.as_p(),contents)
#    def test_new_post_view_can_process_submissions(self):

