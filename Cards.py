'''
Created on Apr 28, 2015

@author: Kevin Walters
'''

class Cards():
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR= 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    
    HEARTS = 0
    SPADES = 1
    CLUBS = 2
    DIAMONDS = 3
    
    CARDS = ["Unknown", "Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
    SUITS = ["Hearts", "Spades", "Clubs", "Diamondss"]
    
    CARD_VALUES = [None, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def __init__(self, params):
        pass