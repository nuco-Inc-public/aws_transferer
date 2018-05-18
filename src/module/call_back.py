# coding: utf-8
import os
import keras
from config import config


class CheckPointTransferer(keras.callbacks.ModelCheckpoint):

  
  def __init__(self, file_path, save_dir, name, verbose=0, save_freq=1):
    super(CheckPointTransferer, self).__init__(file_path, verbose=verbose)
    self.save_freq = save_freq
    self.file_path = file_path
    self.save_dir = save_dir
    self.name = name


  def on_epoch_end(self, epoch, logs={}):
    super(CheckPointTransferer, self).on_epoch_end(epoch, logs=logs)
    os.system("aws s3 cp " + self.file_path + " s3://" + config.BUCKET_NAME + self.save_dir + self.name + "/" +"epoch" + str(epoch) + ".h5")
    print("saved model")