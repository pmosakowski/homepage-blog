#! /home/mosaq/python-env/python3-django/bin/python

from selenium import webdriver
import unittest

class VisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_visitor_navigates_to_the_about_page(self):
        # Ramon navigates to the page and checks its title
        self.browser.get('http://localhost:8000')
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
        self.browser.get('http://localhost:8000/blog')
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
        self.assertIn('This is an example post!t', page_body.text)
        self.assertIn('Lorem ipsum woodchuck chuck out of luck.', page_body.text)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
