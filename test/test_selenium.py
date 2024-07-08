'''
Example of using Chromium with Selenium on Linux machine
'''
import json

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options

import os
import socket
import threading
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class ChatAutomaton:

    def __init__(self, install=False,headless=True,sandbox=False,user_data='~/.config/chromium',has_logs=False):
        '''


        References: https://github.com/SergeyPirogov/webdriver_manager
        https://googlechromelabs.github.io/chrome-for-testing/
        :param install:
        :param headless:
        :param sandbox:
        :param user_data:
        '''
        chrome_options = Options()
        if not sandbox: chrome_options.add_argument('--no-sandbox')
        if headless: chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--user-data-dir={user_data}')
        if not has_logs:
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
            logger.setLevel(logging.ERROR)  # or any variant from ERROR, CRITICAL or NOTSET

            logger = logging.getLogger('urllib3.connectionpool')
            logger.setLevel(logging.ERROR)  # or any variant from ERROR, CRITICAL or NOTSET

        manager = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM)

        browser_type = manager.driver.get_browser_type()
        driver_url = manager.driver.get_driver_download_url(os_type="linux64")
        driver_name = manager.driver.get_name()

        # install the first time
        if install:
            self._driver = webdriver.Chrome(service=ChromiumService(manager.install()),
                                  options=chrome_options)
        else:
            self._driver = webdriver.Chrome(service=ChromiumService(manager),
                                  options=chrome_options)
    def run(self,file_target):
        """

        CSS Selectors: https://www.w3schools.com/cssref/css_selectors.php

        :param file_target:
        :return:
        """

        with open(file_target,"r") as file:
            scans = json.load(file)
            for scan in scans:
                logging.info("Loading page %s" % scan['url'])
                self._driver.get(scan["url"])
                # TODO: how do we know all the page has loaded? Simple wait here for now.
                time.sleep(1)
                logging.debug("Title webpage %s" % self._driver.title)

                try:
                    # locate the various elements
                    user_input = self._driver.find_element(By.CSS_SELECTOR, scan['message_input_css'])

                    if scan['message_human_init']:
                        user_messages = self._driver.find_element(By.CSS_SELECTOR, scan['message_human_css'])
                    if scan['message_bot_init']:
                        bot_messages = self._driver.find_element(By.CSS_SELECTOR, scan['message_bot_css'])

                    user_input.send_keys("Hello!")

                    user_input.send_keys(Keys.ENTER)

                    logging.info("Sent message")

                    #now wait for the response
                    time.sleep(1)
                    user_messages = self._driver.find_elements(By.CSS_SELECTOR, scan['message_human_css'])
                    bot_messages = self._driver.find_elements(By.CSS_SELECTOR, scan['message_bot_css'])

                    logging.info("Got messages")

                    for user_msg in user_messages:
                        logging.info("User message id = {0} text {1}".format(user_msg.id,user_msg.text))
                    for bot_msg in bot_messages:
                        logging.info("User message id = {0} text {1}".format(bot_msg.id,bot_msg.text))

                except selenium.common.exceptions.NoSuchElementException as e:
                    logging.error("Unable to find all the elements")

                self._driver.close()


autobot = ChatAutomaton(install=True)

autobot.run("./found.json")