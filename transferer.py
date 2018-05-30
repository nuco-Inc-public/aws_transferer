# coding: utf-8
import os
import sys
import io
from boto3.session import boto3, Session
from enum import Enum

class S3Manager():

  class ContentType(Enum):
    TEXT_PLAIN = 'text/plain'
    BINARY = 'binary/octet-stream'
    IMAGE = 'image/jpeg'


  def __init__(self, bucket_name):
    session = Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                  aws_secret_access_key=os.environ['AWS_SECRET_KEY'])

    self.s3 = session.resource('s3')
    self.bucket_name = bucket_name


  def download(self, name, save_path):
    o = self.s3.Object(self.bucket_name, name)
    o.download_file(save_path)


  def upload(self, content, name, content_type=ContentType.TEXT_PLAIN):
    '''

    Args:
      content (bytes): 
      name (str):


    Return:
      boolean
    '''
    obj = self.s3.Object(self.bucket_name, name)
    response = obj.put(
      ACL='public-read',
      Body=content,
      ContentType=content_type.value,
    )


  def exists(self, dir_name):
    s3client = Session(
      aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
      aws_secret_access_key=os.environ['AWS_SECRET_KEY']).client('s3')
    response = s3client.list_objects(
        Bucket=self.bucket_name,
        Prefix= dir_name + '/'
      )
    return "Contents" in response