# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from sat8.items import RaovatItem, RaovatItemLoader

from sat8.Classifields.EsRaovat import EsRaovat

from time import gmtime, strftime
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse

from sat8.Helpers.Google_Bucket import *
from sat8.Helpers.Functions import *

import urllib
import logging
import os
import re


class ChototSpider(CrawlSpider):
    name = "raovat_spider"

    bucket = 'static.giaca.org'

    pathSaveImage = 'http://static.giaca.org/uploads/full/'

    allowed_domains = ['chotot.com']

    questionId = 0
    productId = 0;

    def __init__(self):
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()


    def parse_item(self, response):

        sel = Selector(response)
        product_links = sel.xpath('//*[@class="listing-rows"]//div[@class="thumbs_subject"]//a[@class="ad-subject"][1]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            request = scrapy.Request(url, callback=self.parse_raovat)
            request.meta['productId'] = response.meta['productId']
            yield request


    def parse_raovat(self, response):
        productId = response.meta['productId']
        raovatItemLoader = RaovatItemLoader(item = RaovatItem(), response = response)
        raovatItemLoader.add_xpath('title', '//*[@class="adview_subject"]/h2//text()')
        raovatItemLoader.add_value('link', response.url)
        raovatItemLoader.add_value('is_crawl', 1)
        raovatItemLoader.add_xpath('user_name', '//*[@class="advertised_user"]/text()')
        raovatItemLoader.add_xpath('price', '//*[@class="price"]//span[@itemprop="price"]/text()')
        raovatItemLoader.add_xpath('teaser', 'string(//*[@class="view_content"])')
        raovatItemLoader.add_xpath('content', '//*[@class="view_content"]')
        raovatItemLoader.add_xpath('info', '//*[@class="adparams_div"]')
        raovatItemLoader.add_xpath('image', '//*[@id="display_image"]//img[1]/@src')
        raovatItemLoader.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
        raovatItemLoader.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))
        raovatItemLoader.add_value('source', 'chotot.com')
        raovatItemLoader.add_xpath('phone', '//*[@id="real-phone"]/@src')

        raovatItem = raovatItemLoader.load_item()
        # raovatItem['link'] = 'http://vatgia.com' + raovatItem['link'];
        raovatItem['hash_link'] = hashlib.md5(raovatItem['link']).hexdigest()

        if 'user_name' not in raovatItem:
            raovatItem['user_name'] = ''

        if 'price' not in raovatItem:
            raovatItem['price'] = 0

        if 'teaser' not in raovatItem:
            raovatItem['teaser'] = ''

        if 'content' not in raovatItem:
            raovatItem['content'] = ''

        raovatItem['teaser'] = raovatItem['teaser'][0:250]

        # Download image
        image_links = []
        selector = Selector(response)
        images = selector.xpath('//*[@id="main_description"]//img/@src')
        for image in images:
            imgLink = response.urljoin(image.extract())
            image_links.append(imgLink)

        if 'image' in raovatItem:
            image_links.append(raovatItem['image'])
            avatar = sha1FileName(raovatItem['image'])
            raovatItem['image'] = self.pathSaveImage + avatar
        else:
            raovatItem['image'] = ''

        if 'phone' in raovatItem:
            image_links.append(raovatItem['phone'])
            phone = sha1FileName(raovatItem['phone'])
            raovatItem['phone'] = phone
        else:
            raovatItem['phone'] = ''

        # Replace something
        raovatItem['content'] = replace_link(raovatItem['content'])
        raovatItem['content'] = replace_image(raovatItem['content'], self.pathSaveImage)
        raovatItem['image_links'] = image_links

        query = "SELECT id,link FROM classifields WHERE hash_link = %s"
        self.cursor.execute(query, (raovatItem['hash_link']))
        result = self.cursor.fetchone()

        raovatId = 0;
        if result:
            raovatId = result['id']
            sql = "UPDATE classifields SET content = %s, image = %s, phone = %s, source = %s, info = %s, updated_at = %s WHERE id = %s"
            self.cursor.execute(sql, (raovatItem['content'], raovatItem['image'], raovatItem['phone'], raovatItem['source'], raovatItem['info'] , raovatItem['updated_at'] ,raovatId))
            self.conn.commit()
            logging.info("Item already stored in db: %s" % raovatItem['link'])
        else:
            sql = "INSERT INTO classifields (product_id, title, teaser, content, user_name, image, info, is_crawl, price, link, hash_link, phone, source, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (productId, raovatItem['title'], raovatItem['teaser'], raovatItem['content'], raovatItem['user_name'], raovatItem['image'], raovatItem['info'] , raovatItem['is_crawl'] ,raovatItem['price'], raovatItem['link'], raovatItem['hash_link'] ,raovatItem['phone'], raovatItem['source'], raovatItem['created_at'], raovatItem['updated_at']))
            self.conn.commit()
            logging.info("Item stored in db: %s" % raovatItem['link'])
            raovatId = self.cursor.lastrowid

        raovatItem["id"] = raovatId
        # Insert elasticsearch
        esRaovat = EsRaovat()
        esRaovat.insertOrUpdate(raovatId, raovatItem.toJson())

        yield raovatItem


    def start_requests(self):
        print '------------------------------', "\n"
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT DISTINCT id,keyword,rate_keyword FROM products WHERE rate_keyword != '' OR rate_keyword != NULL ORDER BY updated_at DESC")
        products = self.cursor.fetchall()

        # url = 'http://vatgia.com/raovat/quicksearch.php?keyword=Sony+Xperia+Z3'
        # request = scrapy.Request(url, callback = self.parse_item)
        # request.meta['productId'] = 0
        # yield request

        for product in products:
            url = 'https://www.chotot.com/ha-noi/mua-ban/%s' %product['rate_keyword']
            # self.start_urls.append(url)
            request = scrapy.Request(url, callback = self.parse_item)
            request.meta['productId'] = product['id']
            yield request

        for product in products:
            url = 'https://www.chotot.com/tp-ho-chi-minh/mua-ban/%s' %product['rate_keyword']
            # self.start_urls.append(url)
            request = scrapy.Request(url, callback = self.parse_item)
            request.meta['productId'] = product['id']
            yield request

        # yield scrapy.Request(response.url, callback=self.parse_item)
        print '------------------------------', "\n\n"
