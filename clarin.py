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
            title = response.selector.xpath('//*[@itemprop = "headline"]/@content')[0].extract()
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

        links = []

        import datetime
        init_date = datetime.date(2017,12,24)
        final_date = datetime.date(2018,2,4)

        while init_date <= final_date: 
            links += open('Clarin_links/Clarin_links_{}.txt'\
                           .format(init_date),'r').read().split('\n')
            init_date += datetime.timedelta(1)

        for link in set(links):
            yield scrapy.Request(url = 'http://www.clarin.com' + link, callback = self.parse, meta = {'dont_merge_cookies': True})


