'''
Created on May 7, 2015

@author: sabinasmajlaj
'''

import math
from operator import itemgetter

import cv2

from Cards import Cards
from TemplateMatcher import TemplateMatcher
import numpy as np
from BlackjackLogic import BlackjackLogic
from BlackjackLogic import RESULTS
from twisted.python.reflect import isSame

class ContourValue():
    
    def getContourValue(self):
        # Read image
        image = cv2.imread("playing_card_5.png")
        #image = img
        
        # Apply BW and threshold
        image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, image_thresh = cv2.threshold(image_HSV,100,255,cv2.THRESH_BINARY)
        image_canny = cv2.Canny(image,100,200) 
        cv2.imwrite('Edges.png', image_canny)
        
        # Get contours
        contours =  self.getContours(image, image_thresh)
        
        # Get the moments
        moment_list = self.getMoments(contours, image)
        
        # Reduce the moments
        moment_count = self.getReducedMoments(moment_list)
        
        # Get the final card number value
        card_number = self.getCardNumber(moment_count)
        print "card_number %d" %card_number
        return card_number
    
    def getContours(self, image, image_thresh):
        cnt, _ = cv2.findContours(image_thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        contours = cnt # Contour pairs
        #print " contours: %s" % cnt[1] #first contour pair
        #print " contours: %s" % cnt[0][1][0] #second contour pair
       
        # Create a copy of the image
        image_copy = image.copy()
        
        #Draw the contours on the image
        cv2.drawContours(image_copy, contours, 0, 255, -1)
        cv2.imwrite('Contours.png', image_copy)
        return contours
    
    def getMoments(self, contours, image):
        moment_list = []
        for i in range(0, len(contours)):
            M = cv2.moments(contours[i])
            moment_list.append(M) #add the moment to the list
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print("x: %d and y: %d" % (cx, cy))
        return moment_list
    
    def getReducedMoments(self, moment_list):
        moment_count = len(moment_list)
        max_x = 0
        max_y = 0
        numFound = 0
        maxSame = 0
         
        for i in range(0, moment_count):
            numFound = 0
            M = moment_list[i]
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if(cx>max_x):
                max_x = cx
            if(cy>max_y):
                max_y = cy
            for j in range(0, moment_count):
                M2 = moment_list[j]
                dx = int(M2['m10']/M2['m00'])
                dy = int(M2['m01']/M2['m00'])
                if(i != j):
                    if(self.isSameX(cx, dx) and self.isSameY(cy, dy, max_y)):
                        numFound +=1
                        if(numFound > maxSame):
                            maxSame = numFound
            
        # Check for extra contours
        extra_moments = (maxSame -1) *2
        if(extra_moments != 1):
            moment_count = moment_count - extra_moments
        return moment_count
             
         
    def  isSameX(self, x1, x2):
        isSame = False
        pixelDiff = 6
        if(x1>=(x2-pixelDiff) and x1<=(x2+pixelDiff)):
            isSame = True
        if(x2>=(x1-pixelDiff) and x2<=(x1+pixelDiff)):
            isSame = True 
        return isSame
    
    def  isSameY(self, y1, y2, max_y):
        isSame = False
        maxDiff = max_y * 0.12; #diff of 12%
        if(y1>=(y2-maxDiff) and y1<=(y2+maxDiff)):
            isSame = True
        if(y2>=(y1-maxDiff) and y2<=(y1+maxDiff)):
            isSame = True 
        return isSame
      
    def getCardNumber(self, actual_moments):     
        extra_contours = 5
        card_number = actual_moments - extra_contours
        return card_number
        
    def __init__(self):
        return None
    
    
