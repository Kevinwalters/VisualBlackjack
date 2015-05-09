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

class ContourValue():
    
    def getContourValue(self):
        # Read image
        image = cv2.imread("playing_card_3.png")
        #image = img
        
        # Apply BW and threshold
        image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, image_thresh = cv2.threshold(image_HSV,100,255,cv2.THRESH_BINARY)
        image_canny = cv2.Canny(image,100,200) 
        cv2.imwrite('Edges.png', image_canny)
        
        # Get contours
        contours =  self.getContours(image, image_thresh)
        print "hi"
    
    def getContours(self, image, image_thresh):
        cnt, _ = cv2.findContours(image_thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        contours = cnt # Contour pairs
        print " contours: %s" % cnt[1] #first contour pair
        print " contours: %s" % cnt[0][1][0] #second contour pair
       
        # Create a copy of the image
        image_copy = image.copy()
        
        #Draw the contours on the image
        cv2.drawContours(image_copy, contours, 0, 255, -1)
        cv2.imwrite('Contours.png', image_copy)
    
    def getMoments(self, contours, image):
        moment_list = []
         for i in range(0, len(contours)):
            M = cv2.moment(countours[i])
            Moments p = mu.get(i);
            int x = (int) (p.get_m10() / p.get_m00());
            int y = (int) (p.get_m01() / p.get_m00());
            
    def __init__(self):
        return None
    
    

'''
cv2.findContours(, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(white_card, [card_contour], 0, 255, -1)
cv2.imwrite('Output.png', white_card)
imggray = cv2.cvtColor(to_binary, cv2.COLOR_BGR2GRAY)
ret, b_img = cv2.threshold(imggray, 0, 255, 0)
'''