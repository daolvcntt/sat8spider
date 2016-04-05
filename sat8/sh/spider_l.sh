#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/LapNewSpider.py
scrapy runspider sat8/spiders/LaptopChinhHangSpider.py
scrapy runspider sat8/spiders/LaptopGiaHuySpider.py
scrapy runspider sat8/spiders/LaptopNo1Spider.py
scrapy runspider sat8/spiders/LaptopVipSpider.py
scrapy runspider sat8/spiders/LaptopgiagocSpider.py
scrapy runspider sat8/spiders/LazadaSpider.py
scrapy runspider sat8/spiders/LongBinhSpider.py