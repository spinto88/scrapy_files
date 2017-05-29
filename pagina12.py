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
        for i in range(35000, 35100):
            urls.append('http://www.pagina12.com.ar/' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        try:
            title = response.selector.xpath('//div[@class = "article-title"]/text()')[0].extract()
        except:
            title = ''

        try:
            subtitle = response.selector.xpath('//div[@class = "article-summary"]/text()')[0].extract()
        except:
            subtitle = ''

        try: 
            body = response.selector.xpath('//div[@class = "article-text"]//text()')
	    body_text = ''
            for text in body:
                body_text += text.extract() + ' '

        except: 
            body = ''

        try:
            date = response.selector.xpath('//time/@datetime')[0].extract()
        except:
            date = ''

        try:
            section = response.selector.xpath('//div[@class = "breadcrumb"]//text()')[2].extract()
        except:
            section = ''

        item = Item()
        item['title'] = title
        item['subtitle'] = subtitle
        item['date'] = date
        item['newspaper'] = u'Página12'
        item['section'] = section
	item['body'] = body_text

        return item
