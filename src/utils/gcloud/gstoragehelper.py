import sys
import os
import traceback
from src.main.skulk_objects import SkulkObject as sb
from src.utils.error_book.errorbook import ErrorBook
from google.cloud import storage

sys.path.append(sb.skulk_path)
log = None
error = None
class StorageHelper:
    def __init__(self):
        global log, error
        log = sb.log
        error = ErrorBook()

    def ishrhdPresetInGstorage(self, tdate, symbol):
        try:
            client = storage.Client()
            bucket = client.bucket(sb.hrhd_bucket)
            blob = bucket.get_blob(os.path.join(tdate,symbol+".csv"))
            if blob.exists(client):
                return blob.name
            return None
        except Exception as e:
            error.handle(e, traceback.format_exc(),tdate , symbol)