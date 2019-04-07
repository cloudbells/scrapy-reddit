import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class ThreadSpider(scrapy.Spider):
    name = "thread"
    start_urls = [
        'https://www.reddit.com/r/cloudbells/comments/b8yvk7/test2/'] # Testing Continue this thread

    def __init__(self):
        # This disables the browser asking for notifications.
        _browser_profile = webdriver.FirefoxProfile()
        _browser_profile.set_preference("dom.webnotifications.enabled", False)
        self.driver = webdriver.Firefox(
            firefox_profile=_browser_profile, executable_path='geckodriver.exe')

    def parse(self, response):
        self.driver.get(response.url)
        # page_loaded will be True if it finds the element within 10 seconds, False otherwise.
        page_loaded = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                #(By.XPATH, "//*[contains(@id, 'moreComments')]"))
                (By.XPATH, "//button[@type='submit'][contains(text(), 'I Agree')]"))
        )
        if page_loaded:
            # Find and click the cookies button.
            cookiesBtn = self.driver.find_element_by_xpath(
                "//button[@type='submit'][contains(text(), 'I Agree')]")
            cookiesBtn.click()
            # self.saveHtml()
            # self.clickMoreComments()
            # self.clickDownvotedComments() <- should be in the same method as above
        self.continueThreads()

    # Print to local file to see differences.
    def saveHtml(self):
        filename = 'test.html'
        with open(filename, 'a', encoding='utf8') as f:
            f.write(self.driver.page_source)

    # This loop will continue until it does not find any more More replies to click.
    def clickMoreComments(self):
        loop = True
        while (loop):
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
            else:
                loop = False

    # This loop will continue until it does not find any more Continue This Thread elements.
    def continueThreads(self):
        loop = True
        while (loop):
            continue_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//span[text()='Continue this thread']")
                )
            )
            if continue_elements:
                print("FOUND ELEMENTS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                print("FOUND ELEMENTS???????????????????????????????????????????????????????")
                loop = False