# -*- coding: utf-8 -*-
"""
Created on Mon May  9 13:31:51 2022

@author: Rakin
"""

import cv2
import mediapipe as mp
import numpy as np
import time

vid = cv2.VideoCapture(0)

hand_track = mp.solutions.hands

hands = hand_track.Hands(static_image_mode = False,
                   max_num_hands = 1,
                   model_complexity = 1,
                   min_detection_confidence = 0.5,
                   min_tracking_confidence = 0.5)

draw_hands = mp.solutions.drawing_utils
#keep playing when videocapture is on
while vid.isOpened():
    success, image = vid.read()
    
    if not success:
        print("Vid is not on")
        
        break
    
    #convert color for better results (preprocessing)
    #note, do not use 555 as 3 channel rgb data is needed for input
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    results = hands.process(image)
    
    #add hand notations
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_hands.draw_landmarks(image, hand_landmarks,
                                      hand_track.HAND_CONNECTIONS)
                                      # draw_hands.get_default_hand_landmarks_style(),
                                      # draw_hands.get_default_hand_connections_style())
    cv2.imshow("Hand capture", image)
    print(results.multi_hand_landmarks)
               
    if cv2.waitKey(1) & 0xFF == ord("q"): #exit if q is pressed
        break
vid.release()
cv2.destroyAllWindows()
            

