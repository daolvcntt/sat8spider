#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/HalomobileSpider.py
scrapy runspider sat8/spiders/HanoicomputerSpider.py
scrapy runspider sat8/spiders/HoangHaSpider.py
scrapy runspider sat8/spiders/HoangphatvnSpider.py
scrapy runspider sat8/spiders/HongHaAsiaSpider.py
scrapy runspider sat8/spiders/HcSpider.py
scrapy runspider sat8/spiders/HnamMobileSpider.py
scrapy runspider sat8/spiders/HuyHoangSpider.py

scrapy runspider sat8/spiders/IsSmartPhoneSpider.py
scrapy runspider sat8/spiders/ItshophanoiSpider.py

scrapy runspider sat8/spiders/KimmobileSpider.py