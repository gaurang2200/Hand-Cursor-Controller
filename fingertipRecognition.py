"""
Created on Sat May 30 00:30:47 2020
@author: Gaurang Gupta
"""

import cv2
import numpy as np
import pyautogui as pag
import time
import math

# Set it to true, to See the background mask and the image of the camera
Debug = False

# Global Variables - VideoCam, BackgroundSubtractor
cam = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2();


trigger = False
camMarginX = 10
camMarginY = 10
scale = 10
kern = np.ones((3,3), np.uint8)


# Function for Creating suitable mask for the Video Cam
def Masking(camCropped, fgbg):
    hsv = cv2.cvtColor(croppedCam, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LB, UB)
    mask = cv2.dilate(mask, kern, iterations=1)
    mask = cv2.erode(mask, kern, iterations=1)
    mask = cv2.GaussianBlur(mask, (5, 5), 100)
    mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kern)
    
    fgmask = fgbg.apply(croppedCam, learningRate = 3)
    # Background Mask
    res = cv2.bitwise_and(mask, mask, mask=fgmask)
    return mask, res

# Checking the Area of the hand
def checkArea(l, y):
    mappedY = 1

    if l==1:
        if areacnt < 600:    l = -1
        else:   
            if y < 120:
                mappedY = 2
            if y < 180:
                mappedY = 1.6
            if arearatio < (9.5 * mappedY):
                l = 0
            else:   l = 1
    if(Debug):
        print(y, int(arearatio), mappedY, l)
    return l

# Finding the contours and getting 0 or 1 finger 
def FindContours(contours, binary) :
    maxIndex = 0
    maxArea = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area > maxArea:
            maxArea = area
            maxIndex = i
    return contours[maxIndex]

# According to the topmost bright pixel in the video camera the mouse cursor is moved there
# So try to have a Stable and clear background, for seeing your background assign the Debug variable to true
def mouseMovement(fingers, cnt):
    global trigger
    if(Debug):
        # The mouse cursor will move to which pixel on the screen
        print(int(cnt[0][0][0]*mouseMovementXFactor), int(cnt[0][0][1]), fingers)
    if fingers == 5:
        trigger = not(trigger)
        print("Program Started:", trigger)
        time.sleep(0.8)
    if trigger:
        if fingers == 0:    
            try:
                pag.click()
                time.sleep(0.2)
            except pag.FailSafeException :
                pass
        elif fingers == 1:
            try:
                pag.moveTo((cnt[0][0][0]*mouseMovementXFactor), 
                           (cnt[0][0][1]*mouseMovementYFactor))
            except pag.FailSafeException :
                pass
#        Assign fingers 2 According to you
#        elif fingers == 2:
#            pag.rightClick();
        elif fingers == 3:
            pag.scroll(-100)
        elif fingers == 4:
            pag.scroll(100)

# To Find no. of defects due to fingers
def NumberOfFingers(defects, l):
    try:
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            
            # Find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            
            d=(2*ar)/a
            
            # Cosine Rule for angle
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57            
        
            # Ignoring angles > 90 and ignore points very close to convex hull
            if angle <= 70 and d > 30:
                l += 1
                cv2.circle(frame, far, 3, [255,0,0], -1)
    except AttributeError:
        pass
    return l    
    

if cam.isOpened():  # Try to get the first frame
    rval, frame = cam.read()
else:
    rval = False

try:
    while rval:
        rval, img = cam.read()
        img = cv2.flip(img, 1)
        croppedCam = img
        
        LB = np.array([0, 90, 0])
        UB = np.array([180, 220, 255])
        
        roi = (400, 120, 300, 340)
        x, y, w, h = roi
        
        mouseMovementXFactor = 1*1980/w
        mouseMovementYFactor = 1.5*1080/h
        areacnt = 0
        arearatio = 0
    
        try:
            lowY = y-(5*camMarginY)
            lowX = x-(5*camMarginX)
            cropped = croppedCam[lowY:y+h, lowX:x+w]
            croppedCam = cv2.resize(cropped, (h+scale, w+scale), interpolation=cv2.INTER_AREA)
        except cv2.error or NameError:
            pass
        
        mask, res = Masking(croppedCam, fgbg)        
        # Find contours 
        contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        
        # To find contour of max area(hand)
        try:
            cnt = FindContours(contours, mask)
            # Approx the contour a little
            epsilon = 0.0005*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
                
            # Make convex hull around hand
            hull = cv2.convexHull(cnt)
            
            # Define area of hull and area of hand
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)
            
            # Find the defects in convex hull with respect to hand
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)
          
            try:
                #find the percentage of area not covered by hand in convex hull
                arearatio=((areahull-areacnt)/areacnt)*100
            except ZeroDivisionError:
                pass
            # l = no. of defects(To know the number of Fingers)
            l = 0
            l = NumberOfFingers(defects, l)
            
        except IndexError :
            pass
            
        l += 1
        l = checkArea(l, cnt[0][0][1])
        mouseMovement(l, cnt)
        
        # This shows you the background mask and real camera image when debug is True
        if(Debug):
            cv2.imshow('Mask', mask)
            cv2.imshow('Original', img) 
        
        if cv2.waitKey(20) == 27:
            break
except KeyboardInterrupt:
    pass

cam.release()
cv2.destroyAllWindows();
