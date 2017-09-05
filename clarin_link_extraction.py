import dryscrape
import time
import cPickle as pk
import datetime
from copy import deepcopy

dryscrape.start_xvfb()
sess = dryscrape.Session()

sections = ['politica', 'mundo', 'sociedad', 'economia', 'policiales']
        
for section in sections:

    sess.visit('https://www.clarin.com/{}/'.format(section))

    for i in range(100):

      sess.exec_script('window.scrollTo(0, document.body.scrollHeight);')
      time.sleep(1)

    links = sess.xpath('//div[@class = "box-notas"]//article//*[@href]')
    
    hrefs = [link['href'] for link in links]

    fp = open('Clarin_links_{}.txt'.format(section),'a')
    for href in hrefs:
        fp.write('{}\n'.format(href))
    fp.close()

    sess.reset()

