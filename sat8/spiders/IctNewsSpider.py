# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from AbstractPostSpider import AbstractPostSpider

class IctNewsSpider(AbstractPostSpider):
    allowed_domains = ["ictnews.vn"]
    start_urls = [ 'http://ictnews.vn/the-gioi-so/di-dong', 'http://ictnews.vn/the-gioi-so/may-tinh']

    rules = (
        Rule (LinkExtractor(allow=('http://ictnews.vn/the-gioi-so/di-dong/trang-[0-9]+')),  callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://ictnews.vn/the-gioi-so/may-tinh/trang-[0-9]+')),  callback='parse_item', follow= True),
    )

    configs = {
        'links' : '//*[@id="listArticles"]/div/a[1]/@href',
        'title' : '//*[@class="article-brand"]/h1[1]//text()',
        'teaser' : '//*[@class="article-brand"]//h2[@class="pSapo"]//text()',
        'avatar' : '//*[@class="content-detail"]//img[1]/@src',
        'content' : '//*[@class="content-detail"]',
        'category' : '//*[@class="article-brand"]//a[@class="channelname"]/text()',
        'type' : 'post'
    }