# -*- coding: utf-8 -*-
"""
Created on Sat May 28 22:36:56 2022

@author: Rakin
"""
import cv2
import mediapipe as mp
import numpy as np
import time
import serial

#initialize variables
hand_track = mp.solutions.hands
store = []

def send_data(ard, data_arr):
    store1 = ""
    for x in data_arr:
        if int(x) >130:
            store1 += "1"
        else:
            store1 += "0"

    ard.write(bytes(store1,'utf-8'))
#        ard.write(bytes(x, 'utf-8'))
#        time.sleep(0.05)
    

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
    
    for hand in results.multi_hand_landmarks:
        
        for jt in jt_arr:
            jt_1 = np.array([hand.landmark[jt[0]].x, hand.landmark[jt[0]].y]) #top joint coord
            jt_2 = np.array([hand.landmark[jt[1]].x, hand.landmark[jt[1]].y]) #middle joint coord
            jt_3 = np.array([hand.landmark[jt[2]].x, hand.landmark[jt[2]].y]) #bottom joint coord
            
            #Calculating kinematics of a hand using trigo
            #getting radians of joint angles by inversing tan
            #Converting radians to angles
            #tan(jt_3(y)-jt_2(x))^-1
            rad = np.arctan2(jt_3[1]-jt_2[1], jt_3[0]-jt_2[0]) - np.arctan2(jt_1[1]-jt_2[1], jt_1[0]-jt_2[0])
            ang = np.abs(rad*180.0/np.pi)
            ang = int(ang)
            
            #failsafe if goes beyond 180
            
            if ang > 180.0:
                ang = 360-ang
            
            #need to round off and convert value to sttring and display
            #converting the resolution to 640 x 480 
            cv2.putText(image, str(round(ang, 1)), tuple(np.multiply(jt_2, [640, 480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2,cv2.LINE_AA)
            store.append(str(ang))
    return store
    # return ang
