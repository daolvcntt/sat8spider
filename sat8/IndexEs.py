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


queryProduct = "SELECT * FROM products"
cursor.execute(queryProduct)
products = cursor.fetchall()

for product in products:
    productEs = ProductES()
    product['created_at'] = product['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    product['updated_at'] = product['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
    productEs.insertOrUpdate(product['id'], product)


queryPrice = "SELECT * FROM product_prices"
cursor.execute(queryPrice)
prices = cursor.fetchall()

for price in prices:
    priceEs = ProductPriceES()
    price['created_at'] = price['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    price['updated_at'] = price['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
    priceEs.insertOrUpdate(price['id'], price)


queryPost = "SELECT * FROM posts"
cursor.execute(queryPost)
posts = cursor.fetchall()

for post in posts:
    postEs = PostES()
    post['created_at'] = post['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    post['updated_at'] = post['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
    postEs.insertOrUpdate(post['id'], post)


queryVideo = "SELECT * FROM product_videos"
cursor.execute(queryVideo)
videos = cursor.fetchall()

for video in videos:
    videoEs = ProductVideoES()
    video['created_at'] = video['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    video['updated_at'] = video['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
    videoEs.insertOrUpdate(video['id'], video)


