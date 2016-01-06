# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class LaptopChinhHangSpider(AbstractPriceSpider):
    allowed_domains = ['laptopchinhhang.com']
    start_urls = [
        'http://laptopchinhhang.com/San-Pham/104/Asus-X-series---F-series--A-series.dnk',
        'http://laptopchinhhang.com/San-Pham/106/Asus--K45X---K55X.dnk',
        'http://laptopchinhhang.com/San-Pham/280/Dell-55xx-54xx.dnk',
        'http://laptopchinhhang.com/San-Pham/275/Dell-34xx-35xx.dnk',
        'http://laptopchinhhang.com/San-Pham/281/Dell-74xx-75xx.dnk',
        'http://laptopchinhhang.com/San-Pham/204/Acer-Aspire-E--Dong-pho-thong-.dnk',
        'http://laptopchinhhang.com/San-Pham/202/Acer-Aspire-V3-series--Sang-trong-.dnk',
        'http://laptopchinhhang.com/San-Pham/266/Lenovo-G40X0-G50X0.dnk',
        'http://laptopchinhhang.com/San-Pham/269/Lenovo-Flex12---Flex14--Yoga--IBY.dnk',
        'http://laptopchinhhang.com/San-Pham/267/Lenovo-Z4XX-Z5XX-S4XX-Z5070-U4170.dnk',


        'http://laptopchinhhang.com/San-Pham/296/ASUS-GAMING.dnk',
        'http://laptopchinhhang.com/San-Pham/76/ASUS-B--U--N--S--P-series.dnk',
        'http://laptopchinhhang.com/San-Pham/245/Man-Hinh-Cam-Ung.dnk',
        'http://laptopchinhhang.com/San-Pham/29/Dell-vostro.dnk',
        'http://laptopchinhhang.com/San-Pham/31/Dell-xps.dnk',
        'http://laptopchinhhang.com/San-Pham/77/DELL-LATITUDE.dnk',
        'http://laptopchinhhang.com/San-Pham/278/San-Pham-Khac.dnk',
        'http://laptopchinhhang.com/San-Pham/309/HP-Envy.dnk',
        'http://laptopchinhhang.com/San-Pham/87/HP-Probook.dnk',
        'http://laptopchinhhang.com/San-Pham/239/HP-Pavilion-Lean-14.dnk',
        'http://laptopchinhhang.com/San-Pham/240/HP-Pavilion-Lean-15.dnk',
        'http://laptopchinhhang.com/San-Pham/88/HP-14---15---340---350.dnk',
        'http://laptopchinhhang.com/San-Pham/89/HP-Stream--X2--X360.dnk',
        'http://laptopchinhhang.com/San-Pham/306/MSI-Classic-Series.dnk',
        'http://laptopchinhhang.com/San-Pham/305/MSI-Gaming-GP-Series.dnk',
        'http://laptopchinhhang.com/San-Pham/304/MSI-Gaming-GE-Series.dnk',
        'http://laptopchinhhang.com/San-Pham/201/Acer-Aspire-V5-series--Sieu-mong-.dnk',
        'http://laptopchinhhang.com/San-Pham/203/Acer-Ultrabook--Cao-cap---Nhe---Mong---Dep-.dnk',
        'http://laptopchinhhang.com/San-Pham/268/Lenovo-Gaming.dnk'

    ]

    rules = (
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('\?page=[0-9]+')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product-grid"]/div/a[1]/@href',
        'source' : 'laptopchinhhang.com',
        'title' : '//*[@class="pro_name_more"]/h2[1]//text()',
        'price' : '//*[@class="pro_price4"]/text()'
    }