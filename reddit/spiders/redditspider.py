# -*- coding: utf-8 -*-
import scrapy


class RedditspiderSpider(scrapy.Spider):
    name = 'redditspider'
    allowed_domains = ['reddit.com']
    start_urls = ['http://reddit.com/']

    def parse(self, response):
        pass
