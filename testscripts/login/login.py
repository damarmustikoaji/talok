import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging = None
status = None

def Login(driver, ACCOUNT, EMAIL, PASSWORD):
    driver = driver
    if ACCOUNT == "google" or ACCOUNT == "fb":
        window_before = driver.window_handles[0]
        print window_before
        print driver.current_url
        time.sleep(3)
        if "google" in ACCOUNT:
            try:
                googlebutton = driver.find_element_by_xpath('//button[@class="btn btn-block btn-lg btn-gplus btn-glow"]')
                logging = googlebutton.text
                print logging
                googlebutton.click()
                time.sleep(5)
                try:
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    logging = window_after
                    print logging
                    logging = driver.current_url
                    print logging
                    logging = driver.title
                    print logging
                    driver.find_element_by_xpath('//input[@type="email" and @id="identifierId"]').send_keys(EMAIL)
                    time.sleep(1)
                    driver.find_element_by_xpath('//content/span[contains(text(), "Next")]').click()
                    time.sleep(5)
                    try:
                        driver.find_element_by_xpath('//input[@type="password" and @name="password"]').send_keys(PASSWORD)
                        time.sleep(1)
                        driver.find_element_by_xpath('//content/span[contains(text(), "Next")]').click()
                        try:
                            alert = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Wrong")]')))
                            logging = "Wrong password."
                            status = "FAIL"
                        except Exception as e:
                            try:
                                time.sleep(10)
                                driver.switch_to_window(window_before)
                                driver.get("https://kumparan.com")
                                #time.sleep(5)
                                #driver.refresh()
                                logging = window_before
                                print logging
                                logging = driver.current_url
                                try:
                                    notifications = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dropdown-notif")))
                                    status = "PASS"
                                except Exception as e:
                                    logging = "Login Gagal"
                                    status = "FAIL"
                            except Exception as e:
                                raise
                    except Exception as e:
                        raise
                except Exception as e:
                    raise
            except Exception as e:
                raise
        elif "fb" in ACCOUNT:
            try:
                fbbutton = driver.find_element_by_xpath('//button[@class="btn btn-block btn-lg btn-fb btn-glow metro"]')
                logging = fbbutton.text
                print logging
                fbbutton.click()
                time.sleep(5)
                try:
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    logging = window_after
                    print logging
                    logging = driver.current_url
                    print logging
                    logging = driver.title
                    print logging
                    driver.find_element_by_xpath('//input[@type="text" and @id="email"]').send_keys(EMAIL)
                    time.sleep(1)
                    driver.find_element_by_xpath('//input[@type="password" and @id="pass"]').send_keys(PASSWORD)
                    time.sleep(1)
                    driver.find_element_by_xpath('//input[@type="submit" and @name="login"]').click()
                    time.sleep(5)
                    try:
                        alert = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "salah")]')))
                        logging = "Kata sandi yang Anda masukkan salah."
                        status = "FAIL"
                    except Exception as e:
                        try:
                            confirm = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit" and @name="__CONFIRM__"]')))
                            logging = confirm.text
                            print logging
                            time.sleep(5)
                            confirm.click()
                            time.sleep(5)
                        except Exception as e:
                            print "Tidak ada konfirmasi fb"
                        try:
                            time.sleep(10)
                            driver.switch_to_window(window_before)
                            driver.get("https://kumparan.com")
                            #time.sleep(5)
                            #driver.refresh()
                            logging = window_before
                            print logging
                            logging = driver.current_url
                            try:
                                notifications = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dropdown-notif")))
                                status = "PASS"
                            except Exception as e:
                                logging = "Login Gagal"
                                status = "FAIL"
                        except Exception as e:
                            raise
                except Exception as e:
                    raise
            except Exception as e:
                raise
    else:
        logging = "Please check account argument 'google' or 'fb'"
        status = "FAIL"
    return driver, logging, status
