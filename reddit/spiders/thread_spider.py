import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class ThreadSpider(scrapy.Spider):
    name = "thread"
    start_urls = [
        'https://www.reddit.com/r/cloudbells/comments/b8yvk7/test2/']  # Testing Continue this thread

    def __init__(self, dynamic):
        # This disables the browser asking for notifications.
        _browser_profile = webdriver.FirefoxProfile()
        _browser_profile.set_preference("dom.webnotifications.enabled", False)
        self.driver = webdriver.Firefox(
            firefox_profile=_browser_profile, executable_path='geckodriver.exe')

    def parse(self, response):
        dynamic = self.checkDynamic(response)
        if dynamic:
            self.parseDynamic(response)
        else:
            self.parseStatic(response)

    # Parses the HTML, treating it as if it contains dynamic content.
    def parseDynamic(self, response):
        self.driver.get(response.url)
        # page_loaded will be True if it finds the element within 10 seconds, False otherwise.
        page_loaded = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[@type='submit'][contains(text(), 'I Agree')]"))
        )
        if page_loaded:
            # Find and click the cookies button.
            cookiesBtn = self.driver.find_element_by_xpath(
                "//button[@type='submit'][contains(text(), 'I Agree')]")
            cookiesBtn.click()
            self.clickMoreComments()
            self.continueThreads(response)

    # Parses the HTML, treating it as if it contains dynamic content.
    def parseStatic(self, response):
        pass
        # maybe press i agree
        #self.continueThreads(response)

    # Returns true if page is dynamic, false otherwise
    def checkDynamic(self, response):
        return len(response.XPATH("//*[contains(@id, 'moreComments')]").getall()) != 0

    # This loop will continue until it does not find any more More replies to click.
    def clickMoreComments(self):
        more_elements = True
        while (more_elements):
            more_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//*[contains(@id, 'moreComments')]"))
            )
            if more_elements:
                elements = self.driver.find_elements_by_xpath(
                    "//*[contains(@id, 'moreComments')]")
                for e in elements:
                    try:
                        e.click()
                    except Exception as ex:
                        print("caught" + str(ex))
                        continue

    # This loop will continue until it does not find any more Continue This Thread elements.
    def continueThreads(self, response):
        continue_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//span[text()='Continue this thread']")
            )
        )
        if continue_elements:
            cont = self.driver.find_elements_by_xpath(
                "//span[text()='Continue this thread']/..")
            for c in cont:
                href = c.get_attribute("href")
                yield response.follow(href, callback = self.parse)
        else:
            print(
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
