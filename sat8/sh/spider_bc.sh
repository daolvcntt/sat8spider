#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/BachKhoaShopSpider.py
scrapy runspider sat8/spiders/BanHangTrucTuyenSpider.py
scrapy runspider sat8/spiders/BestStoreSpider.py
scrapy runspider sat8/spiders/BinhNguyenCbSpider.py

scrapy runspider sat8/spiders/CellphoneSpider.py
scrapy runspider sat8/spiders/CdiscountSpider.py
scrapy runspider sat8/spiders/ChonhapkhauSpider.py