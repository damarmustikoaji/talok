"""
damar.mustikoaji@gmail.com / @damarresin
Example script to run one test against the Kumparan.com app using Selenium
The test will:
- launch the app
- login as google or fb
- see news from terkini menu
- comment on news
- see news using invalid url
- logout
"""

import sys
import unittest
import time
from HTMLTestRunner import HTMLTestRunner

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testscripts.browser.browser import DriverBrowser
from testscripts.login.login import Login
from testscripts.logout.logout import Logout
from testscripts.news.news import News
from testscripts.news.news import Comment
from testscripts.news.news import Read


LOGIN = None
Baca = None

def NyalakanNotif(driver):
    try:
        modal = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@id="onesignal-popover-dialog" and @class="onesignal-popover-dialog"]')))
        button = modal.find_element_by_xpath('//button[@id="onesignal-popover-allow-button" and @class="align-right primary popover-button"]')
        logging = modal.find_element_by_xpath('//div[@class="popover-body-message"]').text
        print logging
        logging = button.text
        print logging
        button.click()
        time.sleep(2)
    except Exception as e:
        pass#print "Nyalakan notifikasi tidak muncul"

class KumparanTests(unittest.TestCase):
    "Class to run tests against the Kumparan.com app"

    SERVER = None
    ACCOUNT = None
    EMAIL = None
    PASSWORD = None
    BROWSER = None

    @classmethod
    def setUpClass(cls):
        "Setup for the test"
        cls.driver = DriverBrowser(cls.BROWSER)

    def test_a_login(self):
        global LOGIN
        self.startTime = time.time()
        self.driver.get(self.SERVER+"/login")
        self.assertEqual(self.driver.title,"Login")
        NyalakanNotif(self.driver)
        driver, logging, status = Login(self.driver, self.ACCOUNT, self.EMAIL, self.PASSWORD)
        if "PASS" in status:
            print logging
            print status
        else:
            self.fail(logging)
        LOGIN = status
        t = time.time() - self.startTime
        print "%s: %.3f" % (self.id(), t)

    def test_c_see_news(self):
        global LOGIN, Baca
        if LOGIN == "PASS":
            self.startTime = time.time()
            self.driver.get(self.SERVER+"/topic/news/terkini")
            NyalakanNotif(self.driver)
            driver, logging, status = News(self.driver)
            if "PASS" in status:
                print logging
                print status
                Baca = status
            else:
                self.fail(logging)
            t = time.time() - self.startTime
            print "%s: %.3f" % (self.id(), t)
        else:
            self.skipTest("Login Fail")

    def test_d_comment(self):
        global LOGIN, Baca
        if LOGIN == "PASS" and Baca == "PASS":
            self.startTime = time.time()
            #self.driver.get(self.SERVER+"/topic/news/terkini")
            NyalakanNotif(self.driver)
            driver, logging, status = Comment(self.driver)
            if "PASS" in status:
                print logging
                print status
            else:
                self.fail(logging)
            t = time.time() - self.startTime
            print "%s: %.3f" % (self.id(), t)
        else:
            self.skipTest("Login Fail")

    def test_e_see_news_url(self):
        global LOGIN
        #if LOGIN == "PASS":
        self.startTime = time.time()
        url = "/@kumparannews/bnnp-dki-narkoba-di-tempat-hiburan-banyak-dibawa-dari-luarx01"
        self.driver.get(self.SERVER+url)
        NyalakanNotif(self.driver)
        driver, logging, status = Read(self.driver)
        if "PASS" in status:
            print logging
            print status
        else:
            self.fail(logging)
        t = time.time() - self.startTime
        print "%s: %.3f" % (self.id(), t)
        #else:
        #    self.skipTest("Login Fail")

    def test_x_logout(self):
        global LOGIN
        if LOGIN == "PASS":
            self.startTime = time.time()
            self.driver.get(self.SERVER)
            NyalakanNotif(self.driver)
            driver, logging, status = Logout(self.driver)
            if "PASS" in status:
                print logging
                print status
            else:
                self.fail(logging)
            t = time.time() - self.startTime
            print "%s: %.3f" % (self.id(), t)
        else:
            self.skipTest("Login Fail")

    @classmethod
    def tearDownClass(cls):
        "Tear down the test"
        cls.driver.quit()

if __name__ == '__main__':
    command = len(sys.argv)
    if command == 6:
        KumparanTests.BROWSER = sys.argv.pop()
        KumparanTests.SERVER = sys.argv.pop()
        if "http" not in KumparanTests.SERVER:
            KumparanTests.SERVER = "http://"+KumparanTests.SERVER
        KumparanTests.PASSWORD = sys.argv.pop()
        KumparanTests.EMAIL = sys.argv.pop()
        KumparanTests.ACCOUNT = sys.argv.pop()
    else:
        sys.exit("ERROR : Please check again your argument")
    HTMLTestRunner.main()
