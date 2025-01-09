from typing import Iterable
import scrapy


class AdvancescraperSpider(scrapy.Spider):
    name = "jsscraper"

    def start_requests(self):
        yield scrapy.Request('https://quotes.toscrape.com/js/',meta={'playwright':True})

    def parse(self, response):
        yield{
            "text" : response.text
        }
    

        
