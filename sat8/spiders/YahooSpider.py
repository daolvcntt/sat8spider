# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from sat8.items import QuestionItem, QuestionItemLoader
from sat8.items import AnswerItem, AnswerItemLoader

from time import gmtime, strftime
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse

import urllib
import logging

class YahooSpider(CrawlSpider):
    name = "blog_spider"
    allowed_domains = ['vn.answers.yahoo.com']

    questionId = 0
    productId = 0;

    def __init__(self):
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()


    def parse_item(self, response):
        sel = Selector(response)
        product_links = sel.xpath('//*[@class="question-title"]/a[1]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            request = scrapy.Request(url, callback = self.parse_question_content)
            request.meta['productId'] = response.meta['productId']
            yield request


    def parse_question_content(self, response):
        link = response.url
        url_parts = urlparse(link)

        qil = QuestionItemLoader(item = QuestionItem(), response = response)

        qil.add_xpath('question', '//*[@class="Mstart-75 Mr-14 Pos-r"]/h1/text()')
        qil.add_xpath('content', '//*[@class="ya-q-text"]')
        qil.add_value('user', "admin".decode('utf-8'))
        qil.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
        qil.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))
        qil.add_value('link', link)
        qil.add_value('product_id', response.meta['productId'])

        question = qil.load_item()

        query = "SELECT id,link FROM questions WHERE link = %s"
        self.cursor.execute(query, (question['link']))
        result = self.cursor.fetchone()

        questionId = 0;
        if result:
            questionId = result['id']
            logging.info("Item already stored in db: %s" % question['link'])
        else:
            sql = "INSERT INTO questions (question, content, user, link, product_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (question['question'].encode('utf-8'), question['content'], question['user'] ,question['link'],question['product_id'], question['created_at'], question['updated_at']))
            self.conn.commit()
            logging.info("Item stored in db: %s" % question['link'])
            questionId = self.cursor.lastrowid

        # Insert câu trả lời

        slAnswers = Selector(response)
        answers = slAnswers.xpath('//*[@id="ya-qn-answers"]/li[@class="Cf Py-14 ya-other-answer Pend-14  Bdbx-f4 "]')
        created_at = strftime("%Y-%m-%d %H:%M:%S")
        updated_at = strftime("%Y-%m-%d %H:%M:%S")

        # print len(answers)
        # return

        for answer in answers:
            user = answer.xpath('.//a[@class="uname Clr-b"]//text()').extract()
            ans = answer.xpath('.//span[@class="ya-q-full-text"]//text()').extract()


            answerItemLoader = AnswerItemLoader(item = AnswerItem(), response = response)
            answerItemLoader.add_value('question_id', questionId)
            answerItemLoader.add_value('user', user[0])
            answerItemLoader.add_value('answer', ans[0])
            answerItemLoader.add_value('created_at', created_at)
            answerItemLoader.add_value('updated_at', updated_at)
            answerDb = answerItemLoader.load_item()

            sql = "INSERT INTO answers (question_id, answer, user, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (answerDb['question_id'], answerDb['answer'], answerDb['user'], answerDb['created_at'], answerDb['updated_at']))
            self.conn.commit()


        # print question
        # return



    def start_requests(self):
        print '------------------------------', "\n"
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT DISTINCT id,keyword,rate_keyword FROM products WHERE rate_keyword != '' OR rate_keyword != NULL ORDER BY created_at DESC")
        products = self.cursor.fetchall()

        for product in products:
            # url = 'http://vatgia.com/hoidap/quicksearch.php?keyword=%s' %product['rate_keyword']
            url = 'https://vn.answers.yahoo.com/search/search_result?fr=uh3_answers_vert_gs&type=2button&p=%s' %product['rate_keyword']
            # self.start_urls.append(url)
            request = scrapy.Request(url, callback = self.parse_item)
            request.meta['productId'] = product['id']
            yield request

        # yield scrapy.Request(response.url, callback=self.parse_item)
        print '------------------------------', "\n\n"
