# -*- coding: utf-8 -*-
"""
Created on Sat May 28 22:36:56 2022

@author: Rakin
"""
import cv2
import mediapipe as mp
import numpy as np
import time

#initialize variables
hand_track = mp.solutions.hands
jt_arr = [[8,7,6],[12,11,10]]

def hand_type(index, hands, results, ht, wd): #index = hand results(1,0) or left/right, hands = hand landmark, results = all detections
    
    output = None #Define null value output first
    for i, classification in enumerate(results.multi_handedness): #looping through all multi_handedness
        if classification.classification[0].index == index: #check whether correct index
            
            #grabbing the results from hand detected in the array
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score,2))
        
            #grabbing the coordinates of landmark
            coords = tuple(np.multiply(
                np.array((hands.landmark[hand_track.HandLandmark.WRIST].x, hands.landmark[hand_track.HandLandmark.WRIST].y)), #storing x and y values of the wrist landmark in an array
            [wd, ht]).astype(int)) #multiplying the array with the video resolution to translate to the current video resolution
    
            output = text, coords #result variable   
    return output

def get_finger_angle(image, results, jt_arr):
    
    for hand in results.multi_hand_landmarks:  #going through all hands
        for jt in jt_arr: #going through all the joints in the joint array
            jt_1 = np.array([hand.landmark[jt[0]].x, hand.landmark[jt[0]].y]) #top joint coord
            jt_2 = np.array([hand.landmark[jt[1]].x, hand.landmark[jt[1]].y]) #middle joint coord
            jt_3 = np.array([hand.landmark[jt[2]].x, hand.landmark[jt[2]].y]) #bottom joint coord