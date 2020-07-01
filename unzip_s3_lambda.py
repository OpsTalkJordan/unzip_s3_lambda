import boto3
import logging
import os
import sys
from botocore.exceptions import ClientError
from urllib.parse import unquote_plus
from zipfile import ZipFile

# Pulling target bucket from Lambda environment
target_bucket =  os.environ['TARGET_BUCKET']

# Establishing S3 client used by downloads and uploads
s3_client = boto3.client('s3')

def download_object_from_s3(object_key, bucket, file_name=None):
    """Download an object from an S3 bucket

    :param object_key: Object to download
    :param bucket: Bucket to download from
    :param file_name: File name for downloaded object. If not specified then object_key is used
    :return: Client response if file was downloaded, else error
    """

    # If file_name was not specified, use object_key
    if file_name is None:
        file_name = object_key

    # Download the object
    try:
        response = s3_client.download_file(bucket, object_key, file_name)
    except ClientError as e:
        logging.error(e)
        return e
    return response

def upload_file_to_s3(file_name, bucket, object_key=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_key: S3 object name. If not specified then file_name is used
    :return: Client response if file was uploaded, else error
    """

    # If S3 object_key was not specified, use file_name
    if object_key is None:
        object_key = file_name

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_key)
    except ClientError as e:
        logging.error(e)
        return e
    return response

def extract_zip(file_name, destination_dir):
    """Extract a zip file

    :param file_name: Zip file to extract
    :param destination_dir: Directory to extract contents into
    :return file_list[]: List of extracted filenames
    """
    # Create a ZipFile Object and load zip into it
    with ZipFile(file_name, 'r') as zip_obj:
        file_list = zip_obj.namelist()
        zip_obj.extractall(destination_dir)
        return file_list

def lambda_handler(event, context):
    # Parse s3 event, iterate through records
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        object_key = unquote_plus(record['s3']['object']['key'])
        
        # Setting up vars to use in path names
        tmp_key = object_key.replace('/', '')
        download_path = '/tmp/{}'.format(tmp_key)
        extract_dir = '/tmp/{}-unzippped/'.format(tmp_key)
        
        # Downloading and extracting zip files
        download_object_from_s3(object_key, bucket)
        extracted_files = extract_zip(download_path, extract_dir)

        # Iterating over list of extracted files, upload to s3
        for item in extracted_files:
            upload_file_to_s3(item, target_bucket)
