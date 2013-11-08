#! /home/mosaq/python-env/python3-django/bin/python

from django.test import LiveServerTestCase
from django.utils.unittest import skip
from selenium import webdriver

class VisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_visitor_navigates_to_the_about_page(self):
        # Ramon navigates to the page and checks its title
        self.browser.get(self.live_server_url)
        self.assertIn('Mainpage', self.browser.title)

        # Ramon searches for main navigation bar
        main_menu = self.browser.find_element_by_id('main-menu')

        # Ramon looks for a link to about page
        # clicks it
        about_link = main_menu.find_element_by_link_text('About')
        about_link.click()

        # new page loads
        # it displays placeholder page description
        document_header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('About this page', document_header.text)

    def test_user_adds_new_post(self):
        self.browser.get(self.live_server_url + '/blog')
        self.assertIn('Blog', self.browser.title)

        add_post_link = self.browser.find_element_by_link_text('New post')
        add_post_link.click()

        # new page loads
        # it displays a form
        page_body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Add new post', page_body.text)

        # Fill out the form and submit it
        post_form = self.browser.find_element_by_id('id_new_post')

        title_input = post_form.find_element_by_id('id_post_title')
        title_input.send_keys('This is an example post!')
        content_input = post_form.find_element_by_id('id_post_content')
        content_input.send_keys('Lorem ipsum woodchuck chuck out of luck.')

        post_form.find_element_by_id('submit').click()

        # main page loads
        # it displays our newly submitted post
        page_body = self.browser.find_element_by_tag_name('body')
        self.assertIn('This is an example post!', page_body.text)
        self.assertIn('Lorem ipsum woodchuck chuck out of luck.', page_body.text)

    def test_user_navigates_to_full_post_view(self):
        self.browser.get(self.live_server_url + '/blog/new-post')

        # we add new post
        post_form = self.browser.find_element_by_id('id_new_post')

        title_input = post_form.find_element_by_id('id_post_title')
        title_input.send_keys('This is an example post!')
        content_input = post_form.find_element_by_id('id_post_content')
        content_input.send_keys('Lorem ipsum woodchuck chuck out of luck.')

        post_form.find_element_by_id('submit').click()
       
        self.assertEqual(self.browser.current_url, 
                         self.live_server_url + '/blog')

        view_post_link = self.browser.find_element_by_link_text('This is an example post!')
        view_post_link.click()

        self.assertEqual(self.browser.current_url, 
                         self.live_server_url + '/blog/this-is-an-example-post')
        # user clicks on a post title or slug and displays full post contents
        self.fail('Finish the test!')