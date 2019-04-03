import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = ['https://www.reddit.com/r/AskReddit/comments/b0e6ty/whats_an_oh_shit_moment_where_you_realised_youve/']

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='geckodriver.exe')
        

    def parse(self, response):
        self.driver.get(response.url)
        
        sleep(60)

        page_loaded = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id, 'moreComments')]"))
        )

        if page_loaded:
            print("----------------------------------------------------------It worked")
            print("----------------------------------------------------------It worked")
            print("----------------------------------------------------------It worked")
            print("----------------------------------------------------------It worked")
            print("----------------------------------------------------------It worked")
            
            filename = 'test.html'
            print(self.driver.page_source)
            with open(filename, 'a', encoding='utf8') as f:
                f.write(self.driver.page_source)

            # elements = self.driver.find_elements((By.XPATH, "//*[contains(@id, 'moreComments')]"))
            elements = self.driver.find_elements_by_xpath("//*[contains(@id, 'moreComments')]")
            # print(elements)
            print("-------------------------------")
            print(len(elements))
            print("-------------------------------")
            print("LOOK HERE")
            divs = self.driver.find_element_by_xpath("//*[contains(@id, 'SHORTCUT_FOCUSABLE_DIV')]/div[2]/div/div/div/div[2]/div[3]/div[1]/div/div[5]/div/div/div/div[400]")
            # print(len(divs))
            print(divs)

            clickdiv = self.driver.find_elements_by_xpath("//*[contains(@id, 'SHORTCUT_FOCUSABLE_DIV')]/div[2]/div/div/div/div[2]/div[3]/div[1]/div/div[5]/div/div/div/div[400]")[0]
            clickdiv.click()
            print(clickdiv)
            sleep(5)
            filename = 'test2.html'
            with open(filename, 'a', encoding='utf8') as f:
                f.write(self.driver.page_source)
            
            for e in elements:
                try:
                    e.click()
                except Exception as ex:
                    print("caught" + str(ex))
                    continue
                    
            sleep(5)
            filename = 'test3.html'
            with open(filename, 'a', encoding='utf8') as f:
                f.write(self.driver.page_source)
            print("-------------------------------")

        else:
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
        