# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from items import ProductPriceItem, ProductItemLoader
from urlparse import urlparse
from time import gmtime, strftime
import urllib

from scrapy.conf import settings
import hashlib

conn = settings['MYSQL_CONN']
cursor = conn.cursor()


class ConvertImageSpider():

   text = ''

   def convertLinks(self, post):
      sel = Selector(text=self.getText())
      image_links = sel.xpath('//img/@src');
      for pl in image_links:
         url = pl.extract();
         imageName = hashlib.sha1(url).hexdigest() + '.jpg'
         urllib.urlretrieve(url, settings['IMAGES_STORE'] + '/posts/' + imageName)

   def setText(self, text):
      self.text = text

   def getText(self):
      return self.text


query = "SELECT * FROM posts"
cursor.execute(query)

posts = cursor.fetchall()

for post in posts:
   # print post['title']
   c = ConvertImageSpider()
   c.setText(post['content'])
   c.convertLinks(post)