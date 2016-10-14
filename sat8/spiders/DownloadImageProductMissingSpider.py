# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from sat8.items import ProductItem, ProductItemLoader

from time import gmtime, strftime
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse

# from sat8.Helpers.Google_Bucket import *
from sat8.Helpers.Functions import *

import urllib
import logging
import os
import re


sourceLinks = [
    'http://cellphones.com.vn/iphone-5s-16-gb-bh.html',
    'http://cellphones.com.vn/galaxy-note-4-cty.html',
    'http://cellphones.com.vn/mi-5-high-edition.html'
]


class DownloadImageProductMissingSpider(CrawlSpider):
    name = 'shit_spider'

    allowed_domains = []
    start_urls = []
    rules = ()

    def __init__(self):
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()

    def parse_item(self, response):
        link = response.url
        pil = ProductItemLoader(item = ProductItem(), response = response)

        pil.add_xpath('image', '//*[@id="image"]/@src')
        product = pil.load_item()

        # Ảnh chi tiết sản phẩm
        sel = Selector(response)
        images = sel.xpath('//*[@class="more-views"]/ul[1]/li/a/@href');
        image_urls = []
        dataImages = []

        for img in images:
            imgLink = response.urljoin(img.extract())
            image_urls.append(imgLink)
            dataImages.append(sha1FileName(imgLink))

        image_urls.append(product['image'])

        product['image'] = sha1FileName(product['image'])
        product['images'] = ',' . join(dataImages)

        query = "SELECT * FROM products WHERE link = %s"
        self.cursor.execute(query, (link))
        result = self.cursor.fetchone()

        if result:
            productId = result['id']
            sql = "UPDATE products SET image = %s, images = %s WHERE id = %s"
            self.cursor.execute(sql, (product['image'], product['images'], productId))
            self.conn.commit()

        # Download and push to bucket
        for image in  image_urls:

            imageName = sha1FileName(image)
            thumbs = downloadImageFromUrl(image)

            # Upload bucket
            # google_bucket_upload_object('static.giaca.org', thumbs['full'], 'uploads/full/' + imageName)
            # google_bucket_upload_object('static.giaca.org', thumbs['big'], 'uploads/thumbs/big/' + imageName)
            # google_bucket_upload_object('static.giaca.org', thumbs['small'], 'uploads/thumbs/small/' + imageName)


    def start_requests(self):
        for link in sourceLinks:
            request = scrapy.Request(url=link, callback=self.parse_item)
            yield request