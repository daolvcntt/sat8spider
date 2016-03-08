#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/TabletplazaSpider.py
scrapy runspider sat8/spiders/TechOneSpider.py
scrapy runspider sat8/spiders/ThanhNamPcSpider.py
scrapy runspider sat8/spiders/TheGioiTraGopSpider.py
scrapy runspider sat8/spiders/ThegioialoSpider.py
scrapy runspider sat8/spiders/ThegioididongSpider.py
scrapy runspider sat8/spiders/TikiSpider.py
scrapy runspider sat8/spiders/TuNguyetSpider.py
scrapy runspider sat8/spiders/TinVietTienSpider.py
scrapy runspider sat8/spiders/TwoCeSpider.py