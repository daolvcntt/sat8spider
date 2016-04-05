from scrapy.conf import settings

from elasticsearch import Elasticsearch
from sat8.Databases.DB import DB
from sat8.Elasticsearch.ES import ES
from sat8.Posts.PostES import PostES
from sat8.Products.ProductES import ProductES
from sat8.Products.ProductPriceES import ProductPriceES

from sat8.Products.ProductVideoES import ProductVideoES

from time import gmtime, strftime

conn = settings['MYSQL_CONN']
cursor = conn.cursor()

queryPrices = "SELECT * FROM product_prices WHERE source_id = 0"
cursor.execute(queryPrices)
prices = cursor.fetchall()

updated = 0
for price in prices:
    queryShop = "SELECT id FROM sites WHERE name = %s"
    cursor.execute(queryShop, (price['source']))
    shop = cursor.fetchone()
    if shop != None:
        querUpdate = "UPDATE product_prices SET source_id = %s WHERE id = %s"
        cursor.execute(querUpdate, (shop['id'], price['id']))
        conn.commit()
        updated += 1

print updated