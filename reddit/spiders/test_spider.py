import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = ['https://www.reddit.com/r/cloudbells/comments/b8yvk7/test2/']

    def __init__(self):
        _browser_profile = webdriver.FirefoxProfile()
        _browser_profile.set_preference("dom.webnotifications.enabled", False)
        self.driver = webdriver.Firefox(firefox_profile =_browser_profile, executable_path='geckodriver.exe')

    def parse(self, response):
        self.driver.get(response.url)
        # page_loaded will be True if it finds the element within 10 seconds, False otherwise.
        page_loaded = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id, 'moreComments')]"))
        )
        if page_loaded:
            # Find and click the cookies button.
            cookiesBtn = self.driver.find_element_by_xpath("//button[@type='submit'][contains(text(), 'I Agree')]")
            cookiesBtn.click()
            # Find all elements 
            elements = self.driver.find_elements_by_xpath("//*[contains(@id, 'moreComments')]")
            # print(elements)
            print("-------------------------------")
            print(len(elements))
            print("-------------------------------")
            print("LOOK HERE")
            
            # print(len(divs))
            # print(divs)

            try:
                divs = self.driver.find_element_by_xpath("//*[contains(@id, 'SHORTCUT_FOCUSABLE_DIV')]/div[2]/div/div/div/div[2]/div[3]/div[1]/div/div[5]/div/div/div/div[400]")
                clickdiv = self.driver.find_elements_by_xpath("//*[contains(@id, 'SHORTCUT_FOCUSABLE_DIV')]/div[2]/div/div/div/div[2]/div[3]/div[1]/div/div[5]/div/div/div/div[400]")[0]
                clickdiv.click()
                print(clickdiv)
                sleep(5)
            except Exception as ex:
                print("!!!!!!!!!!!!!!!!!!!!!!" + str(ex))
            
            filename = 'test2.html'
            with open(filename, 'a', encoding='utf8') as f:
                f.write(self.driver.page_source)
            
            for e in elements:
                try:
                    print("???????????????????????????????????????????????????????")
                    print(c)
                    print(str(c))
                    print("???????????????????????????????????????????????????????")
                    self.driver.get(str(c))
                except Exception as ex:
                    print("caught " + str(ex))
                    continue

        else:
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
        
        
        