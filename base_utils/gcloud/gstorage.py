import sys
import os
import traceback
from base_utils.error_book.errorbook import ErrorBook
from google.cloud import storage

log = None
error = None
class GStorage:
    def __init__(self, logger):
        global log, error
        log = logger
        error = ErrorBook(logger)

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            if log is not None:
                log.info(
                    "File {} uploaded to {}.".format(
                        source_file_name, destination_blob_name
                    )
                )
        except Exception as e:
            error.handle(e, traceback.format_exc(), bucket_name, source_file_name, destination_blob_name)


    def downloadBlob(self,bucket_name, blobname, save_path):
        try:
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.get_blob(blobname)
            if blob is not None:
                dest = os.path.join(save_path, blob.name)
                if not os.path.exists(os.path.dirname(dest)):
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                blob.download_to_filename(dest)
                return dest
            log.info("Blob not found for {}".format(blobname))
            return None
        except Exception as e:
            error.handle(e, traceback.format_exc(), bucket, blobname, type)
            return None

    def isBlobExist(self,bucket, blobname):
        try:
            client = storage.Client()
            bucket = client.bucket(bucket)
            blob = bucket.get_blob(blobname)
            if blob is not None:
                return blob.name
            return None
        except Exception as e:
            error.handle(e, traceback.format_exc(), bucket, blobname, type)



