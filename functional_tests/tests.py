from time import sleep

from django.test import LiveServerTestCase
from selenium import webdriver

import django.utils.timezone as dtz


from django.contrib.auth.models import User

class VisitorTest(LiveServerTestCase):

    def setUp(self):
        self.profile = webdriver.FirefoxProfile()
        self.firefox_esr_binary = webdriver.firefox.firefox_binary.FirefoxBinary(firefox_path="/usr/bin/firefox-esr")
        self.browser = webdriver.Firefox(firefox_profile=self.profile,firefox_binary=self.firefox_esr_binary)
        self.browser.implicitly_wait(3)

        # create user that will receive our message
        User.objects.create_user('contact', 'contact@example.com','password1', first_name='Mister', last_name='Contact')

    def tearDown(self):
        self.browser.quit()

    # about page
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
        heading = self.browser.find_element_by_xpath("//div[@id='content']/h1")
        self.assertIn('About this page', heading.text)

    def test_visitor_uses_contact_page(self):
        # Ramon navigates to the page and checks its title
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Contact').click()

        self.assertIn('Contact', self.browser.title)

        # fill out the form
        page_body = self.browser.find_element_by_tag_name('body')
        page_body.find_element_by_id('id_subject').\
                send_keys('message subject')
        page_body.find_element_by_id('id_message').\
                send_keys('message body')
        page_body.find_element_by_id('id_contact_email').\
                send_keys('carebear@example.com')
        page_body.find_element_by_id('id_submit').click()

        # check redirect on success
        self.assertEqual(self.live_server_url + '/contact/thanks', self.browser.current_url)
        self.assertIn('Thank you', self.browser.title)

