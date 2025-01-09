import scrapy
from scrapy_playwright.page import PageMethod

class AdvancescraperSpider(scrapy.Spider):
    name = "delayscraper"

    def start_requests(self):
        yield scrapy.Request('https://quotes.toscrape.com/js-delayed/',
                             meta = dict(
                                 playwright = True,
                                 playwright_include_page = True,
                                 playwright_page_methods = [
                                     PageMethod('wait_for_selector','div.quote')
                                 ]
                             ))

    async def parse(self, response):

        for quote in response.css('div.quote'):
            yield{
                'quote' : quote.css('span.text::text').get(),
                'author' : quote.css('span small.author::text').get(),
                'tags' : quote.css('div.tags a::text').get()
            }

        if response.css('li.next'):
            next_page = response.css('li.next a::attr(href)').get()
            yield scrapy.Request('https://quotes.toscrape.com/'+next_page,
                             meta = dict(
                                 playwright = True,
                                 playwright_include_page = True,
                                 playwright_page_methods = [
                                     PageMethod('wait_for_selector','div.quote')
                                 ]
                             ))
            