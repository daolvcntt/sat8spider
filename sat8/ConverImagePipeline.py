import hashlib
import urllib
from scrapy.selector import Selector
from scrapy.conf import settings

class ConverImagePipeline:

   def process_item(self, item, spider):
        if spider.name == 'blog_spider':
            sel = Selector(text=item['content'])
            image_links = sel.xpath('//img/@src');
            for pl in image_links:
                url = pl.extract();
                imageName = hashlib.sha1(url).hexdigest() + '.jpg'
                urllib.urlretrieve(url, settings['IMAGES_STORE'] + '/posts/' + imageName)