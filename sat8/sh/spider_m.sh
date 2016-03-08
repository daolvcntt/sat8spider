#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/Mac24Spider.py
scrapy runspider sat8/spiders/MaiMuaSpider.py
scrapy runspider sat8/spiders/MayTinhThienMinhSpider.py
scrapy runspider sat8/spiders/MaytinhBachGiaSpider.py
scrapy runspider sat8/spiders/MnMobileSpider.py
scrapy runspider sat8/spiders/MobileProSpider.py
scrapy runspider sat8/spiders/MuabanLaptopGiaReSpider.py