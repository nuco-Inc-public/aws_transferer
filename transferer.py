# coding: utf-8
import os
import sys
from util.aws_transferer.config import config
from boto3.session import Session

def init():
  os.system("rm -r ./util/aws_transferer/data/*")

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

# TODO 評価のみの場合、.h5ファイルの存在チェック


def send(text_file, output_dir, dir_name):
  os.system("aws s3 cp " + text_file + " s3://" + config.BUCKET_NAME + output_dir + dir_name + "/")
  print("sent " + text_file)

  os.system("aws s3 cp ./util/aws_transferer/data/*.log s3://" + config.BUCKET_NAME + output_dir + dir_name + "/")
  print("sent log data")


def get_epoch_param(output_dir, dir_name, epoch):
  print("get epoch param from S3 ...")
  os.system("aws s3 cp s3://" + config.BUCKET_NAME + output_dir + dir_name + "/epoch" + str(epoch - 1) + ".h5" + config.RECEIVE_DIR)

