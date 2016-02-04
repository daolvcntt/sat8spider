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

import settings
import hashlib

import gzip
import shutil
import os

from Functions import makeGzFile

conn = settings.MYSQL_CONN
cursor = conn.cursor()

# urllib.urlretrieve('http://res.vtc.vn/media/vtcnews/2014/07/17/di_dong1.jpg', settings['IMAGES_STORE'] + '/posts/a.jpg');


class DownloadImageContentPost():

   text = ''

   def convertLinks(self, post):
      sel = Selector(text=self.getText())
      image_links = sel.xpath('//img/@src');
      for pl in image_links:
         url = pl.extract();
         imageName = hashlib.sha1(url).hexdigest() + '.jpg'
         try:
            filePath = settings.IMAGES_STORE + '/posts/' + imageName
            filePathGzip = filePath + '.gz';
            if os.path.isfile(filePath) == False or os.path.isfile(filePathGzip) == False:
               urllib.urlretrieve(url, filePath)

               # Make gz file
               makeGzFile(filePath)

            print url

         except IOError, e:
            print e

      query = "UPDATE posts set has_image_content = 1 WHERE id = %s"
      cursor.execute(query, (post['id']))
      conn.commit()

   def setText(self, text):
      self.text = text

   def getText(self):
      return self.text


query = "SELECT * FROM posts WHERE has_image_content != 1 ORDER BY updated_at DESC"
cursor.execute(query)

posts = cursor.fetchall()

for post in posts:

   c = DownloadImageContentPost()
   c.setText(post['content'])
   c.convertLinks(post)