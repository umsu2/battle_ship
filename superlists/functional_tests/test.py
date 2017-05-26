import os

import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
# points to the path where the chromedriver is installed
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "/home/yang/Downloads"
os.environ["PATH"] += os.pathsep + chrome_driver_path



class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        live_address = os.environ.get('liveserver')
        if live_address:
                cls.server_url = "http://" + live_address
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if os.environ.get('live_server'):
        # if hasattr(cls, 'server_url') and cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(1)

    def tearDown(self):
        # pass
        self.browser.quit()
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Bob has heard about a cool online to-do app. he goes to checkout its home page
        self.browser.get(self.server_url)

        # Bob notices the title says it is a to-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        value1 = 'Buy peacock feathers'
        inputbox.send_keys(value1)

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')  # 1
        self.check_for_row_in_list_table("1: " + value1)


        inputbox = self.browser.find_element_by_id('id_new_item')
        value2 = 'Use peacock feathers to make a fly'
        inputbox.send_keys(value2)
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table("2: " + value2)

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc #1
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep

        # Satisfied, she goes back to sleep
        self.fail('Finish the Test')


    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + 8 + inputbox.size['width'] / 2, # 8 is webkit margin of 16px /2
            512,
            delta=5
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + 8 + inputbox.size['width'] / 2,
            512,
            delta=5
        )