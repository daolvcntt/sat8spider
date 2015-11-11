# """
# How to run scrapers programmatically from a script
# """
import scrapy

from spiders.ProductSpider import ProductSpider
from spiders.ProductLinkSpider import ProductLinkSpider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(ProductSpider)
# process.crawl(ProductLinkSpider)
process.start()
