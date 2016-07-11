from scrapy.conf import settings
from sat8.Helpers.Functions import *
from sat8.Helpers.Google_Bucket import *

images = [
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/180x350/9df78eab33525d08d6e5fb8d27136e95/v/1/v10-white_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/v/1/v10-black_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/v/1/v10-blue_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/v/1/v10-gold_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/v/1/v10-navy_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/v/1/v10-white_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/v/1/v10-black-back_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/v/1/v10-gold-back.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/v/1/v10-white-back_1.png',

    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-silver_1_2.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-gold_1_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-gray_1_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-silver_1_2.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-gold-back_1_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-gray-back_1_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-silver-back_1_1.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-1_1_1.jpg',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-3_1_1.jpg',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/thumbnail/60x60/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-2_1_1.jpg',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-2_1_1.jpg',

    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/180x350/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-silver_1_2.png',

    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/180x350/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-gold_4.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-gold_4.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-gray_4.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-silver_4.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-gold-back_4.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-gray-back_4.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-silver-back_4.png',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-1_2.jpg',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-2_2.jpg',
    # 'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/n/o/note-3-3_2.jpg'

    'http://cellphones.com.vn/media/catalog/product/cache/1/image/180x350/9df78eab33525d08d6e5fb8d27136e95/i/p/iphone-6-plus-silver_1_1_1.png',
    'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/i/p/iphone-6-plus-gold_2_1.png',
    'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/i/p/iphone-6-plus-gray_2_1.png',
    'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/i/p/iphone-6-plus-silver_1_1_1.png',
    'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/i/p/iphone-6-p-2_2_1.png',
    'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/i/p/iphone-6-p-3_1_1_1.png',
    'http://cellphones.com.vn/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/i/p/iphone-6-p-1_1_1_1.png'
]

for image in images:
    print image + "\n"
    imageName = sha1FileName(image)

    thumbs = downloadImageFromUrl(image)

    # Upload bucket
    google_bucket_upload_object('static.giaca.org', thumbs['full'], 'uploads/full/' + imageName)
    google_bucket_upload_object('static.giaca.org', thumbs['big'], 'uploads/thumbs/big/' + imageName)
    google_bucket_upload_object('static.giaca.org', thumbs['small'], 'uploads/thumbs/small/' + imageName)