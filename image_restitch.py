import os
import numpy as np
from PIL import Image

# Things i need to change:
# how to start vm: source ~/ven/bin/activate
# Input and output directory, must create output directory
# num_omages, 2sec 19, 4sec 39

input_dir = "/home/justin/Downloads/4s_200ms_100ms_172x128/nn_spectrograms/no_stutter/"
output_dir = "/home/justin/github/fydp/data/no_stutter/"
num_images = 39

train_seqs = []
train_labels = []

for fldr_name in os.listdir(input_dir):
    imgs = []
    if(len(os.listdir(input_dir + fldr_name)) != num_images):
            print(fldr_name + " does not have right number of images")
            continue

    for file_name in os.listdir(input_dir + fldr_name):
        img_data = Image.open(input_dir + fldr_name + '/' + file_name)
        #img_data = img_data.resize((172,128), Image.BILINEAR)
        imgs.append(np.array(img_data))

    arr = np.array(imgs)
    shape = arr.shape
    arr = np.reshape(arr, (shape[0]*shape[1], shape[2]))
    img = Image.fromarray(arr)
    img.save(output_dir + fldr_name + ".png")
