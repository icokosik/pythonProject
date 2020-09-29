import random
from bs4 import BeautifulSoup

import dynamoDB
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

propertyItems = []

def test():
    process = CrawlerProcess()
    # process.crawl(MySpider)
    process.crawl(QuotesSpider2)
    process.start()
    print('closed spider')
    print(propertyItems)
    dynamoDB.insertIntoProperties(propertyItems)


class QuotesSpider2(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.nehnutelnosti.sk/bratislava/byty/predaj/',
    ]

    def parse(self, response):
        for quote in response.css('div.advertisement-item'):
            # yield {
            #     'company': quote.css('span.organisationName::text').get(),
            #     'name': quote.css('div.header span[itemprop="name"]::text').get(),
            #     'size': quote.css('span.desc-left::text').get(),
            #     'price': quote.css('section.content-section.isRealestate div.info span.pull-right').get(),
            # }

            prop = {}
            prop['id'] = str(random.randint(1000, 100000))
            prop['URL'] = quote.css('a.advertisement-item--content__title::attr(href)').get()
            prop['name'] = quote.css('a.advertisement-item--content__title::text').get()
            prop['price'] = 50
            prop['size'] = 50
            print(prop)
            propertyItems.append(prop)




        next_page = response.css('li.component-pagination__item a::attr(href)').get()
        if next_page is not None:
            print('next page')
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)





class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),

            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)















class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['willhaben.at']
    start_urls = ['https://www.willhaben.at/iad/immobilien/haus-kaufen/haus-angebote?areaId=900']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )
    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        print('scraping')
        item = scrapy.Item()
        # item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').get()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').get()
        item['link_text'] = response.meta['link_text']
        url = response.xpath('//td[@id="additional_data"]/@href').get()
        return response.follow(url, self.parse_additional_page, cb_kwargs=dict(item=item))

    def parse_additional_page(self, response, item):
        item['additional_data'] = response.xpath('//p[@id="additional_data"]/text()').get()
        return item

