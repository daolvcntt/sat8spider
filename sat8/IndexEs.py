from scrapy.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch import TransportError
from sat8.Databases.DB import DB
from sat8.Elasticsearch.ES import ES
from sat8.Posts.PostES import PostES
from sat8.Products.ProductES import ProductES
from sat8.Products.ProductPriceES import ProductPriceES

from sat8.Products.ProductVideoES import ProductVideoES

from sat8.Classifields.EsRaovat import EsRaovat

from sat8.Questions.EsQuestion import EsQuestion

from time import gmtime, strftime

conn = settings['MYSQL_CONN']
cursor = conn.cursor()

def runIndex():
    indexProducts()
    indexPrices()
    indexPosts()
    indexRaovat()
    indexQuestions()
    indexVideos()

def indexProducts():
    queryProduct = "SELECT * FROM products"
    cursor.execute(queryProduct)
    products = cursor.fetchall()

    updated = 0
    for product in products:
        productEs = ProductES()
        product.pop('created_at', None)
        product.pop('updated_at', None)

        # product['created_at'] = product['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        # product['updated_at'] = product['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        productEs.insertOrUpdate(product['id'], product)

        updated += 1

    print 'Products: %s \n' % (updated)

def indexPrices():
    queryPrice = "SELECT * FROM product_prices"
    cursor.execute(queryPrice)
    prices = cursor.fetchall()

    updated = 0

    for price in prices:
        priceEs = ProductPriceES()

        price.pop('created_at', None)
        price.pop('updated_at', None)

        # price['created_at'] = price['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        # price['updated_at'] = price['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        priceEs.insertOrUpdate(price['id'], price)

        updated += 1

    print 'Prices: %s \n' % (updated)

def indexPosts():
    queryPost = "SELECT * FROM posts"
    cursor.execute(queryPost)
    posts = cursor.fetchall()

    updated = 0

    for post in posts:
        postEs = PostES()

        post.pop('created_at', None)
        post.pop('updated_at', None)

        postEs.insertOrUpdate(post['id'], post)
        updated += 1

        # post['created_at'] = post['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        # post['updated_at'] = post['updated_at'].strftime("%Y-%m-%d %H:%M:%S")

    print 'Posts: %s \n' % (updated)

def indexVideos():
    queryVideo = "SELECT * FROM product_videos"
    cursor.execute(queryVideo)
    videos = cursor.fetchall()

    updated = 0

    for video in videos:
        videoEs = ProductVideoES()

        video.pop('created_at', None)
        video.pop('updated_at', None)

        # video['created_at'] = video['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        # video['updated_at'] = video['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        videoEs.insertOrUpdate(video['id'], video)

        updated += 1

    print 'Videos: %s \n' % (updated)

def indexRaovat():
    query = "SELECT * FROM classifields"
    cursor.execute(query)
    classifields = cursor.fetchall()

    updated = 0

    for classifield in classifields:
        es = EsRaovat()

        classifield.pop('created_at', None)
        classifield.pop('updated_at', None)

        # classifield['created_at'] = classifield['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        # classifield['updated_at'] = classifield['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        es.insertOrUpdate(classifield['id'], classifield)

        updated += 1

    print 'Raovat: %s \n' % (updated)


def indexQuestions():
    query = "SELECT * FROM questions"
    cursor.execute(query)
    questions = cursor.fetchall()

    updated = 0

    for question in questions:
        es = EsQuestion()

        question.pop('created_at', None)
        question.pop('updated_at', None)

        # classifield['created_at'] = classifield['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        # classifield['updated_at'] = classifield['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        es.insertOrUpdate(question['id'], question)

        updated += 1

    print 'Questions: %s \n' % (updated)

# try:
runIndex()
# except TransportError, e:
    # print e
