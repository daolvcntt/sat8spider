# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sat8.items import RealEstateItem, RealEstateItemLoader
from time import gmtime, strftime
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse

from PIL import Image

import urllib

from sat8.Helpers.Google_Bucket import *
from sat8.Helpers.Functions import *

from sat8.Functions import getImageFromContent
from sat8.Functions import makeGzFile
from urlparse import urlparse

class BatDongSanSpider(CrawlSpider):
    name = "nhadat_spider"
    allowed_domains = []
    start_urls = [

    ]

    bucket = 'static.giaca.org'

    pathSaveImage = 'http://static.giaca.org/uploads/posts/'

    def __init__(self, env="production"):
        self.env = env

        for i in range(1, 6):
            url = 'http://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi/p' + str(i)
            self.start_urls.append(url);

    def parse(self, response):
        sel = Selector(response)

        blog_links = sel.xpath('//*[contains(@class, "search-productItem")]/div[@class="p-title"]/a[1]/@href')

        for href in blog_links:
            url = response.urljoin(href.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        image_links = []
        url_parts = urlparse(response.url)

        il = RealEstateItemLoader(item = RealEstateItem(), response=response)
        il.add_value('source', url_parts.netloc)
        il.add_value('source_link', response.url)
        il.add_xpath('title', '//*[@id="product-detail"]//h1[1]/text()')

        il.add_xpath('image', '//*[@id="product-detail"]//div[@class="img-map"]//img[1]/@src')
        il.add_xpath('content', '//*[@class="pm-content stat"]')
        il.add_xpath('content_text', '//*[@class="pm-content stat"]//text()');
        il.add_xpath('characters', '//*[@class="pm-content-detail"]');

        il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
        il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))

        item = il.load_item()
        item['images'] = []

        # Mô tả ngắn
        if 'content_text' in item:
            if len(item['content_text']) >= 245:
                item['teaser'] = item['content_text'][0:240]
            else:
                item['teaser'] = item['content_text']

        if 'image' in item:
            image_links.append(item['image'])

        selector = Selector(response)
        images = selector.xpath('//*[@id="thumbs"]//img/@src');

        dataImage = []
        for img in images:
            image = img.extract().replace('80x60', '745x510')
            image_links.append(image);

            item['images'].append(image)

        item['images'] = ',' . join(item['images'])



        if 'content' in item:
            # Replace something
            item['content'] = replace_link(item['content'])

        # Download image characters
        selector = Selector(response)
        images = selector.xpath('//*[@class="pm-content-detail"]//img/@src')
        for img in images:
            image_links.append(img.extract())

        item['images_array'] = image_links

        if self.env == 'dev':
            print item
            return

        yield(item)


    # def parse_start_url(self, response):
    #     print '------------------------------', "\n"
    #     print response.url
    #     yield scrapy.Request(response.url, callback=self.parse_item)
    #     print '------------------------------', "\n\n"
    #
