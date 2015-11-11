"""
How to run scrapers programmatically from a script
"""
import scrapy
from spiders.CellphoneSpider import CellphoneSpider
from spiders.TgdtSpider import TgdtSpider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(CellphoneSpider)
process.crawl(TgdtSpider)
process.start() # the script will block here until all crawling jobs are finished