from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Limmy has heard about a cool new online to-do app.
        # He goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page titles and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # He types "Buy television" into a text box (Limmy's hobby is reviewing movies)
        inputbox.send_keys('Buy television')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy television" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy television')

        # There is still a text box inviting her to add another item.
        # He enter "Use television to leave movie reviews"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use television to leave movie reviews')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('1: Buy television')
        self.wait_for_row_in_list_table('2: Use television to leave movie reviews')

        # Limmy wonders if the website will remember his list.
        # Then he sees the website generated a unique URL - his to-do list is still there
        self.fail('Finish the test!')

        # Satisfied, he goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy DVD player')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy DVD player')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's list is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #  Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy television', page_text)
        self.assertNotIn('Use television to leave movie reviews', page_text)

        # Francis starts a new list by entering a new item
        # He is less interesting than Edith
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy truffles')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy truffles')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy television', page_text)
        self.assertIn('Buy truffles', page_text)

        # Satisfied, they both go back to sleep
