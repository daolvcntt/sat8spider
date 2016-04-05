# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ShopdunkSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['shopdunk.vn']
    start_urls = [
        'http://shopdunk.vn/san-pham/4-iphone/131-iphone-6s.html',
        'http://shopdunk.vn/san-pham/4-iphone/132-iphone-6s-plus.html',
        'http://shopdunk.vn/san-pham/4-iphone/54-iphone-6.html',
        'http://shopdunk.vn/san-pham/4-iphone/85-iphone-6-plus.html',
        'http://shopdunk.vn/san-pham/4-iphone/53-iphone-5s.html',
        'http://shopdunk.vn/san-pham/4-iphone/8-iphone-5.html',
        'http://shopdunk.vn/san-pham/4-iphone/64-iphone-5c.html',
        'http://shopdunk.vn/san-pham/4-iphone/11-iphone-4s.html',
        'http://shopdunk.vn/san-pham/4-iphone/12-iphone-4.html',

        'http://shopdunk.vn/san-pham/10-ipad/86-ipad-air-2.html',
        'http://shopdunk.vn/san-pham/10-ipad/65-ipad-air.html',
        'http://shopdunk.vn/san-pham/10-ipad/1286-ipad-pro.html',
        'http://shopdunk.vn/san-pham/10-ipad/87-ipad-mini-3.html',
        'http://shopdunk.vn/san-pham/10-ipad/66-ipad-mini-2.html',
        'http://shopdunk.vn/san-pham/10-ipad/16-ipad-mini.html',
        'http://shopdunk.vn/san-pham/10-ipad/15-ipad-4.html',
        'http://shopdunk.vn/san-pham/10-ipad/58-ipad-3-fullbox-100.html',
        'http://shopdunk.vn/san-pham/10-ipad/59-ipad-2-fullbox-100.html',

        'http://shopdunk.vn/san-pham/1-macbook/104-macbook-12-inch.html',
        'http://shopdunk.vn/san-pham/1-macbook/78-macbook-like-new.html',
        'http://shopdunk.vn/san-pham/1-macbook/21-macbook-air.html',
        'http://shopdunk.vn/san-pham/1-macbook/20-macbook-pro.html',
        'http://shopdunk.vn/san-pham/1-macbook/22-macmini.html',
        'http://shopdunk.vn/san-pham/1-macbook/19-imac.html',

        'http://shopdunk.vn/san-pham/3-smartphone/63-oppo.html',
        'http://shopdunk.vn/san-pham/3-smartphone/77-asus-zenfone.html',
        'http://shopdunk.vn/san-pham/3-smartphone/55-black-berry.html',
        'http://shopdunk.vn/san-pham/3-smartphone/41-sony-xperia.html',
        'http://shopdunk.vn/san-pham/3-smartphone/42-samsung.html'
    ]

    rules = (

    )

    configs = {
        'product_links' : '//*[@class="product_item_name"]/a/@href',
        'source' : 'shopdunk.vn',
        'title' : '//*[@class="product_right sp-bd-r"]/div[@class="productName"]/h1//text()',
        'price' : '//*[@id="body"]/div[2]/div/div/div/div[2]/div/div[2]/span[1]/b/text()'
    }