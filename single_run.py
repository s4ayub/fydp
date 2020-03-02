import tensorflow as tf
from tensorflow import keras
import numpy as np

from PIL import Image

import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--inputPath", "-i", help="/home/justin/github/fydp/data/*/*", required=True)

args = parser.parse_args()

BATCH_SIZE = 1
imgs_per_seq = 39
img_h = 172
img_w = 128
img_c = 1

AUTOTUNE = tf.data.experimental.AUTOTUNE
data_dir = args.inputPath + "*" #"/home/justin/github/fydp/data/*/*"


def decode_img(file_path):
    img = tf.io.read_file(file_path)
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=1)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    img = tf.reshape(img, (1, imgs_per_seq, img_w, img_h, img_c))
    return img, tf.strings.split(file_path, os.path.sep)[-1].numpy().decode("utf-8")


list_ds = tf.data.Dataset.list_files(data_dir)
#data = list_ds.map(decode_img, AUTOTUNE)

loaded_model = tf.keras.models.load_model("/home/justin/github/fydp/", compile=True)

acc1 = 0
acc2 = 0
summ = 0

results_s =[]

print("Model Loaded")

for file_path in list_ds.take(100):
    img, path = decode_img(file_path)
    output = loaded_model.predict(img)
    ind = np.argmax(output)
    summ += 1
    if ind == 0:
        acc1 += 1
    else: 
        acc2 += 1
        #if(output[0][ind] <= 0.95):
        #    acc1 += 1
        #else:
        #    acc2 += 1
        results_s.append(path)


print(acc1, acc2, summ)
print(results_s)

