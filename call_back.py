# coding: utf-8
import os
import keras
from util.aws_transferer.config import config


class CheckPointTransferer(keras.callbacks.ModelCheckpoint):

  
  def __init__(self, file_path, name, verbose=0, save_freq=1):
    super(CheckPointTransferer, self).__init__(file_path, verbose=verbose)
    self.save_freq = save_freq
    self.file_path = file_path
    self.name = name

  #[TODO] fix os.system
  def on_epoch_end(self, epoch, logs={}):
    super(CheckPointTransferer, self).on_epoch_end(epoch, logs=logs)
    os.system("aws s3 cp " + self.file_path + " s3://" + config.BUCKET_NAME + config.OUTPUT + self.name + "/" + config.MODELS + "epoch" + str(epoch) + ".h5")
    print("saved model")