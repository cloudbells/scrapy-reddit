import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from time import sleep
import logging

#TODO:  Spider to find threads which is then sent to this spider
#       Save comments
#
#       User config: choose to scrape downvoted comments (WILL INCREASE RUNTIME)
#       User config: choose keywords
#       User config: 

class ThreadSpider(scrapy.Spider):
    name = "thread"
    visitedUrls = []
    start_urls = [
        'https://www.reddit.com/r/cloudbells/comments/30hau3/test/']

    def __init__(self, name=None, **kwargs):
        self.startUrlDriver()

    # Starts the selenium urldriver and clicks cookies button
    def startUrlDriver(self):
        optionsurl = Options()
        #optionsurl.add_argument("--headless")
        _browser_profile = webdriver.FirefoxProfile()
        _browser_profile.set_preference("dom.webnotifications.enabled", False)
        self.urldriver = webdriver.Firefox(
            firefox_profile=_browser_profile, executable_path='geckodriver.exe', firefox_options=optionsurl)
        self.urldriver.get("https://www.reddit.com/r/letstalkmusic")
        page_loaded = WebDriverWait(self.urldriver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[@type='submit'][contains(text(), 'I Agree')]"))
        )
        if page_loaded:
            # Find and click the cookies button.
            cookiesBtn = self.urldriver.find_element_by_xpath(
                "//button[@type='submit'][contains(text(), 'I Agree')]")
            cookiesBtn.click()

    # Finds urls on subreddit and returns a list of url strings
    def getNextUrl(self):
        threadUrls = self.urldriver.find_elements_by_xpath("//a[contains(@data-click-id, 'comments')]")
        urls = []

        for url in threadUrls:
            if url.get_attribute("href") not in self.visitedUrls:
                self.visitedUrls.append(url.get_attribute("href"))
                urls.append(url.get_attribute("href"))

        return urls

    def parse(self, response):
        with open("test.txt", 'a', encoding='utf8') as f:
                    f.write(response.url + "\n")

        if self.checkDynamic(response): # Dynamic.
            print("DYNAMICCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
            hrefList = self.parseDynamic(response)
        else: # Static.
            print("STATIKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            hrefList = self.parseStatic(response)
        # hreflist for continue this thread
        if len(hrefList) != 0:
            for href in hrefList:
                print(href)
                yield response.follow(href, callback=self.parse)
        # hreflist = 0, thread is done scraped
        urls = self.getNextUrl()
        for url in urls:
            yield response.follow(url, callback=self.parse)

        

    # Parses the HTML, treating it as if it contains dynamic content.
    def parseDynamic(self, response):
        # This disables the browser asking for notifications.
        options = Options()
        #options.add_argument("--headless")
        _browser_profile = webdriver.FirefoxProfile()
        _browser_profile.set_preference("dom.webnotifications.enabled", False)
        self.driver = webdriver.Firefox(
            firefox_profile=_browser_profile, executable_path='geckodriver.exe', firefox_options=options)
        self.driver.get(response.url)
        # page_loaded will be True if it finds the element within 10 seconds, False otherwise.
        page_loaded = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[@type='submit'][contains(text(), 'I Agree')]"))
        )
        hrefList = []
        if page_loaded:
            # Find and click the cookies button.
            cookiesBtn = self.driver.find_element_by_xpath(
                "//button[@type='submit'][contains(text(), 'I Agree')]")
            cookiesBtn.click()
            commentsBtn = self.driver.find_element_by_xpath(
                "//button[contains(text(), 'View all')]")
            commentsBtn.click()
            self.clickMoreComments()
            hrefList = self.continueDynamic(response)
        self.driver.close()
        return hrefList

    # Parses the HTML, treating it as if it contains dynamic content.
    def parseStatic(self, response):
        return self.continueStatic(response)

    # This loop will continue until it does not find any more Continue This Thread elements.
    def continueDynamic(self, response):
        continue_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//span[text()='Continue this thread']")
            )
        )
        print(continue_elements)
        hrefList = []
        if continue_elements:
            cont = self.driver.find_elements_by_xpath(
                "//span[text()='Continue this thread']/..")
            for c in cont:
                href = c.get_attribute("href")
                with open("test.txt", 'a', encoding='utf8') as f:
                    f.write(href + "\n")
                hrefList.append(href)
            return hrefList

    # Finds "continue this thread" elements statically.
    def continueStatic(self, response):
        href = response.xpath("//span[text()='Continue this thread']/../@href").getall()
        hList = []
        for h in href:
            with open("test.txt", 'a', encoding='utf8') as f:
                f.write(h)
            hList.append(h)
        return hList

    # Returns true if page is dynamic, false otherwise
    def checkDynamic(self, response):
        return len(response.xpath("//*[contains(@id, 'moreComments')]").getall()) != 0

    # This loop will continue until it does not find any more More replies to click.
    def clickMoreComments(self):
        loop = True
        while (loop):
            try:
                more_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//*[contains(@id, 'moreComments')]"))
                )
            except TimeoutException as te:
                print(str(te))
                loop = False
                break
            if more_elements:
                elements = self.driver.find_elements_by_xpath(
                    "//*[contains(@id, 'moreComments')]")
                for e in elements:
                    try:
                        e.click()
                    except Exception as ex:
                        print(str(ex))
                self.clickDownvoted()
            else:
                loop = False

    # Attempts to click downvoted comments.
    def clickDownvoted(self):
        downvoted = self.driver.find_elements_by_xpath(
            "//div/button/i[contains(@class, 'icon-expand')]")
        for d in downvoted:
            try:
                d.click()
            except Exception as ex:
                print(str(ex))