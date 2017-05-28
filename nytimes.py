# -*- coding: utf-8 -*-

import scrapy

class Item(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    newspaper = scrapy.Field()
    section = scrapy.Field()
    tag = scrapy.Field()

class NYTSpider(scrapy.Spider):
    name = "nyt"

    def start_requests(self):
        urls = []
        urls.append('http://www.nytimes.com/pages/todayspaper/index.html')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links, headers = {})

    def parse(self, response):

        try:
            title = response.selector.xpath('//*[@itemprop = "headline"]/text()')[0].extract()
        except:
            title = ''

        item = Item()
        item['title'] = title

        return item

            
    def parse_links(self, response):

        links = response.selector.xpath('//div[@class = "story"]//*[@href]').extract()
        for link in set(links):
            yield scrapy.Request(url = response.urljoin(link), callback = self.parse)
