# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from AbstractPostSpider import AbstractPostSpider

class SohoaVnExpress_Danhgia_Spider(AbstractPostSpider):
    name = "blog_spider"
    allowed_domains = ["sohoa.vnexpress.net", ]

    config_urls = [
        {
            "url" : "http://sohoa.vnexpress.net/danh-gia/page/[0-9]+.html",
            "max_page" : 15
        },
        {
            "url" : "http://sohoa.vnexpress.net/danh-gia/dien-thoai/page/[0-9]+.html",
            "max_page" : 15
        },
        {
            "url" : "http://sohoa.vnexpress.net/danh-gia/laptop/page/[0-9]+.html",
            "max_page" : 15
        },
        {
            "url" : "http://sohoa.vnexpress.net/danh-gia/may-anh/page/[0-9]+.html",
            "max_page": 15
        }
    ]

    configs = {
        "links" : '//*[@class="list_news"]//h2[@class="title_news"]/a[1]/@href',
        'title' : '//*[@class="title_news"]/h1//text()',
        'teaser' : '//*[@class="short_intro txt_666"]//text()',
        'avatar' : '//*[@class="width_common space_bottom_20"]//img[1 or 2 or 3 or 4]/@src',
        'content' : '//*[@class="content_danhgia_chitiet"][1]',
        'category_value' : 'Đánh giá',
        'category_id' : 2,
        'type' : 'review'
    }
