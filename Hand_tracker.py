# -*- coding: utf-8 -*-
"""
Created on Mon May  9 13:31:51 2022

@author: Rakin
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import serial

from Hand_tracker_fun import hand_type, get_finger_angle, send_data
from matplotlib import pyplot as plt

#initialize variables
vid = cv2.VideoCapture(0)
hand_track = mp.solutions.hands
hands = hand_track.Hands(static_image_mode = False,
                   max_num_hands = 1,
                   model_complexity = 0,
                   min_detection_confidence = 0.5,
                   min_tracking_confidence = 0.5)

draw_hands = mp.solutions.drawing_utils
ard_serial = serial.Serial(port='COM9', baudrate=115200, timeout=.1)

#checking the dimensions of the video feed
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

#2-d array of joint coordinates.
#jt_arr = [[8,7,6], [12,11,10], [16,15,14],[20,19,18], [4,3,2]]
jt_arr = [[8,7,6], [4,3,2]]
store_arr =[]
#all index are derive from the coordiate chart of mediapipe hand
#row 1 are the joint coordinates of the index finger
#row 2 are the joint coordinates of the middle finger
#row 3 are the joint coordinates of the ring finger
#row 4 are the joint coordinates of the pinky finger
#row 5 are the joint coordinates of the thumb

#keep playing when videocapture is on
while vid.isOpened():
    success, image = vid.read()
    
    if not success:
        print("Vid is not on")
        
        break
    
    #convert color for better results (preprocessing)
    #note, do not use 555 as 3 channel rgb data is needed for input
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.flip(image,1)
    results = hands.process(image)
    
    #add hand notations
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            draw_hands.draw_landmarks(image, hand_landmarks,
                                      hand_track.HAND_CONNECTIONS)
                                      # draw_hands.get_default_hand_landmarks_style(),
                                      # draw_hands.get_default_hand_connections_style())
            #To show left or right hand
            if hand_type(i, hand_landmarks, results, height, width):
                text, coord = hand_type(i, hand_landmarks, results, height, width)
                cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255), 2, cv2.LINE_AA)
    
        store_arr=get_finger_angle(image, results, jt_arr)
    
    cv2.imshow("Hand capture", image)
    send_data(ard_serial, store_arr)
    #print(results.multi_hand_landmarks)
    store_arr.clear()
               
    if cv2.waitKey(1) & 0xFF == ord("q"): #exit if q is pressed
        break
vid.release()
cv2.destroyAllWindows()
            