class LoggedUserTest(LiveServerTestCase):

    def setUp(self):
        self.profile = webdriver.FirefoxProfile()
        self.firefox_esr_binary = webdriver.firefox.firefox_binary.FirefoxBinary(firefox_path="/usr/bin/firefox-esr")
        self.browser = webdriver.Firefox(firefox_profile=self.profile,firefox_binary=self.firefox_esr_binary)
        self.browser.implicitly_wait(3)
        user = User.objects.create_user('Shiba Inu', 'doge@kennel.jp','kibbles', first_name='Shiba', last_name='Inu')

        # user navigates to the login page
        self.browser.get(self.live_server_url + '/login')

        # submits his credentials
        self.browser.find_element_by_id('id_username').send_keys('Shiba Inu')
        self.browser.find_element_by_id('id_password').send_keys('kibbles')
        self.browser.find_element_by_id('id_submit').click()
    def tearDown(self):
        self.browser.quit()

    # adding new posts
    def test_user_adds_new_post(self):
        self.browser.get(self.live_server_url + '/blog')
        self.assertIn('Blog', self.browser.title)

        # categories are displayed, they will be empty now
        category_list = self.browser.find_elements_by_id('categories')
        self.assertEqual(1, len(category_list))
        categories = category_list[0].find_elements_by_class_name('category')
        self.assertEqual(0, len(categories))

        add_post_link = self.browser.find_element_by_link_text('New post')
        add_post_link.click()

        # new page loads
        # it displays a form
        page_body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Add new post', page_body.text)

        # Fill out the form and submit it
        post_form = self.browser.find_element_by_id('id_new_post')

        post_form.find_element_by_id('id_post_title')\
                .send_keys('This is an example post!')
        post_form.find_element_by_id('id_post_content')\
                .send_keys('Lorem ipsum woodchuck chuck out of luck.')
        post_form.find_element_by_id('id_post_category')\
                .send_keys('Programming')
        
        # select 'publish' checkbox if it's not selected
        publish_checkbox = post_form.find_element_by_id('id_post_publish')
        if not publish_checkbox.is_selected():
            publish_checkbox.click()

        post_form.find_element_by_id('id_submit').click()

        # main page loads
        # it displays our newly submitted post
        page_body = self.browser.find_element_by_tag_name('body')
        self.assertIn('This is an example post!', page_body.text)
        self.assertIn('Lorem ipsum woodchuck chuck out of luck.', page_body.text)

        # post categories are visible
        categories = self.browser.find_element_by_id('categories')
        # category link present
        category = categories.find_elements_by_link_text('Programming')
        self.assertEquals(1, len(category))
        # check category link url
        category_url = category[0].get_attribute("href")
        self.assertIn("/blog/category/programming/", category_url)

    # individual post views and direct links
    def test_user_adds_post_and_navigates_to_full_post_view(self):
        self.browser.get(self.live_server_url + '/blog/new-post')

        # we add new post
        post_form = self.browser.find_element_by_id('id_new_post')

        post_form.find_element_by_id('id_post_title')\
                .send_keys('This is an example post!')
        post_form.find_element_by_id('id_post_content')\
                .send_keys('Lorem ipsum woodchuck chuck out of luck. *boo!* **ah?**')

        # select 'publish' checkbox if it's not selected
        publish_checkbox = post_form.find_element_by_id('id_post_publish')
        if not publish_checkbox.is_selected():
            publish_checkbox.click()

        post_form.find_element_by_id('id_submit').click()
       
        self.assertEqual(self.browser.current_url, 
                         self.live_server_url + '/blog')

        # user clicks on a post title or slug and displays full post contents
        view_post_link = self.browser.find_element_by_link_text('This is an example post!')
        view_post_link.click()

        self.assertNotIn('Not Found', self.browser.page_source)
        self.assertEqual(self.browser.current_url, 
                         self.live_server_url + '/blog/post/this-is-an-example-post/')

        page_body = self.browser.find_element_by_tag_name('body')
        self.assertIn('This is an example post!', page_body.text)
        self.assertIn('Lorem ipsum woodchuck chuck out of luck.', page_body.text)
        # check if post content uses markdown
        self.assertIn('<em>boo!</em>', self.browser.page_source)
        self.assertIn('<strong>ah?</strong>', self.browser.page_source)


    def test_user_adds_posts_and_examines_extended_attributes(self):
        self.browser.get(self.live_server_url + '/blog/new-post')
        # we add new post
        post_form = self.browser.find_element_by_id('id_new_post')

        title_input = post_form.find_element_by_id('id_post_title')
        title_input.send_keys('I didn\'t ask for this!')
        content_input = post_form.find_element_by_id('id_post_content')
        content_input.send_keys('Adam Jensen didn\'t ask for this.')
        # author should be set by the view
        # submitted date should be set by the view
        # set publish date
        publish_date_input = post_form.find_element_by_id('id_post_publication_date')
        now = dtz.now().strftime('%Y-%m-%d %H:%M:%S')
        publish_date_input.send_keys(now)
        post_form.find_element_by_id('id_post_publish').click()
        # set category 
        category_input = post_form.find_element_by_id('id_post_category')
        category_input.send_keys('Life stories')
        # add tags
        tag_input = post_form.find_element_by_id('id_post_tags')
        tag_input.send_keys('oopsies desuex yolo')
        # submit
        post_form.find_element_by_id('id_submit').click()

        self.browser.find_element_by_link_text('I didn\'t ask for this!').click()
        self.assertNotIn('Not Found', self.browser.page_source)
        page_body = self.browser.find_element_by_tag_name('body')

        self.assertIn('I didn\'t ask for this!', page_body.text)
        self.assertIn('published Today', page_body.text)
        self.assertIn('by Shiba Inu', page_body.text)
        self.assertIn('in Life stories', page_body.text)
        self.assertIn('Tags: oopsies desuex yolo', page_body.text)

    def test_user_adds_unpublished_post(self):
        self.browser.get(self.live_server_url + '/blog/new-post')
        # we add new post
        post_form = self.browser.find_element_by_id('id_new_post')

        title_input = post_form.find_element_by_id('id_post_title')
        title_input.send_keys('I didn\'t ask for this!')
        content_input = post_form.find_element_by_id('id_post_content')
        content_input.send_keys('Adam Jensen didn\'t ask for this.')

        # author should be set by the view
        # submitted date should be set by the view
        # set publish date
        publish_date_input = post_form.find_element_by_id('id_post_publication_date')
        now = dtz.now().strftime('%Y-%m-%d %H:%M:%S')
        publish_date_input.send_keys(now)

        # deselect 'publish' checkbox if it's selected
        publish_checkbox = post_form.find_element_by_id('id_post_publish')
        if publish_checkbox.is_selected():
            publish_checkbox.click()

        # set category
        category_input = post_form.find_element_by_id('id_post_category')
        category_input.send_keys('Life stories')

        # add tags
        tag_input = post_form.find_element_by_id('id_post_tags')
        tag_input.send_keys('oopsies desuex yolo')

        # submit
        post_form.find_element_by_id('id_submit').click()

        self.browser.get(self.live_server_url + '/blog')
        page_body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('I didn\'t ask for this!', page_body.text)

    def test_user_adds_post_with_tomorrow_publication_date(self):
        self.browser.get(self.live_server_url + '/blog/new-post')
        # we add new post
        post_form = self.browser.find_element_by_id('id_new_post')

        title_input = post_form.find_element_by_id('id_post_title')
        title_input.send_keys('I didn\'t ask for this!')
        content_input = post_form.find_element_by_id('id_post_content')
        content_input.send_keys('Adam Jensen didn\'t ask for this.')

        # author should be set by the view
        # submitted date should be set by the view
        # set publish date
        publish_date_input = post_form.find_element_by_id('id_post_publication_date')
        now = dtz.now()
        next_day = dtz.timedelta(days=1)
        tomorrow = (now + next_day).strftime('%Y-%m-%d %H:%M:%S')
        publish_date_input.send_keys(tomorrow)

        # select 'publish' checkbox
        publish_checkbox = post_form.find_element_by_id('id_post_publish')
        if not publish_checkbox.is_selected():
            publish_checkbox.click()

        # set category
        category_input = post_form.find_element_by_id('id_post_category')
        category_input.send_keys('Life stories')

        # add tags
        tag_input = post_form.find_element_by_id('id_post_tags')
        tag_input.send_keys('oopsies desuex yolo')

        # submit
        post_form.find_element_by_id('id_submit').click()

        self.browser.get(self.live_server_url + '/blog')
        page_body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('I didn\'t ask for this!', page_body.text)

