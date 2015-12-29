# -*- coding: utf-8 -*-
import scrapy
import re
from time import gmtime, strftime
import urllib
import logging
from scrapy.conf import settings
import hashlib

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from sat8.Products.ProductVideoES import ProductVideoES

DEVELOPER_KEY = "AIzaSyDgw7JoSOV_VqSLZBWP40kHd8la0tRP8EU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class YoutubePipeline(object):

   def __init__(self):
      self.conn = settings['MYSQL_CONN']
      self.cursor = self.conn.cursor()
      self.video = ProductVideoES()

   def process_item(self, item, spider):
      print 'YOUTUBE', "\n\n"
      print item, "--------------\n\n---------------"
      self.getVideo(item['name'][:20])
      return item

   def getVideo(self, keyword):

      youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

      # Call the search.list method to retrieve results matching the specified
      # query term.
      keyword = "đánh giá " + keyword.encode('utf-8') + " việt nam"

      search_response = youtube.search().list(
         q=keyword,
         type="video",
         # location=options.location,
         # locationRadius=options.location_radius,
         part="id,snippet",
         maxResults=50,
         regionCode='VN',
         order='relevance'
      ).execute()

      search_videos = []

      # Merge video ids
      for search_result in search_response.get("items", []):
         youtubeId   = search_result["id"]["videoId"]
         title       = search_result["snippet"]["title"]
         description = search_result["snippet"]["description"]
         channelId   = search_result["snippet"]["channelId"]
         channelName = search_result["snippet"]["channelTitle"]
         image       = search_result['snippet']['thumbnails']['high']['url']
         created_at  = strftime("%Y-%m-%d %H:%M:%S")
         updated_at  = strftime("%Y-%m-%d %H:%M:%S")

         query = "SELECT * FROM product_videos WHERE video_id = %s"
         self.cursor.execute(query, (youtubeId))
         result = self.cursor.fetchone()

         videoId = 0

         if result:
            videoId = result['id']
            print "Video already stored in db: %s" % title
            logging.info("Video already stored in db: %s" % title)
         else:
            sqlInsert = "INSERT INTO product_videos(video_id, channel_id, channel_name, image, title, teaser, created_at, updated_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sqlInsert, (youtubeId, channelId, channelName, image, title, description, created_at, updated_at))
            self.conn.commit()

            videoId = self.cursor.lastrowid
            print "Video stored in db: %s" % title
            logging.info("Video stored in db: %s" % title)

         self.video.insertOrUpdate(videoId, {
            'id' : videoId,
            'title' : title,
            'product_id' : 0,
            'channel_id' : channelId,
            'video_id' : youtubeId,
            'teaser' : description,
            'channel_name' : channelName,
            'image' : image,
            'created_at' : created_at,
            'updated_at' : updated_at
         })

   def getVideosByProducts(self):
      self.cursor.execute("SELECT keyword FROM products")
      products = self.cursor.fetchall()

      for product in products:
         self.getVideo(product['keyword'])

# youtube = YoutubePipline()
# youtube.getVideo('iphone')