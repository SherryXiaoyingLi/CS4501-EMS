
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
        self.assertEquals(driver.title, "Technology Consultation")
        self.assertFalse(driver.title == "Wrong Site")

    def test_navigate_highest_and_newest_page(self):
        driver = self.driver
        # Navigate to home page
        driver.get("http://web:8000")

        # Click on link to "Highest Offer" page
        driver.find_element_by_link_text('Highest Offers').click()

        # Checking that page is a request details page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEquals(heading3.text, "Request Details")

        # Go back to home
        driver.find_element_by_link_text('Home').click()

        # Click on link to "Newest Request" page
        driver.find_element_by_link_text('Newest Consumer Requests').click()

        # Checking that page is a request details page
        heading3 = driver.find_element_by_tag_name('h3')
        self.assertEquals(heading3.text, "Request Details")

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()