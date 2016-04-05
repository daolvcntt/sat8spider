# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class MrbachkhoaSpider(AbstractPriceSpider):
    allowed_domains = ['mrbachkhoa.com']
    start_urls = [
        'https://mrbachkhoa.com/modules/bkproductfilter/bkproductfilter-ajax.php?id_category_layered=11&layered_price_slider=0_27090000&orderby=position&orderway=desc&page=3&pagination=1&totalCount=0&_=1457339532866',
    ]

    rules = (
        # Rule (LinkExtractor(allow=('http://mrbachkhoa.com/dien-thoai/p\-[0-9]+,sort-0'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@id="product_list"]//a[1]/@href',
        'source' : 'mrbachkhoa.com',
        'title' : '//*[@id="pb-right-column"]/h1//text()',
        'price' : '//*[@id="our_price_display"]//text()'
    }