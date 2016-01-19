import gzip
import shutil
import os
import env

arrayDir = [
    env.IMAGES_STORE + '/full/',
    env.IMAGES_STORE + '/thumbs/small/',
    env.IMAGES_STORE + '/thumbs/big/',
    env.IMAGES_STORE + '/posts/',
    env.IMAGES_STORE + '/settings/',
    env.IMAGES_STORE + '/banners/'
]

arrayExts = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.css', '.js']

# filePath = '/home/justin/public_html/sat8web/public/images/post_default_image.jpg'
# filePathGzip = filePath + '.gz'
# with open(filePath , 'rb') as f_in, gzip.open(filePathGzip, 'wb') as f_out:
#     shutil.copyfileobj(f_in, f_out)

# print arrayDir

for myDir in arrayDir:
    for filename in os.listdir(myDir):
        filePath = myDir + filename
        filePathGzip = filePath + '.gz'

        name, ext = os.path.splitext(filePath)

        # Neu la file anh thi gzip
        if ext in arrayExts:
            if(os.path.isfile(filePathGzip) != True):
                with open(filePath , 'rb') as f_in, gzip.open(filePathGzip, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
