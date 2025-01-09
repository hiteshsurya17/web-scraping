import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector

class AdvancescraperSpider(scrapy.Spider):
    name = "scrollscraper"

    def start_requests(self):
        yield scrapy.Request('https://quotes.toscrape.com/scroll',
                             meta = dict(
                                 playwright = True,
                                 playwright_include_page = True,
                                 playwright_page_methods = [
                                     PageMethod('wait_for_selector','div.quote')
                                 ],
                                 errback = self.close_page
                            ))

    async def parse(self, response):

        page = response.meta['playwright_page']
        for i in range(2,11):
            quote_count = 10 * i
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            await page.wait_for_selector(f'div.quote:nth-child({quote_count})')

        html = await page.content()
        await page.close()
        s = Selector(text=html)

        for quote in s.css('div.quote'):
            yield{
                'quote' : quote.css('span.text::text').get(),
                'author' : quote.css('span small.author::text').get(),
                'tags' : quote.css('div.tags a::text').get()
            }

            
    async def close_page(self, error):

        page = error.request.meta['playwright_page']
        page.close()