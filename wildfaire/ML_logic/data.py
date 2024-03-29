import pandas as pd
import os
import re
import tensorflow as tf

from google.cloud import storage
from colorama import Fore, Style
from pathlib import Path              ####USEFUL IF WE WANT TO TRAIN ON THE CLOUD

from wildfaire.params import *

def get_dataset(file_pattern: str,
    data_size = 64,
    sample_size = 32,
    batch_size = 100,
    num_in_channels = 12,
    compression_type = None,
    clip_and_normalize = False,
    clip_and_rescale = False,
    random_crop = True,
    center_crop = False) -> tf.data.Dataset:
  """Gets the dataset from the file pattern.

  Args:
    file_pattern: Input file pattern.
    data_size: Size of tiles (square) as read from input files.
    sample_size: Size the tiles (square) when input into the model.
    batch_size: Batch size.
    num_in_channels: Number of input channels.
    compression_type: Type of compression used for the input files.
    clip_and_normalize: True if the data should be clipped and normalized, False
      otherwise.
    clip_and_rescale: True if the data should be clipped and rescaled, False
      otherwise.
    random_crop: True if the data should be randomly cropped.
    center_crop: True if the data shoulde be cropped in the center.

  Returns:
    A tf.TensorFlow dataset loaded from the input file pattern, with features
    described in the constants, and with the shapes determined from the input
    parameters to this function.
  """
  if (clip_and_normalize and clip_and_rescale):
    raise ValueError('Cannot have both normalize and rescale.')
  dataset = tf.data.Dataset.list_files(file_pattern)
  dataset = dataset.interleave(
      lambda x: tf.data.TFRecordDataset(x, compression_type=compression_type),
      num_parallel_calls=tf.data.experimental.AUTOTUNE)
  dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
  dataset = dataset.map(
      lambda x: _parse_fn(  # pylint: disable=g-long-lambda
          x, data_size, sample_size, num_in_channels, clip_and_normalize,
          clip_and_rescale, random_crop, center_crop),
      num_parallel_calls=tf.data.experimental.AUTOTUNE)
  dataset = dataset.batch(batch_size)
  dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
  return dataset

def get_file_paths():
    '''
    This function returns 3 strings
    file paths for the train, test and evaluation datasets

    Call it like this: train_pattern, test_pattern, eval_pattern = get_file_paths()

    '''
    folder = os.getcwd()
    if folder.endswith('hooks'):
        name = os.path.join('..', '..', 'raw_data')
    elif directory.endswith('wildfaire'):
        name = os.path.join('..', 'raw_data')
    else:
        name = 'raw_data'
    train_pattern = os.path.join(name, 'next_day_wildfire_spread_train*')
    test_pattern = os.path.join(name, 'next_day_wildfire_spread_test*')
    eval_pattern = os.path.join(name, 'next_day_wildfire_spread_eval*')
    return train_pattern, test_pattern, eval_pattern
