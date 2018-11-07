import datetime
import os
import unittest
import sys
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import configparser
import untangle

class CurrencyTest(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read("/var/ini/data.ini")
        data = self.config['POCdata']

        logging.basicConfig(level=logging.INFO, filename = '/var/logs/'+ data['LogFile'] )

        logging.info("Setting up Driver")
        WAIT = 30
        
        os.environ['MOZ_HEADLESS'] = '1'
        binary = FirefoxBinary('/usr/local/firefox/firefox')
        self.driver = webdriver.Firefox(firefox_binary=binary)
        
        logging.info("Setting Driver Settings")
        self.driver.implicitly_wait(WAIT)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, WAIT)
    
    def test_PoC(self):
        logging.info("Starting PoC")
        driver, wait = self.driver, self.wait
        data = self.config['example']
        
        logging.info("Going to CurrencyConverter")
        link = "http://currencyconverter.kowabunga.net/converter.asmx"
        driver.get(link)
        
        logging.info("Going to GetCurrencyRate")
        elem = wait.until(EC.presence_of_element_located( (By.XPATH, '//*[@id="content"]/span[1]/ul/li[6]/a') ) )
        elem.click()

        logging.info("Enter Data")
        elem = wait.until(EC.presence_of_element_located( (By.XPATH, '//*[@id="content"]/span/form/table/tbody/tr[2]/td[2]/input') ) )
        elem.send_keys(data['currency'], Keys.TAB, data['date'])
		#datetime uitzoeken in Python
        format = "%Y%m%d%H%M%S%f"
        date = datetime.datetime.now()
        driver.get_screenshot_as_file('screenshots/screenshotHomePage'+date.strftime(format)+'.png')
        elem.send_keys(Keys.ENTER)
        
        logging.info("Switch to, and read, XML")
        driver.switch_to.window(driver.window_handles[1])
        elem = wait.until(EC.url_to_be ("http://currencyconverter.kowabunga.net/converter.asmx/GetCurrencyRate"))
        date = datetime.datetime.now()
        driver.get_screenshot_as_file('screenshots/screenshotResultPage'+date.strftime(format)+'.png')
        source = driver.page_source
        result = untangle.parse(source)

        logging.info("Result: " + result.decimal.cdata)
        print(result.decimal.cdata)
		
        cfgfile = open("/var/ini/data.ini", "w")
        self.config.set('example','exchange', result.decimal.cdata)
        self.config.write(cfgfile)
        cfgfile.close()
       

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
