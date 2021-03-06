import scipy.misc
import random
import PIL
from PIL import Image
import numpy as np
import cv2
xs = []
ys = []

#points to the end of the last batch
train_batch_pointer = 0
val_batch_pointer = 0

#read data.txt
with open("driving_dataset/data.txt") as f:
    for line in f:
        # Saving the location of each image in xs
        xs.append("driving_dataset/" + line.split()[0])
        #the paper by Nvidia uses the inverse of the turning radius,
        #but steering wheel angle is proportional to the inverse of turning radius
        #so the steering wheel angle in radians is used as the output
        
        # Converting steering angle which we need to predict from radians
        # to degrees for fast computation 
        ys.append(float(line.split()[1]) * scipy.pi / 180)

#get number of images
num_images = len(xs)

# To change the train and test ratio do it here
# Here Train -> 80% and Test -> 20%
train_xs = xs[:int(len(xs) * 0.8)]
train_ys = ys[:int(len(xs) * 0.8)]

val_xs = xs[-int(len(xs) * 0.2):]
val_ys = ys[-int(len(xs) * 0.2):]

num_train_images = len(train_xs)
num_val_images = len(val_xs)

def LoadTrainBatch(batch_size):
    # Train batch pointer allows we use subsequent ahead images for train 
    # Rather than using random images from train data as we train the model 
    # on batches of data rather thatn whole data at each epoch
    global train_batch_pointer
    x_out = []
    y_out = []
    for i in range(0, batch_size):
        #Resizing and Converting image in ideal form to train
        full_scale = cv2.imread(train_xs[(train_batch_pointer + i) % num_train_images])[-150:]
        x_out.append(np.array(Image.fromarray(full_scale).resize(
(200,66),
resample=PIL.Image.BICUBIC)
) / 255.0)
        y_out.append([train_ys[(train_batch_pointer + i) % num_train_images]])
    train_batch_pointer += batch_size
    return x_out, y_out

def LoadValBatch(batch_size):
    global val_batch_pointer
    x_out = []
    y_out = []
    for i in range(0, batch_size):
        full_scale = cv2.imread(val_xs[(val_batch_pointer + i) % num_val_images])[-150:]
        x_out.append(np.array(Image.fromarray(full_scale).resize(
(200,66),
resample=PIL.Image.BICUBIC)
) / 255.0)
       # x_out.append(cv2.imresize(cv2.imread(val_xs[(val_batch_pointer + i) % num_val_images])[-150:], [66, 200]) / 255.0)
        y_out.append([val_ys[(val_batch_pointer + i) % num_val_images]])
    val_batch_pointer += batch_size
    return x_out, y_out
