# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from AbstractPostSpider import AbstractPostSpider

class GenkReviewSpider(AbstractPostSpider):

    allowed_domains = ["genk.vn"]

    config_urls = [
        {
            "url" : "http://genk.vn/review/page-[0-9]+.htm",
            "max_page" : 2
        }
    ]

    configs = {
        'links' : '//*[@class="list-news-other nob"]/li/h3[1]/a/@href',
        'title' : '//*[@class="news-showtitle mt10"]/h1[1]//text()',
        'teaser' : '//*[@class="init_content oh"]//text()',
        'avatar' : '//*[@class="VCSortableInPreviewMode"]/div[1]/img/@src',
        'content' : '//*[@id="ContentDetail"]',
        'category' : '//*[@id="sub_title"]//text()',
        'type' : 'review'
    }