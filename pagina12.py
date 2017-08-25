# -*- coding: utf-8 -*-

import scrapy
import datetime

init_date = "2017-01-01"
final_date = "2017-08-01"

init_date = datetime.datetime.strptime(init_date, "%Y-%m-%d").date()
final_date = datetime.datetime.strptime(final_date, "%Y-%m-%d").date()

# Ids de las notas tentativas: dentro de esta ventana solo se queda con las notas cuya fecha esta dentro dentro del intervalo de tiempo indicado
# Ver en la pagina...

init_id = 0
final_id = 55100


class Item(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    newspaper = scrapy.Field()
    section = scrapy.Field()
    prefix = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()

class Pagina12Spider(scrapy.Spider):
    name = "pagina12"

    def start_requests(self):
        urls = []
        for i in range(init_id, final_id):
            urls.append('http://www.pagina12.com.ar/' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta = {'dont_merge_cookies': True})

    def parse(self, response):

        try:
            date = response.selector.xpath('//div[@class = "time"]//*[@datetime]/@datetime')[0].extract()
            date_aux = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if date_aux >= init_date and date_aux < final_date:
                pass
            else:
                return None
        except:
            date = ''

        try:
            title = response.selector.xpath('//div[@class = "article-title"]/text()')[0].extract()
        except:
            title = ''
	    return None

        url = response.url

        try:
            subtitle = response.selector.xpath('//div[@class = "article-summary"]/text()')[0].extract()
        except:
            subtitle = ''

        try:
            subtitle = response.selector.xpath('//div[@class = "article-summary"]/text()')[0].extract()
        except:
            subtitle = ''

        try:
            prefix = response.selector.xpath('//div[@class = "article-prefix"]/text()')[0].extract()
        except:
            prefix = ''

        try: 
            body = response.selector.xpath('//div[@class = "article-text"]//text()')
	    body_text = ''
            for text in body:
                body_text += text.extract() + ' '

        except: 
            body = ''

        try:
            section = response.selector.xpath('//div[@class = "suplement"]//text()')[0].extract()
        except:
            section = ''

        try:
            author = response.selector.xpath('//div[@class = "article-author"]//a/text()')[0].extract()
        except:
            author = ''

        item = Item()
        item['title'] = title
        item['subtitle'] = subtitle
        item['date'] = date
        item['newspaper'] = u'Página12'
        item['section'] = section
	item['body'] = body_text
        item['prefix'] = prefix
        item['author'] = author
        item['url'] = url

        return item
