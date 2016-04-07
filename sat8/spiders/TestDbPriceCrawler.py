# -*- coding: utf-8 -*-
# Dành cho việc test xpath
# @author Justin <cong.itsoft@gmail.com>
# @date 2016-04-07

import scrapy
from DbPriceCrawler import DbPriceSpider

class TestDbPriceCrawler(DbPriceSpider):

    def parse_detail_content(self, response):
        print self.get_product(response)

    def start_requests(self):
        conn = settings['MYSQL_CONN']
        cursor = conn.cursor()
        query = "SELECT * FROM sites JOIN site_metas ON sites.id = site_metas.site_id WHERE sites.env_test = 1"
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