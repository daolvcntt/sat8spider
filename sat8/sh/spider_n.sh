#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/NamaSpider.py
scrapy runspider sat8/spiders/NgocThanhMobileSpider.py
scrapy runspider sat8/spiders/NguyenKimLaptopPriceSpider.py
scrapy runspider sat8/spiders/NmobileSpider.py
scrapy runspider sat8/spiders/NovaComVnSpider.py