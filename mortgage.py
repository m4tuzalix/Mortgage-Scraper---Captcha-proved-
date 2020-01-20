from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from data import get_data
import time
import random


class Mortgage:
    def __init__(self,kod, nr, nr2):
        self.kod = kod
        self.nr = nr
        self.nr2 = nr2
        self.random_number = random.uniform(1.17, 4.79)
        self.raw_data = []
        

        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.browser = webdriver.Ie("IeWebDriver.exe", ie_options=self.chrome_options)
        self.browser.set_window_size(1440,900)
        self.browser.delete_all_cookies()
        self.browser.get("https://przegladarka-ekw.ms.gov.pl/eukw_prz/KsiegiWieczyste/wyszukiwanieKW?komunikaty=true&kontakt=true&okienkoSerwisowe=false")
    
    def stop_work(self):
        print("Work has been ended")
        self.browser.quit()
        
    
    def mortgage(self): #// login to kw
        mortgage_inputs_id = ["kodWydzialuInput", "numerKsiegiWieczystej", "cyfraKontrolna"]
        logins = [self.kod, self.nr, self.nr2]
        for option,login in zip(mortgage_inputs_id, logins):
            mortgage_number = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f"//div[@class='section']//div[2]//div[@class='content-column']//div[@class='wkw-form main-content clearfix']//input[@id='{option}']")))
            if mortgage_number:
                mortgage_number.send_keys(login)


        submit = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='content']//form//div[3]//div[@class='button-row']//button[1]")))
        if submit:
            submit.click()
            attempt = 0
            for x in range(50): #/// iterates until captcha is being triggered
                try: #// this 'try' checks if mortgage number is correct. If not then append to excel fails sheet
                    number_validation = WebDriverWait(self.browser, random.uniform(1.1, 1.69)).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='content']//form//div[1]//div[2]//div[@class='content-column']//div[@class='info-content']//span[@id='cyfraKontrolna.errors']")))
                    print("Number Invalid, going to next id")
                    return False
                    self.browser.quit()
                    break
                except TimeoutException:
                        try:
                            self.browser.execute_script("""document.querySelector("button[id='wyszukaj'").click();""")
                            attempt += 1
                            print("attempt: "+str(attempt))
                            time.sleep(self.random_number)
                        except:
                            break #/// if 'try' selector throws exception then it means that captcha has been passed (bot has got in) and can leave the itteration


    def read_content(self):
        try:
            submit_to_main = WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='content']//div[4]//form//button[@id='przyciskWydrukZupelny']")))
            submit_to_main.click()

            pages_amount = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//table//tbody//tr//td//input[contains(@value, 'Dz')]")))
            
            data_info = ["nazwa sądu","siedziba sądu","kod wydziału"]
            for info in data_info:
                data_wydzial = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f"//div[@id='contentDzialu']//table[2]//tbody//tr//td[contains(text(), '{info}')]")))
                if data_wydzial:
                    final_data = data_wydzial.find_element_by_xpath('./following::td').text
                    self.raw_data.append(final_data)
            
            # print("Success, appended to report")
            # print("\n")
            # self.browser.quit() #/// clears selenium
            return self.raw_data
            self.browser.quit()
        except TimeoutException:
            return False
        



