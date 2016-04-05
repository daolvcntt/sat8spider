# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from AbstractPostSpider import AbstractPostSpider

class ZingSpider(AbstractPostSpider):
    name = "blog_spider"
    allowed_domains = ["news.zing.vn", ]

    config_urls = [
        {
            "url" : "http://news.zing.vn/cong-nghe/dien-thoai/trang[0-9]+.html",
            "max_page" : 2
        }
    ]

    configs = {
        "links" : '//*[@class="cate_content"]/article/header/h1/a/@href',
        'title' : '//*[@class="the-article-header"]/h1//text()',
        'teaser' : '//*[@class="the-article-summary"]//text()',
        'avatar' : '//*[@class="the-article-body"]//img[1]/@src',
        'content' : '//*[@class="the-article-body"]',
        'category' : '//*[contains(@class, "parent") and contains(@class, "current") and not(contains(@class, "homepage"))]/a[1]//text()',
        'type' : 'post'
    }
