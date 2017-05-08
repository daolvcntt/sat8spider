# -*- coding: utf-8 -*-
import sys

import socket
import os

hostname = socket.gethostname()

if hostname == 'justin-HP-ProBook-450-G0':
    sys.path.insert(0, "/home/justin/public_html/sat8spider")
else:
    sys.path.insert(0, "/var/www/html/sat8spider")

from sat8.Helpers.Functions import *

url = 'http://minisovietnam.vn/mediacenter/media/images/products/1229/1146/water-soluble-double-headed-colored-pen-blue-0400013031.jpg';

print sha1FileName(url);

pathSaveTempImage = settings['IMAGES_STORE'] + '/full/temp.txt'

# Temp file
urllib.urlretrieve(url, pathSaveTempImage)

mm = magic.Magic(mime=True)
mime = mm.from_file(pathSaveTempImage)

print mime