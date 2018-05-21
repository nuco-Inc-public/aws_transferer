# coding: utf-8
import os
import sys
from util.aws_transferer.config import config
from boto3.session import Session

def init():
  os.system("rm -r ./util/aws_transferer/data/*.h5")

# TODO output/models変数化
def check(train, dir_name):
  print(config.BUCKET_NAME + config.OUTPUT_DIR + dir_name + config.MODELS)
  s3client = Session().client('s3')
  response = s3client.list_objects(
      Bucket=config.BUCKET_NAME,
      Prefix=config.OUTPUT_DIR + dir_name + '/'
    )
  if train:
    if "Contents" in response:
      print("S3上に指定のフォルダが既に存在してます。")
      sys.exit(1)
  else:
    if "Contents" not in response:
      print("S3上に指定のフォルダが存在しません。")
      sys.exit(1)


# TODO 評価のみの場合、.h5ファイルの存在チェック


def send(text_file, dir_name):
  os.system("aws s3 cp " + text_file + " s3://" + config.BUCKET_NAME + config.OUTPUT_DIR  + dir_name + "/" + config.MODELS)
  print("sent " + text_file)

  os.system("aws s3 cp ./util/aws_transferer/data/*.log s3://" + config.BUCKET_NAME + config.OUTPUT_DIR  + dir_name + "/" + config.MODELS)
  print("sent log data")

  os.system("aws s3 cp ./util/aws_transferer/data/grad_cam s3://" + config.BUCKET_NAME + config.OUTPUT_DIR + dir_name + "/" +config.THUMBNAILS + config.NORMAL)
  print("sent grad cam data")

  os.system("aws s3 cp ./util/aws_transferer/data/normal s3://" + config.BUCKET_NAME + config.OUTPUT_DIR + dir_name + "/" +config.THUMBNAILS + config.GRAD_CAM)
  print("sent grad normal img data")


def get_epoch_param(dir_name, epoch):
  print("get epoch param from S3 ...")
  os.system("aws s3 cp s3://" + config.BUCKET_NAME + config.OUTPUT_DIR + dir_name + "/" + config.MODELS + "epoch" + str(epoch - 1) + ".h5 " + config.RECIEVE_DIR)

