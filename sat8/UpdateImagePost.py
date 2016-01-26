# -*- coding: utf-8 -*-
# Cập nhật lại ảnh đại diện của post
# để chuyển dần sang dùng google bucket
from scrapy.conf import settings
import os.path
import re
import hashlib
import urllib
from time import gmtime, strftime
from PIL import Image

import env

def getImageFromContent(content):
    matches = re.search('src="([^"]+)"', content)
    return matches.group(1)

conn = settings['MYSQL_CONN']
cursor = conn.cursor()

queryPost = "SELECT * FROM posts"
cursor.execute(queryPost)
posts = cursor.fetchall()


countPostUpdated = 0


imageThumbs = settings["IMAGES_THUMBS"]

for post in posts:
    # print getImageFromContent(post["content"])
    # Nếu avatar ko có thì lấy 1 ảnh trong nội dung làm avatar bài viết
    if os.path.isfile(env.IMAGES_STORE + '/full/'+ post['avatar']) == False:
        postImage = getImageFromContent(post["content"])
        if postImage != None:
            imageName = hashlib.sha1(postImage).hexdigest() + '.jpg'
            pathSaveImage = settings['IMAGES_STORE'] + '/full/' + imageName

            # Nếu không có ảnh full thì mới download và resize ảnh
            # có rồi thì cập nhật luôn
            if os.path.isfile(pathSaveImage) == False:
                pathSaveImageSmall = settings['IMAGES_STORE'] + '/thumbs/small/' + imageName
                pathSaveImageBig   = settings['IMAGES_STORE'] + '/thumbs/big/' + imageName

                try:
                    urllib.urlretrieve(postImage, pathSaveImage)
                    im = Image.open(pathSaveImage)

                    im.thumbnail(imageThumbs["small"])
                    im.save(pathSaveImageSmall, 'JPEG')

                    im = Image.open(pathSaveImage)
                    im.thumbnail(imageThumbs["big"])
                    im.save(pathSaveImageBig, 'JPEG')

                except IOError:
                    print("cannot create thumbnail for post ID: ", post['id'])

            # Cập nhật ảnh đại diện post
            queryPost = "UPDATE posts SET avatar = %s WHERE id = %s"
            cursor.execute(queryPost, (imageName, post['id']))
            conn.commit()

            countPostUpdated += 1

            print ({
                'id' : post["id"],
                'avatar_old' : post['avatar'],
                'avatar_new' : imageName
            })


print "Post updated :" + str(countPostUpdated)
# print countPostUpdated

