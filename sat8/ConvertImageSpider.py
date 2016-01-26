# -*- coding: utf-8 -*-
# Download toàn bộ ảnh từ phần nội dung post
# Chú ý: Chỉ chạy 1 lần khi cần thiết
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from items import ProductPriceItem, ProductItemLoader
from urlparse import urlparse
from time import gmtime, strftime
import urllib

from scrapy.conf import settings
import hashlib

import gzip
import shutil
import os

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
         try:
            filePath = settings['IMAGES_STORE'] + '/posts/' + imageName
            filePathGzip = filePath + '.gz';
            if os.path.isfile(filePath) == False or os.path.isfile(filePathGzip) == False:
               urllib.urlretrieve(url, filePath)

               with open(filePath , 'rb') as f_in, gzip.open(filePathGzip, 'wb') as f_out:
                  shutil.copyfileobj(f_in, f_out)

               print url

         except IOError, e:
            print e

      query = "UPDATE posts set has_image_content = 1 WHERE id = %s"
      cursor.execute(query, (post['id']))

   def setText(self, text):
      self.text = text

   def getText(self):
      return self.text


query = "SELECT * FROM posts"
cursor.execute(query)

posts = cursor.fetchall()

for post in posts:
   # print post['title']
   if post['has_image_content'] != 1:
      c = ConvertImageSpider()
      c.setText(post['content'])
      c.convertLinks(post)