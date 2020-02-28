import os
import numpy as np
from PIL import Image
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--inputPath", "-i", help="input/path/", required=True)
parser.add_argument("--outputPath", "-o", help="output/path/", required=True)

args = parser.parse_args()

# Things i need to change:
# how to start vm: source ~/ven/bin/activate
# Input and output directory, must create output directory

#input_dir = "/home/justin/Downloads/4s_200ms_100ms_172x128/nn_spectrograms/no_stutter/"
#output_dir = "/home/justin/github/fydp/data/no_stutter/"

input_dir = args.inputPath
output_dir = args.outputPath
num_images = 39

for fldr_name in os.listdir(input_dir):
    imgs = []
    if(len(os.listdir(input_dir + fldr_name)) != num_images):
            print(fldr_name + " does not have right number of images")
            continue

    for file_name in os.listdir(input_dir + fldr_name):
        img_data = Image.open(input_dir + fldr_name + '/' + file_name)
        imgs.append(np.array(img_data))

    arr = np.array(imgs)
    shape = arr.shape
    arr = np.reshape(arr, (shape[0]*shape[1], shape[2]))
    img = Image.fromarray(arr)
    img.save(output_dir + fldr_name + ".png")
