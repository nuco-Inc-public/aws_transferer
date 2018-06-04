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
    a = os.environ.get('AWS_ACCESS_KEY')
    s = os.environ.get('AWS_SECRET_KEY')
    a_key = 'hoge' if a == None else os.environ['AWS_ACCESS_KEY']
    s_key = 'fuga' if s == None else os.environ['AWS_SECRET_KEY']
    session = Session(a_key, s_key)

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
    s3client = Session(
      aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
      aws_secret_access_key=os.environ['AWS_SECRET_KEY']).client('s3')
    response = s3client.list_objects(
        Bucket=self.bucket_name,
        Prefix= dir_name + '/'
      )
    return "Contents" in response
