import unittest

from Helpers.Google_Bucket import google_bucket_upload_object

class GoogleBucketTest(unittest.TestCase):

    def test_upload_object(self):
        bucket = 'static.giaca.org'
        filename = '/home/justin/Desktop/Girls/91.jpg'
        response = google_bucket_upload_object(bucket, filename)
        self.assetEqual(true, response)

if __name__ == '__main__':
    unittest.main()