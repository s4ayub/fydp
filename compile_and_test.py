import tensorflow as tf
from tensorflow import keras
import numpy as np

from PIL import Image

import os

#physical_devices = tf.config.list_physical_devices()
#tf.config.set_visible_devices(physical_devices[:2])

#BATCH_SIZE = 1
#imgs_per_seq = 19
#img_h = 345
#img_w = 257
#img_c = 1


BATCH_SIZE = 1
imgs_per_seq = 39
img_h = 172
img_w = 128
img_c = 1

def residual_network(x):
    def add_common_layers(y):
        y = keras.layers.TimeDistributed(keras.layers.BatchNormalization())(y)
        y = keras.layers.TimeDistributed(keras.layers.ReLU())(y)

        return y

    def residual_block(y, nb_channels_in, nb_channels_out, _strides=(2, 2)):
        shortcut = y

        y = keras.layers.TimeDistributed(keras.layers.Conv2D(nb_channels_in, kernel_size=(3, 3), strides=(1, 1), padding='same'))(y)
        y = add_common_layers(y)

        y = keras.layers.TimeDistributed(keras.layers.Conv2D(nb_channels_out, kernel_size=(3, 3), strides=(2, 2), padding='same'))(y)
        y = add_common_layers(y)

        y = keras.layers.TimeDistributed(keras.layers.Conv2D(nb_channels_out, kernel_size=(3, 3), strides=(1, 1), padding='same'))(y)
        y = keras.layers.TimeDistributed(keras.layers.BatchNormalization())(y)

        shortcut = keras.layers.TimeDistributed(keras.layers.Conv2D(nb_channels_out, kernel_size=(3, 3), strides=_strides, padding='same'))(shortcut)
        shortcut = keras.layers.TimeDistributed(keras.layers.BatchNormalization())(shortcut)

        y = keras.layers.add([shortcut, y])

        y = keras.layers.TimeDistributed(keras.layers.ReLU())(y)

        return y

    # conv1
    x = keras.layers.TimeDistributed(keras.layers.Conv2D(64, kernel_size=(7, 7), padding='same'))(x)
    x = add_common_layers(x)

    strides = (2, 2)
    x = residual_block(x, 32, 64)

    x = residual_block(x, 64, 128)

    x = residual_block(x, 128, 128)

    x = residual_block(x, 128, 64)

    x = residual_block(x, 64, 32)

    x = residual_block(x, 32, 16)

    x = keras.layers.TimeDistributed(keras.layers.Flatten())(x)         # Flatten so that dense can take in
    x = keras.layers.TimeDistributed(keras.layers.Dense(100))(x)        # Randomly put 100 since paper does not specify this

    return x

def lstm_network(x):
    x = keras.layers.Bidirectional(keras.layers.LSTM(512, return_sequences=True))(x)
    #x = keras.layers.LSTM(512, return_sequences=True)(x)
    x = keras.layers.Dropout(0.2)(x)
    #x = keras.layers.LSTM(512)(x)
    x = keras.layers.Bidirectional(keras.layers.LSTM(512))(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(2)(x)
    x = keras.layers.Activation('softmax')(x)
    return x

image_tensor = keras.Input(shape=(imgs_per_seq, img_w, img_h, img_c))
residual = residual_network(image_tensor)
lstm = lstm_network(residual)

model = keras.Model(inputs=[image_tensor], outputs=[lstm])

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

model.compile(optimizer=keras.optimizers.RMSprop(learning_rate=0.0001),#'rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.load_weights("/home/justin/github/fydp/model_weights/model_4s_log_newlr.h5")

acc1 = 0
sum1 = 0
acc2 = 0
sum2 = 0

for img, label in labeled_ds.take(585):
    output = model.predict(img)
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
