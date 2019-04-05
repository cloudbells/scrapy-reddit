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
        self.driver = webdriver.Firefox(executable_path='geckodriver.exe')
        

    def parse(self, response):
        self.driver.get(response.url)
        
        sleep(10)

        if True:
            cookiesBtn = self.driver.find_element_by_xpath("//button[@type='submit'][contains(text(), 'I Agree')]")
            cookiesBtn.click()

            continueLinks = self.driver.find_elements_by_xpath("//span[text()='Continue this thread']/../@href")
            for c in continueLinks:
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
        
        
        