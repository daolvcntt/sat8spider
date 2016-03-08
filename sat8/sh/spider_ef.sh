#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/FptShopSpider.py
scrapy runspider sat8/spiders/FamSpider.py