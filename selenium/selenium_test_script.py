
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import *


# Test from website http://selenium-python.readthedocs.io/getting-started.html#using-selenium-with-remote-webdriver
class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()


class BasicWebTestCase(unittest.TestCase):
    # setUp method is called before each test in this class

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

    #Test that the link leads to correct page with title
    def test_title_check(self):
        driver = self.driver
        driver.get("http://web:8000")
        self.assertEqual(driver.title, "Technology Consultation")
        self.assertFalse(driver.title == "Wrong Site")

    def test_navigate_highest_and_newest_page(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")

        # Click on link to "Highest Offer" page
        driver.find_element_by_link_text('Highest Offers').click()

        # Checking that page is a request details page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Request Details")

        # Go back to home
        driver.find_element_by_link_text('Home').click()

        # Click on link to "Newest Request" page
        driver.find_element_by_link_text('Newest Consumer Requests').click()

        # Checking that page is a request details page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Request Details")

    def test_login1(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Log in').click()

        # Checking that page is a login page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Log In")

        # Fill in fields
        user_elem = driver.find_element_by_name("username")
        user_elem.send_keys("admin")
        pw_elem = driver.find_element_by_name("password")
        pw_elem.send_keys("cs3240team22")
        driver.find_element_by_name("is_consumer").click()
        # Click submit
        driver.find_element_by_name("submit").click()
        self.assertTrue("You successfully logged in!" in driver.page_source)

    def test_login2(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Log in').click()

        # Checking that page is a login page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Log In")

        # Fill in fields
        user_elem = driver.find_element_by_name("username")
        user_elem.send_keys("admi")
        pw_elem = driver.find_element_by_name("password")
        pw_elem.send_keys("cs3240team22")
        # driver.find_element_by_name("is_consumer").click()

        # Click submit
        driver.find_element_by_name("submit").click()
        self.assertTrue("Invalid credentials. Check your username and password or sign up first." in driver.page_source)

    def test_logout1(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Log in').click()

        # Fill in fields
        user_elem = driver.find_element_by_name("username")
        user_elem.send_keys("admin")
        pw_elem = driver.find_element_by_name("password")
        pw_elem.send_keys("cs3240team22")
        driver.find_element_by_name("is_consumer").click()
        # Click submit
        driver.find_element_by_name("submit").click()
        driver.find_element_by_link_text('Log out').click()
        heading4 = driver.find_element_by_tag_name('h4')
        self.assertEqual(heading4.text, "You are logged out!")

    def test_create_producer1(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Create producer account').click()
        # Checking that page is a login page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Create Producer")

        # Fill in fields
        user_elem = driver.find_element_by_name("username")
        user_elem.send_keys("nick" + str(randint(0, 2048)))
        pw_elem = driver.find_element_by_name("password")
        pw_elem.send_keys("123")
        first_elem = driver.find_element_by_name("first_name")
        first_elem.send_keys("Nick1")
        last_elem = driver.find_element_by_name("last_name")
        last_elem.send_keys("Kim")
        phone_elem = driver.find_element_by_name("phone")
        phone_elem.send_keys("123")
        email_elem = driver.find_element_by_name("email")
        email_elem.send_keys("nick@gmail.com")
        bio_elem = driver.find_element_by_name("bio")
        bio_elem.send_keys("hey")
        skill_elem = driver.find_element_by_name("skills")
        skill_elem.send_keys("python")
        driver.find_element_by_name("submit").click()

        self.assertTrue("You successfully created a producer account." in driver.page_source)

    def test_create_producer2(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Create producer account').click()
        # Checking that page is a login page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Create Producer")

        # Fill in fields
        user_elem = driver.find_element_by_name("username")
        user_elem.send_keys("admin")
        pw_elem = driver.find_element_by_name("password")
        pw_elem.send_keys("cs3240team22")
        first_elem = driver.find_element_by_name("first_name")
        first_elem.send_keys("Nick1")
        last_elem = driver.find_element_by_name("last_name")
        last_elem.send_keys("Kim")
        phone_elem = driver.find_element_by_name("phone")
        phone_elem.send_keys("123")
        email_elem = driver.find_element_by_name("email")
        email_elem.send_keys("nick@gmail.com")
        bio_elem = driver.find_element_by_name("bio")
        bio_elem.send_keys("hey")
        skill_elem = driver.find_element_by_name("skills")
        skill_elem.send_keys("python")
        driver.find_element_by_name("submit").click()

        self.assertTrue("Producer with username admin exists." in driver.page_source)

    # test with a new person in the database
    def test_create_consumer1(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Create consumer account').click()
        # Checking that page is a login page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Create Consumer")

        # Fill in fields
        user_elem = driver.find_element_by_name("username")
        user_elem.send_keys("elliott" + str(randint(0, 2048)))
        pw_elem = driver.find_element_by_name("password")
        pw_elem.send_keys("123")
        first_elem = driver.find_element_by_name("first_name")
        first_elem.send_keys("elliott")
        last_elem = driver.find_element_by_name("last_name")
        last_elem.send_keys("Kim")
        phone_elem = driver.find_element_by_name("phone")
        phone_elem.send_keys("123")
        email_elem = driver.find_element_by_name("email")
        email_elem.send_keys("elliott@gmail.com")
        driver.find_element_by_name("submit").click()

        self.assertTrue("You successfully created a consumer account." in driver.page_source)

    # test with an invalid username
    def test_create_consumer2(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Create consumer account').click()
        # Checking that page is a login page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Create Consumer")

        # Fill in fields
        user_elem = driver.find_element_by_name("username")
        user_elem.send_keys("admin")
        pw_elem = driver.find_element_by_name("password")
        pw_elem.send_keys("123")
        first_elem = driver.find_element_by_name("first_name")
        first_elem.send_keys("elliott")
        last_elem = driver.find_element_by_name("last_name")
        last_elem.send_keys("Kim")
        phone_elem = driver.find_element_by_name("phone")
        phone_elem.send_keys("123")
        email_elem = driver.find_element_by_name("email")
        email_elem.send_keys("elliott@gmail.com")
        driver.find_element_by_name("submit").click()

        self.assertTrue("Consumer with username admin exists." in driver.page_source)
        '''
    # test first with Consumer (Doesn't work b/c select won't work)
    def test_create_listing1(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Log in').click()

        # Fill in fields
        user_elem = driver.find_element_by_name("username")
        user_elem.send_keys("admin")
        pw_elem = driver.find_element_by_name("password")
        pw_elem.send_keys("cs3240team22")
        driver.find_element_by_name("is_consumer").click()
        # Click submit
        driver.find_element_by_name("submit").click()
        driver.find_element_by_name("Create listing").click()

        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Create Listing")

        title_elem = driver.find_element_by_name("title")
        title_elem.send_keys("something")
        price_elem = driver.find_element_by_name("offered_price")
        price_elem.send_keys("10")
        desc_elem = driver.find_element_by_name("description")
        desc_elem.send_keys("something else")
        avail_elem = driver.find_element_by_name("availability")
        avail_elem.send_keys("mondays")
        driver.find_element_by_name("submit").click()

        self.assertTrue("You successfully created a listing." in driver.page_source)
        '''
    # test with Producer (Won't be able to find it)
    def test_create_listing2(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Log in').click()

        # Fill in fields
        user_elem = driver.find_element_by_name("username")
        user_elem.send_keys("admin")
        pw_elem = driver.find_element_by_name("password")
        pw_elem.send_keys("cs3240team22")
        # driver.find_element_by_name("is_consumer").click()
        # Click submit
        driver.find_element_by_name("submit").click()
        self.assertFalse("Create Listing" in driver.page_source)

    def test_search_listing1(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Search Listings').click()
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Search")
        searchbox = driver.find_element_by_name("query")
        searchbox.send_keys("something")
        driver.find_element_by_name("submit").click()

        self.assertTrue("April 23, 2018" in driver.page_source)

    def test_search_listing2(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Search Listings').click()
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Search")
        searchbox = driver.find_element_by_name("query")
        searchbox.send_keys("some")
        driver.find_element_by_name("submit").click()

        self.assertFalse("April 23, 2018" in driver.page_source)

    def test_search_consumer1(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Search Consumers').click()
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Search")
        searchbox = driver.find_element_by_name("query")
        searchbox.send_keys("elliott")
        driver.find_element_by_name("submit").click()

        self.assertTrue("elliott" in driver.page_source)

    def test_search_consumer2(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Search Consumers').click()
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Search")
        searchbox = driver.find_element_by_name("query")
        searchbox.send_keys("admin")
        driver.find_element_by_name("submit").click()

        self.assertFalse("elliott" in driver.page_source)

    def test_search_producer1(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Search Producers').click()
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Search")
        searchbox = driver.find_element_by_name("query")
        searchbox.send_keys("nick")
        driver.find_element_by_name("submit").click()

        self.assertTrue("nick64" in driver.page_source)

    def test_search_producer2(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")
        driver.find_element_by_link_text('Search Producers').click()
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEqual(heading3.text, "Search")
        searchbox = driver.find_element_by_name("query")
        searchbox.send_keys("admin")
        driver.find_element_by_name("submit").click()

        self.assertFalse("nick" in driver.page_source)
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
