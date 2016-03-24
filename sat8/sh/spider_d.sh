#!/bin/sh
cd /var/www/html/sat8spider

scrapy runspider sat8/spiders/DiDongHanQuocSpider.py
scrapy runspider sat8/spiders/DiDongProSpider.py
scrapy runspider sat8/spiders/DiDongVietSpider.py
scrapy runspider sat8/spiders/DienMayChoLonSpider.py
scrapy runspider sat8/spiders/DienMayManhCuongSpider.py
scrapy runspider sat8/spiders/DienMayThienHoaSpider.py
scrapy runspider sat8/spiders/DienMayXanhSpider.py
scrapy runspider sat8/spiders/DienThoaiDiDongSpider.py
scrapy runspider sat8/spiders/DienThoaiSaiGonSpider.py
scrapy runspider sat8/spiders/Dienmay247spider.py
scrapy runspider sat8/spiders/DigiPhoneSpider.py
scrapy runspider sat8/spiders/DmartSpider.py