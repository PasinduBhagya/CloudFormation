import boto3
import logging
from botocore.exceptions import ClientError
import os
import time

randomS3BucketName = "pasindubhagyacf" + str(int(round(time.time() * 1000)))
myregion = "ap-southeast-1"
cloudformationFilePath = "SMPI/"
cloudformationMainFilePath = "SMPI/main.yaml"

def createBucket():
    s3_client = boto3.client('s3')
    try:
        s3_client.create_bucket(Bucket=randomS3BucketName, CreateBucketConfiguration={'LocationConstraint': myregion})
    except ClientError as e:
        logging.error(e)
        return False
    return True

def uploadFiles():
    uploadFileNames = []
    for dirpath, dirnames, filenames in os.walk(cloudformationFilePath):
        for filename in filenames:
            uploadFileNames.append(os.path.join(dirpath, filename))
    
    for singleFile in uploadFileNames:
        fileName = singleFile.split("\\")[-1]
        folderPath = singleFile.split("\\")[0]

        object_name = folderPath + "/" + os.path.basename(fileName)
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(singleFile, randomS3BucketName, object_name)
        except ClientError as e:
            logging.error(e)
            return False
    
    return True

def deleteBucket():
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    
    try:
        bucketObjects = s3_resource.Bucket(randomS3BucketName).objects.all()
        bucketObjects.delete()
        s3_client.delete_bucket(Bucket=randomS3BucketName)
        print(f"INFO: Bucket {randomS3BucketName} and its objects have been deleted successfully!")
    except ClientError as e:
        logging.error(e)
        return False

    return True
   
def createStack():
    print("INFO: Starting stack creation")
    cloudformation_client = boto3.client('cloudformation')
    with open(cloudformationMainFilePath, 'r') as f:
        template_body = f.read()

    try:
        response = cloudformation_client.create_stack(
            StackName='SMPI',
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_NAMED_IAM'],
            Parameters=[
                {
                    'ParameterKey': 'BucketName',
                    'ParameterValue': randomS3BucketName
                }
            ]
        )
        print("INFO: Stack ID " + response['StackId'])
    except ClientError as e:
        logging.error(e)
        return False   
    
    return True 


if __name__ == "__main__":
    if createBucket():
        print("INFO: Bucket created successfully.")
    if uploadFiles():
        print("INFO: Uploading files successful.")
    if createStack():
        print("INFO: Stack created successfully.")
        
    print(f'''{"="*100}\nEnter "Delete" if you want to delete the Bucket {randomS3BucketName}\n{"="*100}''')
    print("> ", end="")
    if input() == "Delete":
        print("INFO: Deleting the bucket and its objects.")
        if deleteBucket():
            print("INFO: Bucket deleted successfully.")
    else:
        print(f"INFO: Bucket {randomS3BucketName} not deleted.")
        
    