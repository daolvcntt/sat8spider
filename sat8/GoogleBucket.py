import GoogleBucketConfig
import boto
import shutil

GOOGLE_STORAGE = GoogleBucketConfig.GOOGLE_STORAGE
BUCKET_NAME = GoogleBucketConfig.BUCKET_NAME

uri = boto.storage_uri('', GOOGLE_STORAGE)
header_values = {"x-goog-project-id": "search-1068"}

# If the default project is defined, call get_all_buckets() without arguments.
for bucket in uri.get_all_buckets(headers=header_values):
    print bucket.name

def uploadFileToBucket(fullPathFile, filePathUpload):
    f = open(fullPathFile, 'r')
    dst_uri = boto.storage_uri(BUCKET_NAME + filePathUpload, GOOGLE_STORAGE)
    dst_uri.new_key().set_contents_from_file(f)

localfile = '/home/justin/public_html/sat8spider/sat8/IMG_20150910_174739.jpg'
uploadFileToBucket(localfile, '/IMG_20150910_174739_test.jpg')

