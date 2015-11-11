# """
# How to run scrapers programmatically from a script
# """
import scrapy

from spiders.BlogSpider import BlogSpider
from spiders.GenkReviewSpider import GenkReviewSpider
from spiders.TgddPostSpider import TgddPostSpider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(BlogSpider)
process.crawl(GenkReviewSpider)
process.crawl(TgddPostSpider)
process.start()
