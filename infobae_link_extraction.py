import dryscrape
import time
import cPickle as pk
import datetime
from copy import deepcopy

dryscrape.start_xvfb()
sess = dryscrape.Session()

sections = ['politica', 'deportes', 'sociedad', 'economia']
        
for section in sections:

    sess.visit('https://www.infobae.com/{}/'.format(section))

    for i in range(100):

     try:
      button = sess.xpath('//div[@class="button pb-loadmore clear generic-results-list-load-more"]')[0]
      button.click()
      time.sleep(1)
     except:
      pass

    links = sess.xpath('//div[@class = "result-listing"]//*[@href]')
    
    hrefs = [link['href'] for link in links]

    fp = open('Infobae_links_{}.txt'.format(section),'a')
    for href in set(hrefs):
        fp.write('{}\n'.format(href))
    fp.close()

    sess.reset()

