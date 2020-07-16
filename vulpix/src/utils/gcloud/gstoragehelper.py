import sys
import os
import traceback
from vulpix.src.main.skulk_objects import SkulkObject as sb
from vulpix.src.utils.error_book.errorbook import ErrorBook
from google.cloud import storage

sys.path.append(sb.skulk_path)
log = None
error = None
class StorageHelper:
    def __init__(self):
        global log, error
        log = sb.log
        error = ErrorBook()

    def ishrhdPresetInGstorage(self, tdate, symbol, contract_type="STK"):
        try:
            client = storage.Client()
            bucket = client.bucket(sb.hrhd_bucket)
            blob = bucket.get_blob(os.path.join(contract_type,tdate,symbol+".csv"))
            if blob.exists(client):
                dest = os.path.join(sb.hrhd_local_path,blob.name)
                if not os.path.exists(os.path.dirname(dest)):
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                blob.download_to_filename(os.path.join(sb.hrhd_local_path,blob.name))
                log.info(
                    "HRHD Blob {} downloaded to {} for {} - {}".format(
                        blob.name, os.path.join(sb.hrhd_local_path,blob.name, tdate, symbol)
                    )
                )
                return blob.name
            return None
        except Exception as e:
            error.handle(e, traceback.format_exc(),tdate , symbol, type)