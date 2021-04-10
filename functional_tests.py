from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Limmy has heard about a cool new online to-do app.
        # He goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # He notices the page titles and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # He types "Buy television" into a text box (Limmy's hobby is reviewing movies)
        inputbox.send_keys('Buy telivision')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy television" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1. Buy television' for row in rows), "New to-do item did not appear in table")

        # There is still a text box inviting her to add another item.
        # He enter "Use television to leave movie reviews"
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on his list

        # Limmy wonders if the website will remember his list.
        # Then he sees the website generated a unique URL - his to-do list is still there

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main()
