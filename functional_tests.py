#! /home/mosaq/python-env/python3-django/bin/python

from selenium import webdriver
import unittest

class VisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_visitor_reads_an_about_page(self):
        # Ramon navigates to the page and checks its title
        self.browser.get('http://localhost:8000')
        self.assertIn('Homepage', self.browser.title)

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
        
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
