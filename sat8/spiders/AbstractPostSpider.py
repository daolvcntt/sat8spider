# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sat8.items import BlogItem, PostItemLoader
from time import gmtime, strftime
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse

class AbstractPostSpider(CrawlSpider):
    name = "blog_spider"
    allowed_domains = []
    start_urls = []

    rules = ()

    # def parse(self, response):
    #     return self.parse_item(response)

    def parse_item(self, response):
        sel = Selector(response)

        blog_links = sel.xpath(self.configs['links'])

        for href in blog_links:
            url = response.urljoin(href.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        il = PostItemLoader(item = BlogItem(), response=response)
        il.add_value('link', response.url)
        il.add_xpath('title', self.configs['title'])
        il.add_xpath('teaser', self.configs['teaser'])
        il.add_xpath('avatar', self.configs['avatar'])
        il.add_xpath('category', self.configs['category']);
        il.add_xpath('content', self.configs['content'])
        il.add_value('category_id', 1)
        il.add_value('product_id', 0)
        il.add_value('user_id', 1)

        il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
        il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))
        il.add_value('post_type', self.configs['type'])

        item = il.load_item()

        item['typ'] = 'blog'

        if 'avatar' in item:
            item['image_urls'] = [il.get_value(item['avatar'])]
            item['avatar'] = hashlib.sha1(il.get_value(item['avatar'])).hexdigest() + '.jpg'


        # print item
        # return

        yield(item)
