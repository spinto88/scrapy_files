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

class InfobaeSpider(scrapy.Spider):
    name = "infobae"

    def start_requests(self):
        urls = []
        urls.append('http://www.infobae.com/')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links, meta = {'dont_merge_cookies': True})

    def parse(self, response):

        try:
            title = response.selector.xpath('//header[@class = "article-header hed-first col-sm-12"]/h1/text()')[0].extract()
        except:
            title = ''

        try:
            subtitle = response.selector.xpath('//span[@class = "subheadline"]/text()')[0].extract()
        except:
            subtitle = ''

        try:
            body = response.selector.xpath('//p[@class = "element element-paragraph"]//text()').extract()
        except:
            body = ''

        try:
            aux = response.url.split('/')
            date = "{}-{}-{}".format(aux[4], aux[5], aux[6])
        except:
            date = ''

        try:
            author = response.selector.xpath('//div[@class = "byline-author"]//b//text()')[0].extract()
        except:
            author = ''

        try:
            section = response.selector.xpath('//header[@class = "article-header hed-first col-sm-12"]//a/text()')[0].extract()
        except:
            section = ''
        
        item = Item()
        item['title'] = title
        item['subtitle'] = subtitle
	item['section'] = section
        item['author'] = author
        item['date'] = date
        item['newspaper'] = u'Infobae'
	item['url'] = response.url


        body_text = ' '.join(body)
        item['body'] = body_text

        return item

    
    def parse_links(self, response):

        links = []
 	for section in ['politica', 'sociedad', 'deportes', 'economia']:

            links += open('Infobae_links_{}.txt'.format(section), 'r').\
                                                      read().split('\n')

        for link in set(links):
	    if '.html' in link:
                yield scrapy.Request(url = 'https://www.infobae.com' + link, callback = self.parse, meta = {'dont_merge_cookies': True})
    
