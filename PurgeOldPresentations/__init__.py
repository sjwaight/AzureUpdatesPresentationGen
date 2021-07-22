import datetime
import logging
import os

import azure.functions as func
from azure.storage.blob import BlobServiceClient

#####
# Azure Function main entry point
#####
def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    try:

        blob_path = os.environ["LocalTempFilePath"] + "AzureUpdate-"

        blob_client = BlobServiceClient.from_connection_string(conn_str=os.environ["PowerPointAccountConnection"])
        container_client = blob_client.get_container_client(os.environ["PowerPointContainer"])

        old_presentations = container_client.list_blobs(name_starts_with=blob_path)
        container_client.delete_blobs(*old_presentations)

        logging.info("Deleted files.")
    
    except:
        logging.error("Failed file processing.")