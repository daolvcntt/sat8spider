#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/PhongVuSpider.py
scrapy runspider sat8/spiders/PicoSpider.py

scrapy runspider sat8/spiders/QuocHungComVnSpider.py

scrapy runspider sat/spiders/StyleMobileSpider.py