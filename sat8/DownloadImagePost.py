# -*- coding: utf-8 -*-
# Cập nhật lại ảnh đại diện của post
# để chuyển dần sang dùng google bucket
import settings
import os.path
import re
import hashlib
import urllib
from time import gmtime, strftime
from PIL import Image
import gzip
import shutil

import env

from Functions import getImageFromContent
from Functions import makeGzFile

from Helpers.Functions import *
from Helpers.Google_Bucket import *

bucket = 'static.giaca.org'

conn = settings.MYSQL_CONN
cursor = conn.cursor()

queryPost = "SELECT * FROM posts WHERE has_image = 0 ORDER BY updated_at DESC LIMIT 2000"
cursor.execute(queryPost)
posts = cursor.fetchall()


countPostUpdated = 0


imageThumbs = settings.IMAGES_THUMBS

for post in posts:

    # print getImageFromContent(post["content"])
    # Nếu avatar ko có thì lấy 1 ảnh trong nội dung làm avatar bài viết
    if os.path.isfile(env.IMAGES_STORE + '/full/'+ post['avatar']) == False:

        postImage = getImageFromContent(post["content"])
        if postImage != None:
            imageName = hashlib.sha1(postImage).hexdigest() + '.jpg'
            pathSaveImage = settings.IMAGES_STORE + '/full/' + imageName

            # Nếu không có ảnh full thì mới download và resize ảnh
            # có rồi thì cập nhật luôn
            if os.path.isfile(pathSaveImage) == False:
                pathSaveImageSmall = settings.IMAGES_STORE + '/thumbs/small/' + imageName
                pathSaveImageBig   = settings.IMAGES_STORE + '/thumbs/big/' + imageName

                try:
                    # Download
                    urllib.urlretrieve(postImage, pathSaveImage)
                    im = Image.open(pathSaveImage)

                    im.thumbnail(imageThumbs["small"])
                    im.save(pathSaveImageSmall, 'JPEG')

                    im = Image.open(pathSaveImage)
                    im.thumbnail(imageThumbs["big"])
                    im.save(pathSaveImageBig, 'JPEG')

                    # Make gz file
                    makeGzFile(pathSaveImage)
                    makeGzFile(pathSaveImageBig)
                    makeGzFile(pathSaveImageSmall)

                    # Upload to google bucket
                    google_bucket_upload_object(bucket, pathSaveImage, 'uploads/full/' + imageName)
                    google_bucket_upload_object(bucket, pathSaveImageBig, 'uploads/thumbs/big/' + imageName)
                    google_bucket_upload_object(bucket, pathSaveImageSmall, 'uploads/thumbs/small/' + imageName)

                    google_bucket_upload_object(bucket, pathSaveImage + '.gz', 'uploads/full/' + imageName + '.gz')
                    google_bucket_upload_object(bucket, pathSaveImageBig + '.gz', 'uploads/thumbs/big/' + imageName + '.gz')
                    google_bucket_upload_object(bucket, pathSaveImageSmall + '.gz', 'uploads/thumbs/small/' + imageName + '.gz')

                except IOError:
                    print("cannot create thumbnail for post ID: ", post['id'])

            # Cập nhật ảnh đại diện post
            queryPost = "UPDATE posts SET avatar = %s, has_image = 1 WHERE id = %s"
            cursor.execute(queryPost, (imageName, post['id']))
            conn.commit()

            countPostUpdated += 1

            print "Download success picture from: ", postImage


print "Post updated :" + str(countPostUpdated)
# print countPostUpdated

