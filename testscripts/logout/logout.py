import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging = None
status = None

def Logout(driver):
    driver = driver
    try:
        #dropdown = driver.find_element_by_xpath('//li/a[@id="dropdown-profile" and @class="dropdown-toggle"]')
        dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li/a[@id="dropdown-profile" and @class="dropdown-toggle"]')))
        dropdown.click()
        time.sleep(2)
        try:
            logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li/a[contains(text(), "Log Out")]')))
            logout.click()
            time.sleep(2)
            try:
                login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@class="btn btn-link color-primary" and @href="/login"]')))
                logging = login.text
                status = "PASS"
            except Exception as e:
                raise
        except Exception as e:
            raise
    except Exception as e:
        raise
    return driver, logging, status
