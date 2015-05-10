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
EXTRA_CNT = 4

class ContourValue():
    
    '''
    Given the original image and a contour of a card, get its rank
    '''
    def getContourValue(self, img, cnt):
        # Threshold the image to BW
        # A boundary for any non-green pixel
        green_boundary = ([0, 210, 0], [255, 255, 255])
        lower_boundary = np.array(green_boundary[0], dtype="uint8")
        upper_boundary = np.array(green_boundary[1], dtype="uint8")
        # Apply a mask to the image, using the boundaries
        mask = cv2.inRange(img, lower_boundary, upper_boundary)
        img = cv2.bitwise_and(img, img, mask = mask)
        #cv2.imwrite("Output.png", img)
        #cv2.imshow("out", img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, card_img = cv2.threshold(imggray, 0, 255, 0)
        
        # Get an image of only this card from this
        mask = np.zeros_like(card_img) # Create mask where white is what we want, black otherwise
        cv2.drawContours(mask, [cnt], 0, 255, -1) # Draw filled contour in mask
        img = np.zeros_like(card_img) # Extract out the object and place into output image
        img[mask == 255] = card_img[mask == 255]
        
        kernel = np.ones((2,2), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        
        
        cv2.imwrite("Output.png", img)
        cv2.imshow("out", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Apply BW and threshold
        #image_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #ret, image_thresh = cv2.threshold(image_HSV,100,255,cv2.THRESH_BINARY)
        #image_canny = cv2.Canny(img,100,200) 
        #cv2.imwrite('Edges.png', image_canny)
        
        # Get contours
        contours = self.getContours(img)
        
        print "Number:", len(contours)
        
        if len(contours) == 16:
            return Cards.TEN
        else:
            return len(contours) - EXTRA_CNT
                
        # Get the moments
        moment_list = self.getMoments(contours)
        
        # Reduce the moments
        moment_count = self.getReducedMoments(moment_list)
        
        # Get the final card number value
        card_number = self.getCardNumber(moment_count)
        print "card_number %d" %card_number
        return card_number
    
    def getContours(self, img):
        cnt, hier = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print len(cnt)
        cnts = []
        #print cnt
        for i in range(len(hier[0])):
            #print hier[0][i]
            print hier[0][i][3]
            if hier[0][i][3] == 0:
                cnts.append(cnt[i])
        return cnts
    
    def getMoments(self, contours):
        moment_list = []
        for i in range(0, len(contours)):
            M = cv2.moments(contours[i])
            moment_list.append(M) #add the moment to the list
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #print("x: %d and y: %d" % (cx, cy))
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
    
    
