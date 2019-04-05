import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class ThreadSpider(scrapy.Spider):
    name = "thread"
    start_urls = ['https://www.reddit.com/r/AskReddit/comments/b0e6ty/whats_an_oh_shit_moment_where_you_realised_youve/']

    def __init__(self):
        _browser_profile = webdriver.FirefoxProfile()
        _browser_profile.set_preference("dom.webnotifications.enabled", False)
        self.driver = webdriver.Firefox(firefox_profile =_browser_profile, executable_path='geckodriver.exe')
        

    def parse(self, response):
        self.driver.get(response.url)
        
        
        # sleep(60)

        page_loaded = WebDriverWait(self.driver, 100).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id, 'moreComments')]"))
        )

        if page_loaded:
            cookiesBtn = self.driver.find_element_by_xpath("//button[@type='submit'][contains(text(), 'I Agree')]")
            cookiesBtn.click()
            filename = 'test.html'
            print(self.driver.page_source)
            with open(filename, 'a', encoding='utf8') as f:
                f.write(self.driver.page_source)

            loop = True
            while(loop):
                more_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id, 'moreComments')]"))
                )
                if more_elements:
                    elements = self.driver.find_elements_by_xpath("//*[contains(@id, 'moreComments')]")
                    for e in elements:
                        try:
                            e.click()
                        except Exception as ex:
                            print("caught" + str(ex))
                            continue
                else:
                    loop = False
                    
            print("----------------------------------------------------------It worked")
            print("----------------------------------------------------------It worked")
            print("----------------------------------------------------------It worked")
            print("----------------------------------------------------------It worked")
            print("----------------------------------------------------------It worked")
            
            filename = 'test2.html'
            with open(filename, 'a', encoding='utf8') as f:
                f.write(self.driver.page_source)

        else:
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
            print("----------------------------------------------------------It didn't")
        