#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/AchauMobileSpider.py
scrapy runspider sat8/spiders/AmazonVnSpider.py
scrapy runspider sat8/spiders/AdayroiSpider.py
scrapy runspider sat8/spiders/AnKhangSpider.py