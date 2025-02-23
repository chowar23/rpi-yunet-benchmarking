####################################################################
# Copyright (C) 2024-2025 Nand Compute LLC | All Rights Reserved 
#
####################################################################

import cv2
import numpy as np
import os
import pandas as pd
from timeit import default_timer as timer

import data
import utils

####################################################
# Constants
####################################################
model_path = '../models/face_detection_yunet_2023mar.onnx'
img_path   = '../images/NH 96919-KN.jpeg' 
csv_path   = '../data/rpi_yunet_data.csv'

img_w = 480//2
img_h = 640//2

n_iters_warmup = 24  # number of inferences at beginning to ignore
n_iters_test   = 512 # number of inferences to average

####################################################
# Save configuration
####################################################
# Get Pi configuration
config = utils.get_pi_config()

# Add model configuration
config['input_width'] = img_w
config['input_height'] = img_h
config['model'] = os.path.basename(model_path)

####################################################
# Set up detector and load / resize image
####################################################
detector = cv2.FaceDetectorYN.create(model_path, '', (img_w,img_h))

img = cv2.imread(img_path)
img = cv2.resize(img, (img_w,img_h))

####################################################
# Run detector N times and time it
####################################################
total_iters = n_iters_warmup + n_iters_test
inf_times = np.zeros(total_iters)

for i in range(total_iters):
  start = timer()
  ret,results = detector.detect(img)
  inf_times[i] = timer() - start

####################################################
# Find average inference time
####################################################
inf_ms = 1.0e3 * np.mean(inf_times[n_iters_warmup:])
print(f'Average inference time: {inf_ms:.2f} ms')

####################################################
# Save data
####################################################
df = data.read_csv(csv_path)
df = data.add(df.copy(), config, inf_ms)
data.save_to_csv(csv_path, df)

