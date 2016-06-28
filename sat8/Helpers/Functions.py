from mimetypes import MimeTypes
import urllib2
import re
import hashlib
import time
from scrapy.conf import settings
from PIL import Image
import urllib
import os

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
        content = re.sub(image, newPath +  hashlib.sha1(image).hexdigest() + '.jpg', content)

    return content

def timestamp():
    return time.time()

def getExtension(url):
    arrayUrl = url.split('.')
    ext = arrayUrl[len(arrayUrl)-1]
    ext = ext.lower();
    if ext == 'jpg':
        ext = 'jpeg';

    return ext;

def downloadImageFromUrl(url, createThumbs = 1):
    ext = getExtension(url);
    imageName = hashlib.sha1(url).hexdigest() + '.' + ext;

    pathSaveImage = settings['IMAGES_STORE'] + '/full/' + imageName
    pathSaveImageSmall = settings['IMAGES_STORE'] + '/thumbs/small/' + imageName
    pathSaveImageBig   = settings['IMAGES_STORE'] + '/thumbs/big/' + imageName

    if os.path.isfile(pathSaveImage) == False:
        urllib.urlretrieve(url, pathSaveImage)

    # Resize image
    imageThumbs = settings['IMAGES_THUMBS']

    if os.path.isfile(pathSaveImageSmall) == False:
        im = Image.open(pathSaveImage)
        im.thumbnail(imageThumbs["small"])
        im.save(pathSaveImageSmall, ext);

    if os.path.isfile(pathSaveImageBig) == False:
        im = Image.open(pathSaveImage)
        im.thumbnail(imageThumbs["big"])
        im.save(pathSaveImageBig, ext);

    return {
        "full" : pathSaveImage,
        "big" : pathSaveImageBig,
        "small" : pathSaveImageSmall
    }