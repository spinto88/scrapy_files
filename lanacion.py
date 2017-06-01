# -*- coding: utf-8 -*-
import scrapy

class Item(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    newspaper = scrapy.Field()
    section = scrapy.Field()
    tag = scrapy.Field()
    author = scrapy.Field()

class LaNacionSpider(scrapy.Spider):
    name = "lanacion"

    def start_requests(self):
        urls = []
        urls.append('http://www.lanacion.com.ar/edicion-impresa')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links)

    def parse(self, response):

        try:
            title = response.selector.xpath('//*[@itemprop = "headline"]/text()')[0].extract()
        except:
            title = ''

        try:
            subtitle = response.selector.xpath('//*[@itemprop = "description"]/text()')[0].extract()
        except:
            subtitle = ''

        try:
            body = response.selector.xpath('//*[@itemprop = "articleBody"]//*/text()')
        except:
            body = ''

        try:
            date_time = response.selector.xpath('//div[@class = "fecha"]//@content')[0].extract()
            date = date_time.split(' ')[0] 
            time = date_time.split(' ')[1]
        except:
            date = ''
            time = ''

        try:
            names = response.selector.xpath('//span[@itemprop = "name"]/text()')
        except:
            names = ''

        try:
            author = response.selector.xpath('//a[@itemprop = "author"]/text()')[0].extract()
        except:
            author = ''

        item = Item()
        item['title'] = title
        item['subtitle'] = subtitle
        item['date'] = date
        item['time'] = time
        item['author'] = author

        try:
            item['newspaper'] = names[0].extract()
        except:
            item['newspaper'] = u'LaNación'

        try:
            item['section'] = names[1].extract()
        except:
            item['section'] = ''

        try:
            item['tag'] = names[2].extract()
        except:
            item['tag'] = ''

        body_text = ''
        try:
            for text in body:
                body_text += text.extract() + ' '
        except: 
            pass

        item['body'] = body_text

        return item

            
    def parse_links(self, response):

        links = response.selector.xpath('//*[@class = "f-linkNota"]/@href').extract()
        for link in links:
            yield scrapy.Request(url = response.urljoin(link), callback = self.parse)
