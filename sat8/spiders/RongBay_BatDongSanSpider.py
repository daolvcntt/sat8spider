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
from slugify import slugify

import urllib
import html2text
import json

# from sat8.Helpers.Google_Bucket import *
from sat8.Helpers.Functions import *

from sat8.Functions import getImageFromContent
from sat8.Functions import makeGzFile
from urlparse import urlparse


rules = [
    {
        "url": "http://rongbay.com/Ha-Noi/Can-ho-chung-cu-Mua-Ban-nha-dat-c15-t5-trang@page@.html",
        "max_page": 10
    },
    {
        "url": "http://rongbay.com/Ha-Noi/Biet-thu-lien-ke-phan-lo-Mua-Ban-nha-dat-c15-t1-trang@page@.html",
        "max_page": 10
    },
    {
        "url": "http://rongbay.com/Ha-Noi/Nha-mat-pho-Mua-Ban-nha-dat-c15-t639-trang@page@.html",
        "max_page": 10
    },
    {
        "url": "http://rongbay.com/Ha-Noi/Cua-hang-mat-bang-Mua-Ban-nha-dat-c15-t2-trang@page@.html",
        "max_page": 10
    },
    {
        "url": "http://rongbay.com/Ha-Noi/Dat-o-Mua-Ban-nha-dat-c15-t626-trang@page@.html",
        "max_page": 10
    }
]


class RongBay_BatDongSanSpider(CrawlSpider):
    name = "nhadat_spider"
    allowed_domains = []
    start_urls = [

    ]

    bucket = 'static.giaca.org'

    pathSaveImage = 'http://static.giaca.org/uploads/full/'

    def __init__(self, env="production"):
        self.env = env

        for rule in rules:
            for i in range(rule["max_page"], 0, -1):
                url = rule["url"].replace('@page@', str(i))
                self.start_urls.append(url)

    def parse(self, response):
        sel = Selector(response)

        blog_links = sel.xpath('//*[contains(@class, "rd_view newsTitle title_vip_item itemVip")]/@href')

        for href in blog_links:
            url = response.urljoin(href.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        image_links = []
        url_parts = urlparse(response.url)

        il = RealEstateItemLoader(item = RealEstateItem(), response=response)
        il.add_value('source', url_parts.netloc)
        il.add_value('source_link', response.url)
        il.add_xpath('title', '//*[@class="detail_title color333 font_26"]/text()')
        il.add_value('placement', '.');

        il.add_xpath('image', '//*[@class="content_input_editior"]//img[1]/@src')
        il.add_xpath('content', '//*[@class="content_input_editior"]')
        il.add_xpath('content_text', '//*[@class="content_input_editior"]//text()')
        il.add_value('characters', '[]')


        il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
        il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))

        il.add_value('type', 0);

        item = il.load_item()

        keyword = []

        tags = {}

        item['json_tags'] = '[]'

        item['images'] = []
        # return

        # Mô tả ngắn
        if 'content_text' in item:
            if len(item['content_text']) >= 245:
                item['teaser'] = item['content_text'][0:240]
            else:
                item['teaser'] = item['content_text']

        if 'image' in item:
            image_links.append(item['image'])

        # Download image content
        selector = Selector(response)
        images = selector.xpath('//*[@class="content_input_editior"]//img/@src');

        dataImage = []
        for img in images:
            image = img.extract()
            image_links.append(image);

            dataImage.append(sha1FileName(image))

        item['images'] = ',' . join(dataImage)


        if 'content' in item:
            # Replace something
            item['content'] = replace_link(item['content'])
            item['content'] = replace_image(item['content'], self.pathSaveImage)


        item['images_array'] = image_links

        if 'title' in item:
            keyword.append(item['title'])

        if 'placement' in item:
            item['placement'] = replace_link(item['placement'])
            item['placement_text'] = html2text.html2text(item['placement'])
            keyword.append(item['placement_text'])

        item['all_keyword'] = ' ' . join(keyword)

        item['all_keyword_lower'] = item['all_keyword'].lower()

        item['all_keyword_lower_no_accent'] = slugify(item['all_keyword_lower'])
        item['all_keyword_lower_no_accent'] = item['all_keyword_lower_no_accent'].replace('-', ' ')

        item['image_links'] = image_links

        if 'image' in item:
            item['image'] = sha1FileName(item['image'])

        if 'image' not in item:
            item['image'] = ''

        if self.env == 'dev':
            item['image_links'] = []

        yield(item)


    # def parse_start_url(self, response):
    #     print '------------------------------', "\n"
    #     print response.url
    #     yield scrapy.Request(response.url, callback=self.parse_item)
    #     print '------------------------------', "\n\n"
    #
