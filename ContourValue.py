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
    
    '''
    Given the original image and a contour of a card, get its rank
    '''
    def getContourValue(self, img, cnt, b_thresh):
        # Black out everything except the card we're dealing with
        mask = np.zeros_like(img)
        cv2.drawContours(mask, [cnt], 0, (255, 255, 255), -1)
        card_img = np.zeros_like(img)
        card_img[mask == (255, 255, 255)] = img[mask == (255, 255, 255)]

        red_boundary = ([170, 0, 0], [255, 255, 255])
        lower_boundary = np.array(red_boundary[0], dtype="uint8")
        upper_boundary = np.array(red_boundary[1], dtype="uint8")
        # Apply a mask to the image, using the boundaries
        mask = cv2.inRange(card_img, lower_boundary, upper_boundary)
        no_red = cv2.bitwise_and(card_img, card_img, mask = mask)
        
        # Binarize the image
        imggray = cv2.cvtColor(no_red, cv2.COLOR_BGR2GRAY)
        
        ret, card_img = cv2.threshold(imggray, b_thresh, 255, 0)
        
        cnt, hier = cv2.findContours(card_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnt) > 30:
            return len(cnt)
        cnt_count = 0
        for element in hier[0]:
            if element[3] == 0:
                cnt_count += 1
                
        if cnt_count == 16:
            return 10
        else:
            return cnt_count - 4
        
    def __init__(self):
        return None