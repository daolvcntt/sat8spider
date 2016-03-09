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

    config_urls = [
        # {
        #     "url" : "http://news.zing.vn/cong-nghe/dien-thoai/trang[0-9]+.html",
        #     "max_page" : 10
        # }
    ]

    configs = {
        # "links" : '//*[@class="cate_content"]/article/header/h1/a/@href',
        # 'title' : '//*[@class="the-article-header"]/h1//text()',
        # 'teaser' : '//*[@class="the-article-summary"]//text()',
        # 'avatar' : '//*[@class="the-article-body"]//img[1]/@src',
        # 'content' : '//*[@class="the-article-body"]',
        # 'category' : '//*[contains(@class, "parent") and contains(@class, "current") and not(contains(@class, "homepage"))]/a[1]//text()',
        # 'type' : 'post'
    }

    def __init__(self):
        # Add start_urls
        config_urls = self.config_urls
        for url in config_urls:
            if url["max_page"] > 0:
                for i in range(1, url["max_page"]):
                    self.start_urls.append(url["url"].replace('[0-9]+', str(i)))
            else:
                self.start_urls.append(url["url"])

    def parse(self, response):
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

        il.add_value('category_id', 1)

        if 'category' in self.configs:
            il.add_xpath('category', self.configs['category']);
        else:
            if 'category_value' in self.configs:
                il.add_value('category', self.configs['category_value'].decode('utf-8'))

            if 'category_id' in self.configs:
                il.add_value('category_id', self.configs['category_id'])

        il.add_xpath('content', self.configs['content'])

        il.add_value('product_id', 0)
        il.add_value('user_id', 1)

        il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
        il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))
        il.add_value('post_type', self.configs['type'])

        item = il.load_item()

        item['typ'] = 'blog'

        if 'avatar' in item:
            item['image_urls'] = [il.get_value(item['avatar'])]
            item['avatar'] = hashlib.sha1(il.get_value(item['avatar'].encode('utf-8'))).hexdigest() + '.jpg'


        # print item
        # return

        yield(item)


    # def parse_start_url(self, response):
    #     print '------------------------------', "\n"
    #     print response.url
    #     yield scrapy.Request(response.url, callback=self.parse_item)
    #     print '------------------------------', "\n\n"
