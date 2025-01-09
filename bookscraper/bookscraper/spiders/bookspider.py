import scrapy
from bookscraper.items import BookItem
import random

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    # custom_settings = {
    #     'FEEDS' : {
    #         'books.json' : {'format': 'json','overwrite': 'true'},
    #      }
    # }

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url,callback = self.book_parse)

            next_page = response.css('li.next a::attr(href)').get()
            if next_page :
                if 'catalogue' in next_page:
                    next_page_url = 'https://books.toscrape.com/' + next_page
                else: 
                    next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
                yield response.follow(next_page_url,callback = self.parse)

    def book_parse(self,response):
        rows = response.css('table.table-striped tr')
        book_item =BookItem()

        book_item['url'] = response.url,
        book_item['title'] = response.css('div.product_main h1::text').get(),
        book_item['price'] = response.css('div.product_main p.price_color::text').get(),
        book_item['product_type'] = rows[1].css('td').get(),
        book_item['price_excl_tax'] = rows[2].css('td').get(),
        book_item['price_incl_tax'] = rows[3].css('td').get(),
        book_item['tax'] = rows[4].css('td').get(),
        book_item['availability'] = rows[5].css('td').get(),
        book_item['num_of_reviews'] = rows[6].css('td').get(),
        book_item['stars'] = response.css('p.star-rating').attrib['class'],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            
        yield book_item