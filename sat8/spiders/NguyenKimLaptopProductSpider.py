# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductItem, ProductItemLoader

from time import gmtime, strftime

class NguyenKimLaptopProductSpider(CrawlSpider):
    name = "product_spider"
    allowed_domains = ["www.nguyenkim.com"]
    start_urls = ['http://www.nguyenkim.com/may-tinh-xach-tay/',]
    rules = (
        Rule (LinkExtractor(allow=('may-tinh-xach-tay/page-[0-9]+/'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
    )

    images = [];

    def parse_item(self, response):
    	sel = Selector(response)
        product_links = sel.xpath('//*[@class="ty-grid-list__image"]/a[1]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        pil = ProductItemLoader(item = ProductItem(), response = response)
        pil.add_xpath('name', '//*[@class="block_product-title"]/text()')
        pil.add_xpath('image', '//*[@class="border-image-wrap cm-preview-wrapper"]/a[1]/img/@data-original')
        pil.add_xpath('spec', '//*[@id="content_product_tab_58"]')
        pil.add_xpath('images', '//*[@class="  pict imagelazyload"]/@data-original')
        pil.add_xpath('price', '//*[@class="actual-price"]/span/span/span[1]/text()')
        pil.add_xpath('brand', '//*[@id="breadcrumbs_320"]/div/a[4]/text()')

        # Ảnh chi tiết sản phẩm
        sel = Selector(response)
        images = sel.xpath('//*[@class="cm-item-gallery float-left"]/a/img/@data-original');

        dataImage = []
        image_urls = []

        for img in images:
            imgLink = response.urljoin(img.extract())
            image_urls.append(imgLink)

            imgLinkHash = hashlib.sha1(imgLink).hexdigest() + '.jpg'
            dataImage.append(imgLinkHash)

        product = pil.load_item()

        image_urls.append(pil.get_value(product['image']))

        # Price
        price = pil.get_value(product['price'].encode('utf-8'))
        price = re.sub('\D', '', price)

        product['price']      = price
        product['link']       = response.url
        product['image_urls'] = image_urls
        product['image']      = hashlib.sha1(pil.get_value(product['image'])).hexdigest() + '.jpg'
        product['images']     = ',' . join(dataImage)
        product['hash_name']  = hashlib.md5(pil.get_value(product['name']).encode('utf-8')).hexdigest()
        product['brand']      = pil.get_value(product['brand'])
        product['typ']        = 'product'
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        yield(product)
