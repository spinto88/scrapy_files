# -*- coding: utf-8 -*-
import scrapy

class Item(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    body = scrapy.Field()
    prefix = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    newspaper = scrapy.Field()
    section = scrapy.Field()
    tag = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()

class ClarinSpider(scrapy.Spider):
    name = "clarin"

    def start_requests(self):
        urls = []
        urls.append('https://www.clarin.com/')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links, meta = {'dont_merge_cookies': True})

    def parse(self, response):

        try:
            title = response.selector.xpath('//*[@itemprop = "headline"]/text()')[0].extract()
        except:
            title = ''

        try:
            subtitle = response.selector.xpath('//*[@itemprop = "description"]//*/text()')[0].extract()
        except:
            subtitle = ''

        try:
            body = response.selector.xpath('//*[@itemprop = "articleBody"]//*/text()')
        except:
            body = ''

        try:
            prefix = response.selector.xpath('//*[@class = "volanta"]/text()')[0].extract()
        except:
            prefix = ''
       
        try:
            date_time = response.selector.xpath('//*[@itemprop = "datePublished"]//@content')[0].extract()
            date = date_time.split(' ')[0] 
            time = date_time.split(' ')[1]
        except:
            date = ''
            time = ''

        try:
            author = response.selector.xpath('//*[@itemprop = "author"]/text()')[0].extract()
        except:
            author = ''

        try:
            section = response.selector.xpath('//*[@class = "header-section-name"]/text()')[0].extract()
        except:
            section = ''
        
        item = Item()
        item['title'] = title
        item['subtitle'] = subtitle
	item['prefix'] = prefix
	item['section'] = section
        item['author'] = author
        item['date'] = date
        item['time'] = time
        item['newspaper'] = u'Clarín'
	item['url'] = response.url


        body_text = ''
        try:
            for text in body:
                body_text += text.extract() + ' '
        except: 
            pass

        item['body'] = body_text

        return item

    
    def parse_links(self, response):

        links = open('Clarin_links.txt','r').read().split('\n')

        for link in set(links):
	    if '.html' in link:
                yield scrapy.Request(url = 'https://www.clarin.com' + link, callback = self.parse, meta = {'dont_merge_cookies': True})
    
