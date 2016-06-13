from googleapiclient import discovery
from googleapiclient import http

from oauth2client.client import GoogleCredentials

from Functions import *
import urllib

def google_bucket_create_service():
    # Get the application default credentials. When running locally, these are
    # available after running `gcloud init`. When running on compute
    # engine, these are available from the environment.
    credentials = GoogleCredentials.get_application_default()

    # Construct the service object for interacting with the Cloud Storage API -
    # the 'storage' service, at version 'v1'.
    # You can browse other available api services and versions here:
    #     http://g.co/dev/api-client-library/python/apis/
    return discovery.build('storage', 'v1', credentials=credentials)


def google_bucket_upload_object(bucket, filepath, pathSaveBucket):
    service = google_bucket_create_service()

    # This is the request body as specified:
    # http://g.co/cloud/storage/docs/json_api/v1/objects/insert#request

    filename = get_file_name(filepath)

    body = {
        'name': pathSaveBucket,
    }

    # If specified, create the access control objects and add them to the

    # https://cloud.google.com/storage/docs/json_api/v1/objectAccessControls#resource-representations
    body['acl'] = []
    body['acl'].append({
        'entity': 'allUsers',
        'role': 'READER',
        'name': 'allUsers'
    });

    body['acl'].append({
        'entity': 'user-cong.itsoft@gmail.com',
        'role': 'OWNER',
        'email': 'cong.itsoft@gmail.com'
    })

    # Now insert them into the specified bucket as a media insertion.
    # http://g.co/dev/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#insert

    with open(filepath, 'rb') as f:
        req = service.objects().insert(
            bucket=bucket, body=body,
            # You can also just set media_body=filename, but # for the sake of
            # demonstration, pass in the more generic file handle, which could
            # very well be a StringIO or similar.
            media_body=http.MediaIoBaseUpload(f, get_mime_type(filepath)))
        resp = req.execute()

    return resp


def google_bucket_get_object(bucket, filename, out_file):
    service = create_service()

    # Use get_media instead of get to get the actual contents of the object.
    # http://g.co/dev/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#get_media
    req = service.objects().get_media(bucket=bucket, object=filename)

    downloader = http.MediaIoBaseDownload(out_file, req)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download {}%.".format(int(status.progress() * 100)))

    return out_file


def google_bucket_delete_object(bucket, filename):
    service = create_service()

    req = service.objects().delete(bucket=bucket, object=filename)
    resp = req.execute()

    return resp


def google_bucket_bucket_metadata(bucket):
    """Retrieves metadata about the given bucket."""
    service = create_service()

    # Make a request to buckets.get to retrieve a list of objects in the
    # specified bucket.
    req = service.buckets().get(bucket=bucket)
    return req.execute()


def google_bucket_list_bucket(bucket):
    """Returns a list of metadata of the objects within the given bucket."""
    service = create_service()

    # Create a request to objects.list to retrieve a list of objects.
    fields_to_return = \
        'nextPageToken,items(name,size,contentType,metadata(my-key))'
    req = service.objects().list(bucket=bucket, fields=fields_to_return)

    all_objects = []
    # If you have too many items to list in one request, list_next() will
    # automatically handle paging with the pageToken.
    while req:
        resp = req.execute()
        all_objects.extend(resp.get('items', []))
        req = service.objects().list_next(req, resp)
    return all_objects