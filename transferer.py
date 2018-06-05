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
    '''
      s3Managerのコンストラクタ
      Args:
          bucket_name(string): バケット名
      Returns:
          なし
    '''
    self.a_key = os.environ.get('AWS_ACCESS_KEY')
    self.s_key = os.environ.get('AWS_SECRET_KEY')
    self.session = Session(self.a_key, self.s_key) if self.a_key and self.s_key else Session()
    self.s3 = session.resource('s3')
    self.bucket_name = bucket_name


  def download(self, name, save_path):
    '''
      s3からファイルをダウンロードする
      Args:
          name(string): ファイル名
          save_path(string): 保存先パス
      Returns:
          なし
    '''
    o = self.s3.Object(self.bucket_name, name)
    o.download_file(save_path)


  def upload(self, content, name, content_type=ContentType.TEXT_PLAIN):
    '''
      s3にファイルをアップロードする
      Args:
          content: アップロードするコンテンツデータ
          name(string): ファイル名
          content_type(string): s3Managerのコンテンツ種別
      Returns:
          なし
    '''
    obj = self.s3.Object(self.bucket_name, name)
    response = obj.put(
      ACL='public-read',
      Body=content,
      ContentType=content_type.value,
    )


  def exists(self, dir_name):
    '''
      s3上に指定ディレクトリ階層が存在するかチェックする
      Args:
          dir_name(string): 
      Returns:
          boolean: 階層の存在有無
    '''
    s3client = self.session.client('s3')
    response = s3client.list_objects(
        Bucket=self.bucket_name,
        Prefix= dir_name + '/'
      )
    return "Contents" in response
