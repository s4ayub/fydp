import tensorflow as tf
from tensorflow import keras
import numpy as np

from PIL import Image

import os

BATCH_SIZE = 1
imgs_per_seq = 39
img_h = 172
img_w = 128
img_c = 1

AUTOTUNE = tf.data.experimental.AUTOTUNE
CLASS_NAMES = np.array(["no_stutter", "sound_repetition"])
data_dir = "/home/justin/github/fydp/data/*/*"

def get_label(file_path):
    parts = tf.strings.split(file_path, os.path.sep)
    return parts[-2] == CLASS_NAMES

def decode_img(file_path):
    img = tf.io.read_file(file_path)
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=1)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    img = tf.reshape(img, (1, imgs_per_seq, img_w, img_h, img_c))
    return img

def process_path(file_path):
    label = get_label(file_path)
    img = decode_img(file_path)
    return img, label

list_ds = tf.data.Dataset.list_files(data_dir)
labeled_ds = list_ds.map(process_path, AUTOTUNE)

#tf.keras.models.save_model(model, "/home/justin/github/fydp/", save_format='tf')
loaded_model = tf.keras.models.load_model("/home/justin/github/fydp/", compile=True)

acc1 = 0
sum1 = 0
acc2 = 0
sum2 = 0

print("Model Saved")

for img, label in labeled_ds.take(585):
    output = loaded_model.predict(img)
    ind = np.argmax(output)
    if label.numpy()[0]:
        sum1 += 1
        if ind == 0:
            acc1 += 1
    else:
        sum2 += 1
        if ind == 1:
            acc2 += 1
print(acc1, sum1, acc1/sum1)
print(acc2, sum2, acc2/sum2)