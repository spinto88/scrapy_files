import dryscrape
import time
import cPickle as pk
import datetime
from copy import deepcopy

#dryscrape.start_xvfb()
sess = dryscrape.Session()

init_date = datetime.date(2017,07,31)
        
while init_date <= datetime.date(2017,12,24):

    sess.visit('https://www.clarin.com/ediciones-anteriores/{}'\
               .format(str(init_date).replace('-','')))

    for i in range(50):

      sess.exec_script('window.scrollTo(0, document.body.scrollHeight);')
      time.sleep(2)

    links = sess.xpath('//article//*[@href]')
 
    hrefs = [link['href'] for link in links]

    fp = open('Clarin_links.txt', 'a')
    for href in hrefs:
        fp.write('{}\n'.format(href))
    fp.close()

    sess.reset()

    init_date += datetime.timedelta(1)

