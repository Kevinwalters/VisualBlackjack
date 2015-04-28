'''
Created on Apr 27, 2015

@author: Kevin Walters
'''


from TemplateMatcher import TemplateMatcher
from Cards import Cards
import numpy as np
import cv2

CORNER_LEFT = 10
CORNER_RIGHT = 70
CORNER_TOP = 30
CORNER_BOTTOM = 115


'''
Given a card's contour, determines its rank
Order of steps:
    1. Get the four coordinates of the card in a known order
    2. Perform a perspective transform, to get a top-down view of the card
    3. Warp the perspective to 500x700 (cards are 5"x7")
    4. Get the rank from the top-left corner of the card (to speed up template matching)
    5. Use the template matcher on the corner to determine the rank
'''
def getRank(img, card_contour):
    # Get coordinates of the card in a known order
    rect = cv2.minAreaRect(card_contour[0])
    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box) # Box coordinates: [LR, LL, UL, UR]
    
    # Points to be mapped for perspective transformation
    src_points = np.float32([box[0], box[1], box[2], box[3]])
    target_points = np.float32([[499, 699],[0, 699], [0, 0], [499, 0]])
    
    # Transform the image into a 500x700 top-down view
    M = cv2.getPerspectiveTransform(src_points, target_points)
    output = cv2.warpPerspective(img, M, (500, 700))

    # Perform template matching on the corner of the card
    card_corner = output[CORNER_TOP:CORNER_BOTTOM, CORNER_LEFT:CORNER_RIGHT]
    tm = TemplateMatcher()
    card_val = tm.matchTemplate(card_corner)
    print Cards.CARDS[card_val]

if __name__ == '__main__':
    
    img = cv2.imread("king-spades.png")

    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, b_img = cv2.threshold(imggray, 127, 255, 0)
    img2 = b_img.copy()
    cnt, hier = cv2.findContours(b_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    getRank(img2, cnt)