class UserTest(LiveServerTestCase):

    def setUp(self):
        self.profile = webdriver.FirefoxProfile()
        self.firefox_esr_binary = webdriver.firefox.firefox_binary.FirefoxBinary(firefox_path="/usr/bin/firefox-esr")
        self.browser = webdriver.Firefox(firefox_profile=self.profile,firefox_binary=self.firefox_esr_binary)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
    # authentication features
    def test_user_logs_in_adds_a_post_and_logs_out(self):
        user = User.objects.create_user('Juan Ramirez', 'juan@mexicocity.mx','tequila')

        # user navigates to the login page
        self.browser.get(self.live_server_url + '/')
        self.browser.find_element_by_link_text('Log in').click()

        # submits his credentials
        self.browser.find_element_by_id('id_username').send_keys('Juan Ramirez')
        self.browser.find_element_by_id('id_password').send_keys('tequila')
        self.browser.find_element_by_id('id_submit').click()

        # when he's logged in he can see his name on the page
        page_body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Juan Ramirez', page_body.text)
        
        # Juan navigates to submit new post
        self.browser.get(self.live_server_url + '/blog/new-post')

        # Juan fills out the form and adds new post
        post_form = self.browser.find_element_by_id('id_new_post')

        title_input = post_form.find_element_by_id('id_post_title')
        title_input.send_keys('Juan\'s first post!')
        content_input = post_form.find_element_by_id('id_post_content')
        content_input.send_keys('Juan has a few words to say.')

        # select 'publish' checkbox if it's not selected
        publish_checkbox = post_form.find_element_by_id('id_post_publish')
        if not publish_checkbox.is_selected():
            publish_checkbox.click()

        post_form.find_element_by_id('id_submit').click()
        
        # Juan goes to check main page for his post
        self.browser.get(self.live_server_url + '/blog')

        page_body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Juan\'s first post!', page_body.text)

        # Juan logs out
        self.browser.find_element_by_link_text('Log out').click()
        self.browser.get(self.live_server_url + '/')
        page_body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Juan Ramirez',page_body.text)
        self.assertIn('Log in',page_body.text)
