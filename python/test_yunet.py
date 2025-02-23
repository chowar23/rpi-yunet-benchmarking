####################################################################
# Copyright (C) 2024-2025 Nand Compute LLC | All Rights Reserved 
#
####################################################################

import cv2
from timeit import default_timer as timer

import yunet

# Constants
model_path = '../models/face_detection_yunet_2023mar.onnx'
img_path   = '../images/NH 96919-KN.jpeg' 

img_w = 480//4
img_h = 640//4

# Set up detector
detector = cv2.FaceDetectorYN.create(model_path, '', (img_w,img_h))

# Load image and resize
img = cv2.imread(img_path)
img = cv2.resize(img, (img_w,img_h))

# Run detector (and time it)
start = timer()
ret,results = detector.detect(img)
stop = timer()

inf_time_ms = 1e3*(stop - start)
print(f'Input size: {img_w}x{img_h}x3')
print(f'Inference time: {inf_time_ms:.2f} ms')

# Visualize result
img_result = yunet.visualize(img, results)

cv2.namedWindow('YuNet Result', cv2.WINDOW_NORMAL)
cv2.imshow('YuNet Result', img_result)
cv2.waitKey(0)

cv2.destroyAllWindows()

