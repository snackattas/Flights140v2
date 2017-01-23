
from selenium import webdriver
import logging
DEFAULT_WAIT = 5
class TestClass:

    def setup_method(self):
        logging.warninig('here')
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def teardown_method(self):
        self.browser.quit()

    def test_login_links_present(self):
        body = self.browser.find_element_by_tag_name('body')
        assert 'facebook' in body.text
        assert 'google' in body.text
        assert 'twitter' in body.text
