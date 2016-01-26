# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from AbstractPostSpider import AbstractPostSpider


class GenkSpider(AbstractPostSpider):
    allowed_domains = ["genk.vn"]
    start_urls = [

    ]

    config_urls = [
        {
            "url" : "http://genk.vn/may-tinh-bang/page-[0-9]+.chn",
            "max_page" : 10
        },
    ]

    configs = {
        'links' : '//*[@class="list-news-status pt5 pr10"]/h2[1]/a/@href',
        'title' : '//*[@class="news-showtitle mt10"]/h1[1]//text()',
        'teaser' : '//*[@class="init_content oh"]//text()',
        'avatar' : '//*[@class="VCSortableInPreviewMode"]/div[1]/img/@src',
        'content' : '//*[@id="ContentDetail"]',
        'category' : '//*[@id="sub_title"]//text()',
        'type' : 'blog'
    }