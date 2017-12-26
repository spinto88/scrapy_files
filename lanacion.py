# -*- coding: utf-8 -*-

import scrapy
import datetime

init_date = "2017-11-06"
final_date = "2017-12-26"

init_date = datetime.datetime.strptime(init_date, "%Y-%m-%d").date()
final_date = datetime.datetime.strptime(final_date, "%Y-%m-%d").date()

# Ids de las notas tentativas: dentro de esta ventana solo se queda con las notas cuya fecha esta dentro dentro del intervalo de tiempo indicado
# Ver en la pagina...

init_id = 2079772
final_id = 2095430

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

class LaNacionSpider(scrapy.Spider):
    name = "lanacion"

    def start_requests(self):
        urls = []
        j = 0
        for i in range(init_id, final_id):
            urls.append('http://www.lanacion.com.ar/' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta = {'dont_merge_cookies': True})

    def parse(self, response):

        url = response.url

        try:
            date_time = response.selector.xpath('//div[@class = "fecha"]//@content')[0].extract()
            date = date_time.split(' ')[0] 
            time = date_time.split(' ')[1]
	
            date_aux = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if date_aux >= init_date and date_aux < final_date: 
                pass
            else:
                return None

        except:
            date = ''
            time = ''

        try:
            title = response.selector.xpath('//*[@itemprop = "headline"]//text()').extract()
            title = ' '.join(title)
        except:
            title = ''
	    return None

        try:
            subtitle = response.selector.xpath('//*[@itemprop = "description"]/text()').extract()
            subtitle = ' '.join(subtitle)
        except:
            subtitle = ''

        try:
            body = response.selector.xpath('//*[@itemprop = "articleBody"]//*/text()').extract()
            body = ' '.join(body)
        except:
            body = ''

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
        item['url'] = url

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

        item['body'] = body

        return item
