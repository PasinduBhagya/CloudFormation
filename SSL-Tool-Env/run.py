import boto3
import logging
from botocore.exceptions import ClientError
import os

def uploadFiles():
    file_name = "SMPI/main.yaml"
    bucket = "pasindubhagyacloudformationfiles"
    folder_name = "SMPI/"
    object_name = folder_name + os.path.basename(file_name)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


    
if __name__ == "__main__":
    if uploadFiles():
        print("INFO: Uploading files successful.")
    