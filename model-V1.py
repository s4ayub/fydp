import tensorflow as tf
from tensorflow import keras

# Input spectogram size: 
# TODO: parse data (?)

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
    x = residual_block(x, 32, 64)				# why is input channels 32 here?

    x = residual_block(x, 64, 128)

    x = residual_block(x, 128, 128)

    x = residual_block(x, 128, 64)

    x = residual_block(x, 64, 32)

    x = residual_block(x, 32, 16)

    x = keras.layers.TimeDistributed(keras.layers.Flatten())(x)		# Flatten so that dense can take in 
    x = keras.layers.TimeDistributed(keras.layers.Dense(100))(x)	# Output (?) what does it look like, why 100?

    return x

def lstm_network(x):
	# Might needs to set return_sequences=false, return_state=false 
    x = keras.layers.Bidirectional(keras.layers.LSTM(512, return_sequences=True))(x)
    # (?) Missing: "Dropout rates of 0.2 and 0.4 are utilized after each recurrent layer"
    x = keras.layers.Bidirectional(keras.layers.LSTM(512))(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(2)(x)
    return x


image_tensor = keras.Input(shape=(5, 256, 256, 1))
residual = residual_network(image_tensor)
lstm = lstm_network(residual)
  
model = keras.Model(inputs=[image_tensor], outputs=[lstm])
print(model.summary())