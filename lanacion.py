# -*- coding: utf-8 -*-

import scrapy
import datetime

init_date = "2017-02-02"
final_date = "2018-02-05"

init_date = datetime.datetime.strptime(init_date, "%Y-%m-%d").date()
final_date = datetime.datetime.strptime(final_date, "%Y-%m-%d").date()

name2month = {'enero': 1, 'febrero': 2, 'marzo': 3,\
              'abril': 4, 'mayo': 5, 'junio': 6,\
              'julio': 7, 'agosto': 8, 'septiembre': 9,\
              'octubre': 10, 'noviembre': 11, 'diciembre': 12}


# Ids de las notas tentativas: dentro de esta ventana solo se queda con las notas cuya fecha esta dentro dentro del intervalo de tiempo indicado
# Ver en la pagina...

init_id = 2106600
final_id = 2106800

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
            date = response.selector.xpath('//section[@class = "fecha"]//text()')[0].extract()	
            date = date.split()
            date = "{}-{}-{}".format(date[4], name2month[date[2]], date[0]) 
            date_aux = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            date = date_aux
            if date_aux >= init_date and date_aux < final_date: 
                pass
            else:
                return None
            
        except:
            date = ''
            time = ''

        try:
            title = response.selector.xpath('//article//*[@class = "titulo"]//text()')[0].extract()
        except:
            title = ''

        """
        try:
            subtitle = response.selector.xpath('//*[@itemprop = "description"]/text()').extract()
            subtitle = ' '.join(subtitle)
        except:
            subtitle = ''
        """
        try:
            body = response.selector.xpath('//section[@id = "cuerpo"]//p//text()').extract()
            body = ' '.join(body)
            body = body.replace('\r', '')
            body = body.replace('\n', '')

        except:
            body = ''

        try:
            section = response.selector.xpath('//*[@class = "categoria"]//a//text()')[0].extract()
            section = section.replace(' ', '')
            section = section.replace('\r', '')
            section = section.replace('\n', '')
        except:
            section = ''

        try:
            author = response.selector.xpath('//section[@class = "autor"]//a//text()')[0].extract()
        except:
            author = ''

        item = Item()
        item['title'] = title
#        item['subtitle'] = subtitle
        item['date'] = date
#        item['time'] = time
        item['author'] = author
        item['url'] = url
        item['newspaper'] = u'LaNación'

        item['section'] = section

        try:
            item['tag'] = names[2].extract()
        except:
            item['tag'] = ''

        item['body'] = body

        return item
