# -*- coding: utf-8 -*-

import boto
import gcs_oauth2_boto_plugin
import os
import shutil
import StringIO
import tempfile
import time

import env

# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'

# URI scheme for accessing local files.
LOCAL_FILE = 'file'

# Fallback logic. In https://console.cloud.google.com/
# under Credentials, create a new client ID for an installed application.
# Required only if you have not configured client ID/secret in
# the .boto file or as environment variables.
CLIENT_ID = env.GOOGLE_STORAGE_CLIENT_ID
CLIENT_SECRET = env.GOOGLE_STORAGE_CLIENT_SECRET

BUCKET_NAME = env.GOOGLE_STORAGE_BUCKET_NAME

gcs_oauth2_boto_plugin.SetFallbackClientIdAndSecret(CLIENT_ID, CLIENT_SECRET)