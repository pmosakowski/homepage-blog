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

        self.fail('Finish the test!')

        # Ramon searches for main navigation bar

        # Ramon looks for a link to about page
        # clicks it

        # new page loads
        # it displays placeholder page descritption

if __name__ == '__main__':
    unittest.main(warnings='ignore')
