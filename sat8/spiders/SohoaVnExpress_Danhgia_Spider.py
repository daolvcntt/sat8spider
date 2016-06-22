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
            "url" : "http://sohoa.vnexpress.net/danh-gia",
            "max_page" : 5
        },
        {
            "url" : "http://sohoa.vnexpress.net/danh-gia/dien-thoai",
            "max_page" : 5
        },
        {
            "url" : "http://sohoa.vnexpress.net/danh-gia/laptop",
            "max_page" : 5
        }
    ]

    configs = {
        "links" : '//*[@class="list_news"]//h2[@class="title_news"]/a[1]/@href',
        'title' : '//*[@class="title_news"]/h1//text()',
        'teaser' : '//*[@class="short_intro txt_666"]//text()',
        'avatar' : '//*[@id="detail_danhgia"]//img[1 or 2 or 3 or 4]/@src',
        'content' : '//*[@class="content_danhgia_chitiet"]',
        'category_value' : 'Đánh giá',
        'category_id' : 2,
        'type' : 'review'
    }
