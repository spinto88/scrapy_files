# -*- coding: utf-8 -*-

import scrapy

class Item(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    newspaper = scrapy.Field()
    section = scrapy.Field()
#    tag = scrapy.Field()

class Pagina12Spider(scrapy.Spider):
    name = "pagina12"

    def start_requests(self):
        urls = []
        for i in range(35000, 40000):
            urls.append('http://www.pagina12.com.ar/' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers = {'User-agent': 'Mozilla/5.0'})

    def parse(self, response):

        title = response.selector.xpath('//div[@class = "article-title"]/text()')[0].extract()
        subtitle = response.selector.xpath('//div[@class = "article-summary"]/text()')[0].extract()
        body = response.selector.xpath('//div[@class = "article-text"]//text()')
        date = response.selector.xpath('//time/@datetime')[0].extract()
        section = response.selector.xpath('//div[@class = "breadcrumb"]//text()')[2].extract()

        item = Item()
        item['title'] = title
        item['subtitle'] = subtitle
        item['date'] = date
        item['newspaper'] = u'Página12'
        item['section'] = section

        body_text = ''
        for text in body:
            body_text += text.extract() + ' '
        item['body'] = body_text

        return item
