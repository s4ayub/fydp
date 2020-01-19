import tensorflow as tf
from tensorflow import keras
import numpy as np

from matplotlib import image
from matplotlib import pyplot

from os import listdir


 #RESNET
#
# image dimensions
#

batch = 3
img_h = 257
img_w = 5 #replace
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

    x = keras.layers.TimeDistributed(keras.layers.Flatten())(x)		# Flatten so that dense can take in 
    x = keras.layers.TimeDistributed(keras.layers.Dense(100))(x)	# Randomly put 100 since paper does not specify this 

    return x

def lstm_network(x):
	# Might needs to set return_sequences=false, return_state=false 
    x = keras.layers.Bidirectional(keras.layers.LSTM(512, return_sequences=True))(x)
    # (?) Missing: "Dropout rates of 0.2 and 0.4 are utilized after each recurrent layer"
    x = keras.layers.Bidirectional(keras.layers.LSTM(512))(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(2)(x)
    x = keras.layers.Activation('softmax')(x)  	
    return x

# 5 sequences, size image and channel
image_tensor = keras.Input(shape=(5, 256, 256, 1))
residual = residual_network(image_tensor)
lstm = lstm_network(residual)
  
model = keras.Model(inputs=[image_tensor], outputs=[lstm])
print(model.summary())

print("Compliling model...")
model.compile(optimizer='rmsprop',
				loss='binary_crossentropy',
				metrics=['accuracy'])

print("... compliling complete")

#TODO: set learning rate (10^-4, but i think this is default so OK)

''' -------------- Preprocessing data 
	1. Load all image from  dir
	2. Downsize (?)  
	2. Scale by ./255 [Already done by arnet ]
	3. Pad the sequence so that  all are same length (Probably dont need to do this)
	4. 
	'''

# find a better way to load all the data 
# TODO: load all the data, rn this is just a sample

training_imgs = list()
for filename in listdir('/home/harminder/fydp/train_imgs'):
	img_data = image.imread('/home/harminder/fydp/train_imgs/' + filename)
	training_imgs.append(img_data)

print(str(len(training_imgs)))	


x_train = np.reshape(training_imgs, (len(training_imgs)/5), 5) # recall 5 is random, real: 400 
y_train = np.full(x_train.size, 0, dtype=np.float)

print("Training model...")
model.fit(x_train, y_train, 
			batch_size=1,
			epochs=30)
			#validation_data=[x_test, y_test])

			