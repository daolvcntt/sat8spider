# -*- coding: utf-8 -*-

import boto
import gcs_oauth2_boto_plugin
import os
import shutil
import StringIO
import tempfile
import time

# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'

# URI scheme for accessing local files.
LOCAL_FILE = 'file'

# Fallback logic. In https://console.cloud.google.com/
# under Credentials, create a new client ID for an installed application.
# Required only if you have not configured client ID/secret in
# the .boto file or as environment variables.
CLIENT_ID = '357469820882-rafsas8umtg6t7c11oqpskv3q9a55k8p.apps.googleusercontent.com'
CLIENT_SECRET = 'MXoq05non8N3SGP3ZzlhryHy'

BUCKET_NAME = 'static-giaca-org'

gcs_oauth2_boto_plugin.SetFallbackClientIdAndSecret(CLIENT_ID, CLIENT_SECRET)