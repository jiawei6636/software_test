from django.test import LiveServerTestCase
import time
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10
# class NewVisitorTest(unittest.TestCase):
class NewVisitorTest(LiveServerTestCase):



    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

#------动态的等待检查时间-----


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

    # 第六节初始另写了一个
    def test_can_start_a_list_for_one_user(self):

        #-------------------v1 start----------------------
        # self.browser.get('http://localhost:8000')
        # self.assertIn('To-Do',self.browser.title)
        # self.fail("Finish the test!")
        # -------------------v1 end----------------------



        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        # self.browser.get('http://localhost:8000')

        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box (Edith's hobby # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        #  "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)

        #没有动态检查时间的版本
        # self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')


        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # # self.assertTrue(
        # #     any(row.text == '1: Buy peacock feathers' for row in rows),
        # #     f"New to-do item did not appear in table. Contents were:\n{table.text}"
        # # )
        # self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

        # The page updates again, and now shows both items on her list

        # There is still a text box inviting her to add another item. She
        #  enters "Use peacock feathers to make a fly" (Edith is very
        #  methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # # The page updates again, and now shows both items on her list
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        # self.assertIn(
        #     '2: Use peacock feathers to make a fly',
        #     [row.text for row in rows]
        # )

        # 没有动态检查时间的版本
        # self.check_for_row_in_list_table('1: Buy peacock feathers')
        # self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')


        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Satisfied, she goes back to sleep

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        [...]





    def test_multiple_users_can_start_lists_at_different_urls(self):

        #  Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc

        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis visits the home page. There is no sign of Edith's
        #  list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        #  is less interesting than Edith...

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep


#-----------using the Django test runner to launch the FT.-----
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')




# browser = webdriver.Chrome()
#
# browser.get('http://localhost:8000')
#
# # She notices the page title and header mention to-do lists
#
# assert 'To-Do' in browser.title,"Brower title was "+browser.title
#
# # She is invited to enter a to-do item straight away
#
# # She types "Buy peacock feathers" into a text box (Edith's hobby
# # is tying fly-fishing lures)
#
# # When she hits enter, the page updates, and now the page lists
# # "1: Buy peacock feathers" as an item in a to-do list
#
# # There is still a text box inviting her to add another item. She
# # enters "Use peacock feathers to make a fly" (Edith is very methodical)
#
# # The page updates again, and now shows both items on her list
#
# # Edith wonders whether the site will remember her list. Then she sees # that the site has generated a unique URL for her -- there is some
# # explanatory text to that effect.
#
# # She visits that URL - her to-do list is still there.
#
# # Satisfied, she goes back to sleep
#
# browser.quit()
