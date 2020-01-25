import tensorflow as tf
from tensorflow import keras
import numpy as np

from matplotlib import image
from matplotlib import pyplot as plt

import os


stutter_dir = "/home/harminder/fydp/train_imgs/stutterA/"
no_stutter_dir = "/home/harminder/fydp/train_imgs/noStutter/"

train_seqs = []
train_labels = []

for fldr_name in os.listdir(stutter_dir): # assumes everything within dir is a dir 
	imgs = []

	for file_name in os.listdir(stutter_dir + fldr_name):
		img_data = plt.imread(stutter_dir + fldr_name + '/' + file_name)
		img_data = np.reshape(img_data,(300,300,1))
		print(img_data.shape)
		imgs.append(img_data)	
		
	train_seqs.append(np.asarray(imgs))

train_labels = [1 for i in range(len(train_seqs))]

for fldr_name in os.listdir(no_stutter_dir): # assumes everything within dir is a dir 
	imgs = []

	for file_name in os.listdir(no_stutter_dir + fldr_name):
		img_data = image.imread(no_stutter_dir + fldr_name + '/' + file_name)
		img_data = np.reshape(img_data,(300,300,1))
		imgs.append(img_data)	
		
	train_seqs.append(np.asarray(imgs))
	train_labels.append(0)

print(train_labels)
print(np.array(train_seqs).shape)	