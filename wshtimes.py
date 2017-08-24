# -*- coding: utf-8 -*-
import scrapy
import datetime
import calendar

class Item(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    newspaper = scrapy.Field()
    section = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()

class WSHTSpider(scrapy.Spider):
    name = "wsht"

    def start_requests(self):
        urls = []

	init_date = datetime.date(2016, 1, 1)
	final_date = datetime.date(2017, 8, 1)

        while init_date < final_date:
            url_name = 'http://www.washingtontimes.com/news/{}/{}/{}/'.format(init_date.year, calendar.month_abbr[init_date.month].lower(), init_date.day)
            for page in range(10):
                urls.append(url_name + '?page={}'.format(page))
            init_date += datetime.timedelta(1)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links, meta = {'dont_merge_cookies': True})

    def parse(self, response):

        try:
            title = response.selector.xpath('//div[@id="page-title-container"]//text()')[0].extract()
        except:
            title = ''

        try:
            url = response.url
        except:
            url = ''
        
        try:
            body = response.selector.xpath('//div[@class="bigtext"]//p//text()').extract()
            body_text = ' '.join(body)
        except:
            body_text = ''
        
        try:
            section = response.selector.xpath('//ul[@class = "menu"]//li//text()')[0:3].extract()
            section = '/'.join(section)
        except:
            section = ''
        
        try:
            date = response.selector.xpath('//span[@class = "source"]//text()').extract()
        except:
            date = ''

        try:
            author = response.selector.xpath('//div[@class = "article-text"]/div[@class = "meta"]/span[@class = "byline"]//text()').extract()
            author = ''.join(author)
        except:
            author = ''
        
        item = Item()
        item['title'] = title
        item['author'] = author
        item['body'] = body_text
        item['section'] = section
        item['date'] = date
        item['url'] = url
        item['newspaper'] = 'WSHTimes'
        
        if 'staff/' in response.url or title == '':
            return None
        else:
            return item

            
    def parse_links(self, response):

        links = response.selector.xpath('//*[@class="article-headline"]/a[@href]/@href').extract()

        for link in links:
            yield scrapy.Request(url = 'http://www.washingtontimes.com' + link, callback = self.parse, meta = {'dont_merge_cookies': True})
    
