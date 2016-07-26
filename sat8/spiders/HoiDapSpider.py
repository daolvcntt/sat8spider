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

class HoiDapSpider(CrawlSpider):
    name = "hoidap_spider"
    allowed_domains = ['vatgia.com']

    questionId = 0
    productId = 0;

    def __init__(self, env="production"):
        self.env = env
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()


    def parse_item(self, response):
        sel = Selector(response)
        product_links = sel.xpath('//*[@id="box_main_content"]//a[@class="tooltip"]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            request = scrapy.Request(url, callback = self.parse_question_content)
            request.meta['productId'] = 0
            yield request


    def parse_question_content(self, response):
        link = response.url
        url_parts = urlparse(link)

        qil = QuestionItemLoader(item = QuestionItem(), response = response)

        qil.add_xpath('question', '//*[@class="box_content_news"]/h1/text()')
        qil.add_xpath('content', '//*[@class="detail_description"]')
        qil.add_xpath('user', '//*[@class="fl info_user_left"]/p[1]/a[1]//text()')
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
        answers = slAnswers.xpath('//*[@id="box_replyhoidap"]/div[@class="story_comment fl "]')
        created_at = strftime("%Y-%m-%d %H:%M:%S")
        updated_at = strftime("%Y-%m-%d %H:%M:%S")

        # print len(answers)
        # return

        for answer in answers:
            user = answer.xpath('.//div[@class="fl info_user_left"][1]/p[1]/a[1]/text()').extract()
            ans = answer.xpath('.//div[@class="text_comment"]').extract()

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


    def parse_answer_content(self, response):
        link = response.url
        url_parts = urlparse(link)

        ail = AnswerItemLoader(item = AnswerItem(), response = response)

        ail.add_xpath('answer', '//*[@id="box_replyhoidap"]//div[@class="text_comment"]');
        ail.add_xpath('user', '//*[@id="box_replyhoidap"]//div[@class="fl info_user_left"]/p[1]/a[1]//text()');
        ail.add_value('question_id', response.meta['questionId'])
        ail.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
        ail.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))

        answer = ail.load_item()

        print answer



    def start_requests(self):
        print '------------------------------', "\n"
        # self.conn = settings['MYSQL_CONN']
        # self.cursor = self.conn.cursor()
        # self.cursor.execute("SELECT DISTINCT id,keyword,rate_keyword FROM products WHERE rate_keyword != '' OR rate_keyword != NULL ORDER BY created_at DESC")
        # products = self.cursor.fetchall()

        # for product in products:
        #     url = 'http://vatgia.com/hoidap/quicksearch.php?keyword=%s' %product['rate_keyword']
        #     # self.start_urls.append(url)
        #     request = scrapy.Request(url, callback = self.parse_item)
        #     request.meta['productId'] = product['id']
        #     yield request


        links = [
            'http://vatgia.com/hoidap/type.php?iCat=3943&page={#page#}',
            'http://vatgia.com/hoidap/type.php?iCat=3878&page={#page#}'
        ]

        for link in links:
            for i in range(1,2):
                url = link.replace('{#page#}', str(i))
                request = scrapy.Request(url, callback=self.parse_item)
                yield request

        # yield scrapy.Request(response.url, callback=self.parse_item)
        print '------------------------------', "\n\n"
