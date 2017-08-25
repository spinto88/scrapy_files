# -*- coding: utf-8 -*-
import scrapy
import datetime

class Item(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    newspaper = scrapy.Field()
    section = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()

class NYTSpider(scrapy.Spider):
    name = "nyt"

    def start_requests(self):
        urls = []

	init_date = datetime.date(2016, 1, 1)
	final_date = datetime.date(2017, 8, 1)

        while init_date < final_date:
            date_str = init_date.isoformat().split('-')
            url_name = 'http://www.nytimes.com/indexes/{}/{}/{}/todayspaper/index.html'.format(date_str[0], date_str[1], date_str[2])
            urls.append(url_name)
            init_date += datetime.timedelta(1)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links, meta = {'dont_merge_cookies': True})

    def parse(self, response):

        try:
            title = response.selector.xpath('//*[@itemprop = "headline"]/text()').extract()
            title = ' '.join(title)
        except:
            title = ''
            return None

        try:
            url = response.url
        except:
            url = ''

        try:
            body = response.selector.xpath('//p[@class = "story-body-text story-content"]//text()').extract()
            body_text = ' '.join(body)

        except:
            body_text = ''

        try:
            section = response.selector.xpath('//span[@class = "kicker-label"]//text()')[0].extract()
        except:
            section = ''

        try:
            date = response.selector.xpath('//time[@class = "dateline"]/@content')[0].extract()
            date = date.split('T')[0]
        except:
            date = ''

        try:
            authors = response.selector.xpath('//span[@class = "byline-author"]//text()').extract()
            author = ', '.join(list(set(authors)))
        except:
            author = ''

        item = Item()
        item['title'] = title
        item['body'] = body_text
        item['section'] = section
        item['date'] = date
        item['author'] = author
        item['url'] = url
        item['newspaper'] = 'NYTimes'

        return item

            
    def parse_links(self, response):

        links = response.selector.xpath('//div[@class = "story"]//div[@class = "thumbnail"]//@href').extract()
        links += response.selector.xpath('//div[@class = "columnGroup singleRule last"]//*[@href]/@href').extract()
        links += response.selector.xpath('//*[@class = "headlinesOnly multiline flush"]//*[@href]/@href').extract()

        for link in links:
            yield scrapy.Request(url = link, callback = self.parse, meta = {'dont_merge_cookies': True})
    
