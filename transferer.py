# coding: utf-8
import os
import sys
from util.aws_transferer.config import config
from boto3.session import Session


# TODO output/models変数化
def check(output_dir, dir_name):
  print(config.BUCKET_NAME + output_dir + dir_name)
  s3client = Session().client('s3')
  response = s3client.list_objects(
    Bucket=config.BUCKET_NAME,
    Prefix=output_dir + dir_name + '/'
  )
  if "Contents" in response:
    print("S3上に指定のフォルダが既に存在してます。")
    sys.exit(1)


def send(text_file, output_dir, dir_name):
  os.system("aws s3 cp " + text_file + " s3://" + config.BUCKET_NAME + output_dir + dir_name + "/")
  print("sent " + text_file)

  os.system("aws s3 cp ./util/aws_transferer/data/*.log s3://" + config.BUCKET_NAME + output_dir + dir_name + "/")
  print("sent log data")
