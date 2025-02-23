####################################################################
# Copyright (C) 2024-2025 Nand Compute LLC | All Rights Reserved 
#
####################################################################

import cv2
import numpy as np

# BGR Colors
BLUE   = (255, 0, 0)
RED    = (0, 0, 255)
GREEN  = (0, 255, 0)
PURPLE = (255, 0, 255)
YELLOW = (0, 255, 255)

LANDMARK_COLOR = [ 
        BLUE,    # left eye
        RED,     # right eye
        GREEN,   # nose tip
        PURPLE,  # left mouth corner
        YELLOW ] # right mouth corner

def result_to_bbox(result):
    '''Extract bounding box from YuNet result.'''
    if result is None:
        return None
    (x,y,w,h) = result[0:4].astype(np.int32)
    return (x,y,w,h)

def result_to_landmarks(results):
    '''Extrace landmark points from YuNet result(s).'''
    if type(results) == np.ndarray:
        landmarks = results[4:14].reshape((5,2)).astype(np.int32)
        return landmarks
    elif type(results) == list:
        landmarks = []
        for result in (results if results is not None else []):
            landmark = result[4:14].reshape((5,2)).astype(np.int32)
            landmarks.append( landmark )
        return landmarks

def result_to_confidence(result):
    '''Extract confidence value from YuNet result.'''
    return result[-1]

def visualize(img, results, box_color=GREEN, text_color=RED):
    output = img.copy()

    # Iterate over each result and add bounding box, confidence level, and landmark points
    for result in (results if results is not None else []):
        (x,y,w,h) = result_to_bbox(result)
        cv2.rectangle(output, (x,y), (x+w,y+h), box_color, 2)

        confidence = result_to_confidence(result)
        cv2.putText(output, '{:.4f}'.format(confidence), (x,y+12), cv2.FONT_HERSHEY_DUPLEX, 0.5, text_color)

        landmarks = result_to_landmarks(result)
        for idx, landmark in enumerate(landmarks):
             cv2.circle(output, landmark, 2, LANDMARK_COLOR[idx], 2)
    
    return output
