from scrapy.conf import settings

from elasticsearch import Elasticsearch
from sat8.Databases.DB import DB
from sat8.Elasticsearch.ES import ES
from sat8.Posts.PostES import PostES
from sat8.Products.ProductES import ProductES
from sat8.Products.ProductPriceES import ProductPriceES

from sat8.Products.ProductVideoES import ProductVideoES

conn = settings['MYSQL_CONN']
cursor = conn.cursor()


queryProduct = "SELECT * FROM products"
cursor.execute(queryProduct)
products = cursor.fetchall()

for product in products:
    productEs = ProductES()
    productEs.insertOrUpdate(product['id'], product)


queryPrice = "SELECT * FROM product_prices"
cursor.execute(queryPrice)
prices = cursor.fetchall()

for price in prices:
    priceEs = ProductPriceES()
    priceEs.insertOrUpdate(price['id'], price)


queryPost = "SELECT * FROM posts"
cursor.execute(queryPost)
posts = cursor.fetchall()

for post in posts:
    postEs = PostES()
    postEs.insertOrUpdate(post['id'], post)


queryVideo = "SELECT * FROM product_videos"
cursor.execute(queryVideo)
videos = cursor.fetchall()

for video in videos:
    videoEs = ProductVideoES()
    videoEs.insertOrUpdate(video['id'], video)


