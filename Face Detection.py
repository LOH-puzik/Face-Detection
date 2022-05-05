# -*- coding: utf-8 -*-
"""
Created on Fri March 26 15:37:10 2022

@author: Dhia
"""

import cv2

def ask_for_tracker():
    print("Enter 0 for BOOSTING: ")
    print("Enter 1 for MIL: ")
    print("Enter 2 for KCF: ")
    print("Enter 3 for TLD: ")
    print("Enter 4 for MEDIANFLOW: ")
    choice = input("Please select your tracker: ")
    
    if choice == '0':
        tracker = cv2.TrackerBoosting_create()
    if choice == '1':
        tracker = cv2.legacy.TrackerMIL_create()
    if choice == '2':
        tracker = cv2.legacy.TrackerKCF_create()
    if choice == '3':
        tracker = cv2.legacy.TrackerTLD_create()    
    if choice == '4':
        tracker = cv2.legacy.TrackerMedianFlow_create()   
        
    return tracker

tracker = ask_for_tracker()
tracker_name = str(tracker).split()[0][1:]

#Read video
cap = cv2.VideoCapture(0)

#Read first frame
ret, frame = cap.read()

#Special function to draw on the very first frame of the desired ROI
roi = cv2.selectROI(frame, False)

#Init tracker with first frame and bounding box
ret = tracker.init(frame, roi)

while True:
    #Read a new frame
    ret, frame = cap.read()
    
    #Update tracker
    success, roi = tracker.update(frame)
    
    #Roi variable is a tuple of 4 floats
    #Each value has to be as integers
    (x,y,w,h) = tuple(map(int,roi))
    
    #Draw rectangle as tracker moves
    if success:
        #Tracking success
        p1 = (x,y)
        p2 = (x+w, y+h)
        cv2.rectangle(frame, p1, p2, (0,255,0), 2)
    else:
        #Tracking failure
        cv2.putText(frame, "Failure to detect tracking!",
                    (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
        
    #Display tracker type on frame
    cv2.putText(frame, tracker_name, (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2);
    
    #Display result
    cv2.imshow(tracker_name, frame)
    
    #Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 :
        break
        
cap.release()
cv2.destroyALLWindows()