# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class HoangphatvnSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['hoangphatvn.vn']
    start_urls = [
        'http://hoangphatvn.vn/dell.html#.VukjYib9rVM',
        'http://hoangphatvn.vn/asus.html#.Vukj1yb9rVM',
        'http://hoangphatvn.vn/hp.html#.Vukj9ib9rVM',
        'http://hoangphatvn.vn/acer.html#.VukkBCb9rVM',
        'http://hoangphatvn.vn/lenovo-33.html#.VukkDSb9rVM',
        'http://hoangphatvn.vn/msi-405.html#.VukkGCb9rVM',

        'http://hoangphatvn.vn/apple-71.html#.VukkKSb9rVM',
        'http://hoangphatvn.vn/samsung-72.html#.VukkNSb9rVM',
        'http://hoangphatvn.vn/microsoft.html',
        'http://hoangphatvn.vn/sony.html',
        'http://hoangphatvn.vn/htc.html',
        'http://hoangphatvn.vn/lenovo-76.html',
        'http://hoangphatvn.vn/oppo.html',
        'http://hoangphatvn.vn/asus-358.html',
        'http://hoangphatvn.vn/masscom.html',
        'http://hoangphatvn.vn/motorola-476.html',
        'http://hoangphatvn.vn/xiaomi.html',
        'http://hoangphatvn.vn/q-mobile.html',
        'http://hoangphatvn.vn/wiko.html',
        'http://hoangphatvn.vn/loai-khac-457.html'
    ]

    rules = (

    )

    configs = {
        'product_links' : '//*[@class="img-thumb"]/@href',
        'source' : 'hoangphatvn.vn',
        'title' : '//*[@id="dp-teaser"]//h1[1]//text()',
        'price' : '//*[@id="td_info"]//text()'
    }

    def parse(self, response):
        return self.parse_item(response)