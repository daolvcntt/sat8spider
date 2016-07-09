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
        # urllib.urlretrieve(url, pathSaveImage)

        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Cookie':'__cfduid=dfda1912a121b8d1dfe9dc69f2a1e93d41468034870; _ants_utm=%7B%22source%22%3A%22google.com.vn%22%2C%22medium%22%3A%22%22%2C%22campaign%22%3A%22%22%2C%22content%22%3A%22%22%2C%22term%22%3A%22%22%2C%22type%22%3A%22refferrer%22%2C%22time%22%3A1467946927336%7D; au_aid=173313886; au_gt=1460616547; move_address=move_address_hide; frontend=sj1ijvvolfsl50do6vltsuc1p0; _pk_id.578785290.11d9=2275fcb40cbfe515.1468034872.3.1468040768.1468040767.; an_session=zkzkzqzlzizjzgzgzdzizkzgzgzizgzrzrzlzdziznzlzhzqzgzlzjzrzmzdzmzjzdziznzlzrzjznzjzkzlzkzdziznzlzrzjzgzrzizrzrzdzizjzdzhznzdzhzd2f27zdzgzdzlzmzmznzr; dgs=1468031157%3A1%3A0-24; _ants_services=%5B%5D; _ga=GA1.3.1272787306.1468034872; __zlcmid=bXfgYZs2hizO6g',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
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


def sha1(string):
    return hashlib.sha1(string.encode('utf-8')).hexdigest()

def sha1FileName(fileName):
    return sha1(fileName) + '.' + getExtension(fileName)

def md5(string):
    return hashlib.md5(string).hexdigest()