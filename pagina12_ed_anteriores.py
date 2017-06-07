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

class Pagina12_ea(scrapy.Spider):
    name = "pagina12_ea"

    def start_requests(self):
        urls = []

	init_date = datetime.date(2003, 1, 1)
	final_date = datetime.date(2016, 12, 31)

        while init_date <= final_date:
            date_str = init_date.isoformat().split('-')
            url_name = 'http://www.pagina12.com.ar/diario/principal/diario/index-{}-{}-{}.html'.format(date_str[0], date_str[1], date_str[2])
            urls.append(url_name)
            init_date += datetime.timedelta(1)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links)

    def parse(self, response):

        try:
            title = response.selector.xpath('//div[@class = "nota top12"]/h2/text()')[0].extract()
        except:
            title = ''

        try:
            url = response.url
        except:
            url = ''

        try:
            subtitle = response.selector.xpath('//p[@class = "intro"]//text()')[0].extract()
        except:
            subtitle = ''

        try:
            body = response.selector.xpath('//div[@id = "cuerpo"]//text()').extract()
            body_text = ''
            for text in body:
                body_text += text
        except:
            body_text = ''

        try:
            section = response.selector.xpath('//p[@class="volanta"]//text()')[0].extract()
        except:
            section = ''

        try:
            prefix = response.selector.xpath('//p[@class="volanta"]//text()')[1].extract()
        except:
            prefix = ''

        try:
            date = response.selector.xpath('//span[@class = "fecha_edicion"]/text()')[0].extract()
        except:
            date = ''

        try:
            author = response.selector.xpath('//p[@class="autor"]//text()')[0].extract()
            author = author.split('Por ')[1]
        except:
            author = ''

        item = Item()
        item['title'] = title
        item['subtitle'] = subtitle
        item['body'] = body_text
        item['section'] = section
        item['date'] = date
        item['author'] = author
        item['newspaper'] = u'Página12'
        item['url'] = url

        return item

            
    def parse_links(self, response):

        links = response.selector.xpath('//a[@class = "cprincipal"]/@href').extract()

        for link in links:
            yield scrapy.Request(url = 'http://www.pagina12.com.ar' + link, callback = self.parse)
    
