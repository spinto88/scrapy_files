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
    url = scrapy.Field()

class WPostSpider(scrapy.Spider):
    name = "wpost"

    def start_requests(self):
        urls = []
        urls.append('https://www.washingtonpost.com/todays_paper/updates/')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links)

    def parse(self, response):

        try:
            title = response.selector.xpath('//*[@itemprop = "headline"]/text()')[0].extract()
        except:
            title = ''

        try:
            url = response.url
        except:
            url = ''

        try:
            body = response.selector.xpath('//*[@itemprop = "articleBody"]//*/text()')
        except:
            body = ''

        try:
            date_time = response.selector.xpath('//*[@itemprop = "datePublished"]//@content')[0].extract()
            date = date_time.split('T')[0] 
            time = date_time.split('T')[1]
        except:
            date = ''
            time = ''

        try:
            section = response.selector.xpath('//*[@class = "headline-kicker"]//text()')[0].extract()
        except:
            section = ''

        try:
            authors = response.selector.xpath('//*[@itemprop = "author"]//*[@itemprop = "name"]//text()').extract()
            author = ', '.join(list(set(authors)))
        except:
            author = ''

        item = Item()
        item['title'] = title
        item['date'] = date
        item['time'] = time
        item['author'] = author
        item['newspaper'] = u'Washington Post'
        item['section'] = section
        item['url'] = url

        body_text = ''
        try:
            for text in body:
                body_text += text.extract() + ' '
        except: 
            pass

        item['body'] = body_text

        return item

            
    def parse_links(self, response):

        links = response.selector.xpath('//a[@class = "headline"]/@href').extract()
        for link in links:
            yield scrapy.Request(url = link, callback = self.parse)
