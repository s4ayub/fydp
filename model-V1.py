import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.utils import class_weight

from PIL import Image

import os

#physical_devices = tf.config.list_physical_devices()
#tf.config.set_visible_devices(physical_devices[:2])

BATCH_SIZE = 1
imgs_per_seq = 39
img_h = 172
img_w = 128
img_c = 1

#imgs_per_seq = 19
#img_h = 345
#img_w = 257
#img_c = 1

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

print(model.summary())

print("Compliling model...")
#TODO: set learning rate (10^-4, but i think this is default so OK)
model.compile(optimizer=keras.optimizers.RMSprop(learning_rate=0.0001), #'rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
print("... compliling complete")
#sums = 0
#for layer in model.layers:
#    prod = 1
#    for i in layer.output_shape[1:]:
#        prod *= i
#    sums += prod
#print(sums)


'''
PREPROCESSING DATA
        1. Load imgs from stutter/no stutter dir
        2. Scale by ./255 [Possibly done by arnet]
        3. [Optional] Add option to visualize images
        4. Check to make sure each sequence of same length (prob do in step 1)
        5. Check to make sure final shape is correct

'''
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
    img = tf.reshape(img, (imgs_per_seq, img_w, img_h, img_c))
    return img

def process_path(file_path):
    label = get_label(file_path)
    img = decode_img(file_path)
    return img, label

def prepare_for_training(ds):
    ds.cache("cache")

    ds = ds.batch(BATCH_SIZE)

    # `prefetch` lets the dataset fetch batches in the background while the model
    # is training.
    ds = ds.prefetch(buffer_size=AUTOTUNE)

    return ds

list_ds = tf.data.Dataset.list_files(data_dir)
num_elements = tf.data.experimental.cardinality(list_ds).numpy()
list_ds = list_ds.shuffle(num_elements)

val_size = int(0.1*num_elements)
val_ds = list_ds.take(val_size) 
train_ds = list_ds.skip(val_size)

labeled_ds = train_ds.map(process_path, AUTOTUNE)
train_dataset = prepare_for_training(labeled_ds)

val_temp = val_ds.map(process_path, AUTOTUNE)
val_dataset = prepare_for_training(val_temp)

print("Training model...")
#class_weight = [4.0/7, 5.0/3]
model.fit(train_dataset, validation_data=val_dataset,epochs = 30)#, class_weight=class_weight)

model.save_weights("model_4s_log_newlr_val.h5")