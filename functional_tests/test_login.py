
from selenium import webdriver
import os
import logging
import sys
import time
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

DEFAULT_WAIT = 5

class TestClass(LiveServerTestCase):

    def setUp(self, *args, **kwargs):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self, *args, **kwargs):
        self.browser.quit()

    def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        # one more try, which will raise any errors if they are outstanding
        return function_with_assertion()

    def to_auth_provider_screen(self, auth_provider):
        self.wait_for(
            lambda: self.browser.find_element_by_id(auth_provider).click())

    def log_out_button(self):
        return self.wait_for(
            lambda: self.browser.find_element_by_id('Logout'))

    def login_buttons(self):
        return self.wait_for(
            lambda: self.browser.find_element_by_id('LoginButtons'))

    def test_login_links_present(self):
        self.browser.get(self.live_server_url)
        login_buttons = self.login_buttons()
        assert 'Facebook' in login_buttons.text
        assert 'Google' in login_buttons.text
        assert 'Twitter' in login_buttons.text

    def test_facebook_login(self):
        self.browser.get(self.live_server_url)
        self.to_auth_provider_screen("Facebook")

        email = self.wait_for(
            lambda: self.browser.find_element_by_id('email'))
        email.send_keys(os.environ.get("TEST_FACEBOOK_NAME"))
        self.browser.find_element_by_id('pass').\
            send_keys(os.environ.get("TEST_FACEBOOK_PASSWORD")+"\n")

        logout_button = self.log_out_button()
        logout_button.click()
        self.login_buttons()

    def test_google_login(self):
        self.browser.get(self.live_server_url)
        self.to_auth_provider_screen("Google")

        email = self.wait_for(
            lambda: self.browser.find_element_by_id('Email'))
        email.send_keys(os.environ.get("TEST_GOOGLE_NAME")+"\n")
        password = self.wait_for(
            lambda: self.browser.find_element_by_id('Passwd'))
        password.send_keys(os.environ.get("TEST_GOOGLE_PASSWORD")+"\n")
        time.sleep(4)
        self.wait_for(
            lambda: self.browser.find_element_by_id("submit_approve_access").\
                click())

        logout_button = self.log_out_button()
        logout_button.click()
        self.login_buttons()

    def test_twitter_login(self):
        self.browser.get(self.live_server_url)
        self.to_auth_provider_screen("Twitter")

        email = self.wait_for(
            lambda: self.browser.find_element_by_id('username_or_email'))
        email.send_keys(os.environ.get("TEST_TWITTER_NAME"))
        self.browser.find_element_by_id('password').\
            send_keys(os.environ.get("TEST_TWITTER_PASSWORD")+"\n")

        logout_button = self.log_out_button()
        logout_button.click()
        self.login_buttons()
