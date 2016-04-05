#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/ValaSpider.py
scrapy runspider sat8/spiders/VienThongASpider.py
scrapy runspider sat8/spiders/ViettabletSpider.py
scrapy runspider sat8/spiders/VinhPhatMobileSpider.py

scrapy runspider sat8/spiders/XtMobileSpider.py

scrapy runspider sat8/spiders/Yes24Spider.py