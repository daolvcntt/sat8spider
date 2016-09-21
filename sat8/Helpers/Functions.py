# -*- coding: utf-8 -*-

from mimetypes import MimeTypes
from urlparse import urlparse

import urllib2
import re
import hashlib
import time
from scrapy.conf import settings
from PIL import Image
import urllib
import os
import imghdr



def list_get(array, key, default = ''):
	if key in array :
		return array[key]
	else :
		return default



def file_get_contents(filename, use_include_path = 0, context = None, offset = -1, maxlen = -1):
    if (filename.find('://') > 0):
        ret = urllib2.urlopen(filename).read()
        if (offset > 0):
            ret = ret[offset:]
        if (maxlen > 0):
            ret = ret[:maxlen]
        return ret
    else:
        fp = open(filename,'rb')
        try:
            if (offset > 0):
                fp.seek(offset)
            ret = fp.read(maxlen)
            return ret
        finally:
            fp.close( )


def get_file_name(path):
    arrayStr = path.split('/')
    return arrayStr[len(arrayStr)-1]

def get_mime_type(path):
    mime = MimeTypes()
    return mime.guess_type(path)[0]

def replace_link(content):
    filter_content = re.sub('<a\s(.+?)>(.+?)</a>', '\\2', content, flags=re.MULTILINE)
    return filter_content

def replace_image(content, newPath):
    images = re.findall('src="(.+?)"', content)
    for image in images:
        content = re.sub(image, newPath +  sha1FileName(image), content)

    return content

def timestamp():
    return time.time()

def getExtension(url):
    arrayUrl = url.split('.')
    ext = arrayUrl[len(arrayUrl)-1]
    ext = ext.lower();

    mime = get_mime_type(url)

    if mime == 'image/gif':
        return 'gif'
    elif mime == 'image/jpeg':
        return 'jpeg'
    elif mime == 'image/png':
        return 'png'
    elif mime == 'image/bmp':
        return 'bmp'
    else:
        return ext;

def downloadImageFromUrl(url, createThumbs = 1):
    ext = getExtension(url);
    imageName = sha1FileName(url);

    pathSaveImage = settings['IMAGES_STORE'] + '/full/' + imageName
    pathSaveImageSmall = settings['IMAGES_STORE'] + '/thumbs/small/' + imageName
    pathSaveImageBig   = settings['IMAGES_STORE'] + '/thumbs/big/' + imageName

    isFile = os.path.isfile(pathSaveImage)

    if (isFile == True and imghdr.what(pathSaveImage) == None) or (isFile == False):
        # urllib.urlretrieve(url, pathSaveImage)

        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        imgRequest = urllib2.Request(url, headers=hdr)
        imgData = urllib2.urlopen(imgRequest).read()

        f = open(pathSaveImage, 'w')
        f.write(imgData)
        f.close()

    # Resize image
    imageThumbs = settings['IMAGES_THUMBS']

    if (os.path.isfile(pathSaveImageSmall) == True and imghdr.what(pathSaveImageSmall) == None) or (os.path.isfile(pathSaveImageSmall) == False):
        im = Image.open(pathSaveImage)
        im.thumbnail(imageThumbs["small"])
        im.save(pathSaveImageSmall, ext);

    if (os.path.isfile(pathSaveImageBig) == True and imghdr.what(pathSaveImageBig) == None) or (os.path.isfile(pathSaveImageBig) == False):
        im = Image.open(pathSaveImage)
        im.thumbnail(imageThumbs["big"])
        im.save(pathSaveImageBig, ext);

    return {
        "full" : pathSaveImage,
        "big" : pathSaveImageBig,
        "small" : pathSaveImageSmall
    }


def sha1(string):
    return hashlib.sha1(string.encode('utf-8')).hexdigest()

def sha1FileName(fileName):
    return sha1(fileName) + '.' + getExtension(fileName)

def md5(string):
    return hashlib.md5(string).hexdigest()

def getUrlWithoutParams(url):
    index = url.find('?')

    if index > -1 :
        return url[0:index]

    return url


# Lấy id sản phẩm vg từ link
def getVGProductId(link):
    if 'record_id' in link:
        parsed = urlparse(link)
        record_id = urlparse.parse_qs(parsed.query)['record_id']
        return int(record_id)

    parsed = urlparse(link)
    path = parsed.path
    return int(path.split('/')[2])