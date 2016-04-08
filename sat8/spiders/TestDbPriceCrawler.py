# -*- coding: utf-8 -*-
# Dành cho việc test xpath
# @author Justin <cong.itsoft@gmail.com>
# @date 2016-04-07

import scrapy
import datetime
from DbPriceCrawler import DbPriceSpider
from scrapy.conf import settings

class TestDbPriceCrawler(DbPriceSpider):

    def parse_detail_content(self, response):
        print self.get_product(response)

    def start_requests(self):
        conn = settings['MYSQL_CONN']
        cursor = conn.cursor()

         # Ngày trong tuần
        weekday = datetime.datetime.today().weekday()

        # Lấy các site sẽ chạy ngày hôm nay
        siteIds = []
        query = "SELECT site_id FROM site_cronjob WHERE day = %s"
        cursor.execute(query, (weekday))
        rows = cursor.fetchall()
        for row in rows:
            siteIds.append(row['site_id'])

        siteIds = ','.join(str(id) for id in siteIds )

        if len(siteIds) <= 0:
            print 'Không có site nào được đặt cronjob, vui lòng đặt cronjob cho từng site trong Admin'
            return

        query = "SELECT * FROM sites JOIN site_metas ON sites.id = site_metas.site_id WHERE sites.env_testing = 1 AND sites.id IN("+ siteIds +")"
        cursor.execute(query)
        sites = cursor.fetchall()

        crawlLinks = []

        for site in sites:
            queryLink = "SELECT * FROM site_links WHERE site_id = %s ORDER BY id DESC"
            cursor.execute(queryLink, (site["id"]))
            links = cursor.fetchall()

            for link in links:
                if link["max_page"] > 0:
                    for i in range(1, link["max_page"]+1):
                        startLink = link["link"].replace('[0-9]+', str(i))
                        crawlLinks.append(startLink)


        for lik in crawlLinks:
            request = scrapy.Request(lik, callback = self.parse_item)
            request.meta['site'] = site
            request.meta['link_item'] = link
            yield request