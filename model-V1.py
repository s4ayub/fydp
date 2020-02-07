import tensorflow as tf
from tensorflow import keras
import numpy as np

from matplotlib import image
from matplotlib import pyplot

import os

imgs_per_seq = 39
img_h = 345
img_w = 257  
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
    x = keras.layers.Bidirectional(keras.layers.LSTM(512, return_sequences=True))(x)
    # (?) Missing: "Dropout rates of 0.2 and 0.4 are utilized after each recurrent layer"
    # But where would it go? after each bidirectional layer?
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
model.compile(optimizer='rmsprop',
				loss='binary_crossentropy',
				metrics=['accuracy'])
print("... compliling complete")



'''
PREPROCESSING DATA
	1. Load imgs from stutter/no stutter dir 
	2. Scale by ./255 [Possibly done by arnet]
	3. [Optional] Add option to visualize images 
	4. Check to make sure each sequence of same length (prob do in step 1)
	5. Check to make sure final shape is correct

'''

stutter_dir = "/home/harminder/fydp/train_imgs/stutterA/"
no_stutter_dir = "/home/harminder/fydp/train_imgs/noStutter/"

train_seqs = []
train_labels = []

for fldr_name in os.listdir(stutter_dir): # assumes everything within dir is a dir 
	imgs = []

	for file_name in os.listdir(stutter_dir + fldr_name):
		img_data = image.imread(stutter_dir + fldr_name + '/' + file_name)
		img_data = np.reshape(img_data,(img_w,img_h,img_c))
		imgs.append(img_data)	
		
	train_seqs.append(np.asarray(imgs))

train_labels = [[0,1] for i in range(len(train_seqs))]

for fldr_name in os.listdir(no_stutter_dir): # assumes everything within dir is a dir 
	imgs = []

	for file_name in os.listdir(no_stutter_dir + fldr_name):
		img_data = image.imread(no_stutter_dir + fldr_name + '/' + file_name)
		img_data = np.reshape(img_data,(img_w,img_h,img_c))
		imgs.append(img_data)	
		
	train_seqs.append(np.asarray(imgs))
	train_labels.append([1,0])

print(train_labels)
print(np.array(train_seqs).shape)	


x_train = np.asarray(train_seqs)
y_train = np.asarray(train_labels, dtype=np.float)

print("Training model...")
model.fit(x_train, y_train, 
			batch_size=1,
			epochs=2) # put back to 30
			#validation_data=[x_test, y_test])
			