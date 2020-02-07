import tensorflow as tf
from tensorflow import keras
import numpy as np
import pdb

from matplotlib import image
from matplotlib import pyplot as plt

import os


stutter_dir = "/home/harminder/fydp/nn_spectrograms/sound_repetition/"
no_stutter_dir = "/home/harminder/fydp/nn_spectrograms/no_stutter/"

train_seqs = []
train_labels = []

for fldr_name in os.listdir(stutter_dir): # assumes everything within dir is a dir 
	imgs = []
	print(fldr_name)
	if(len(os.listdir(stutter_dir + fldr_name)) != 39): 
		print(fldr_name + " does not have right number of images")
		continue 

	for file_name in os.listdir(stutter_dir + fldr_name):
		img_data = plt.imread(stutter_dir + fldr_name + '/' + file_name)
		#print("Image Shape:")
		print(img_data.shape)
		print(np.mean(img_data))
		img_data = np.reshape(img_data,(257,345,1))
		imgs.append(img_data)	
		
	train_seqs.append(np.asarray(imgs))

train_labels = [1 for i in range(len(train_seqs))]

'''for fldr_name in os.listdir(no_stutter_dir): # assumes everything within dir is a dir 
	imgs = []

	for file_name in os.listdir(no_stutter_dir + fldr_name):
		img_data = image.imread(no_stutter_dir + fldr_name + '/' + file_name)
		img_data = np.reshape(img_data,(257,345,1))
		imgs.append(img_data)	
		
	train_seqs.append(np.asarray(imgs))
	train_labels.append(0)

print(train_labels)
print(np.array(train_seqs).shape)	'''