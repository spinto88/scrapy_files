import dryscrape
import time
import cPickle as pk
import datetime
from copy import deepcopy

sess = dryscrape.Session()

sections = ['politica/']#, 'mundo/', 'sociedad/', 'economia/', 'policiales/']

first_date = "2017-8-1"
first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d").date()
        
for section in sections:

    sess.visit('https://www.clarin.com/{}'.format(section))

    date_min = deepcopy(first_date)

    try:
     for i in range(10):

      sess.exec_script('window.scrollTo(0, document.body.scrollHeight);')
      time.sleep(1)

      dates_info = sess.xpath('//div[@class = "box-notas"]//article//*[@class = "fecha"]')

      dates_aux = [[daux.split('.') for daux in d.text().split(' ')] \
                                      for d in dates_info] 
      dates = []
      for d in dates_aux:
          try:
              dates.append(datetime.datetime.strptime('-'.join(d[1]), '%d-%m-%Y').date())
          except:
              try:
                dates.append(datetime.datetime.strptime('-'.join(d[0]), '%d-%m-%Y').date())
              except:
                dates.append(datetime.datetime.today().date())

      date_min = min(set(dates))

      links = sess.xpath('//div[@class = "box-notas"]//article//*[@href]')
    
      hrefs = [link['href'] for link in links]

      fp = open('Clarin_links.txt','a')
      for href in hrefs:
          fp.write('{}\n'.format(href))
      fp.close()

    except:
     pass

    sess.reset()

