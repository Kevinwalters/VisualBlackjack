'''
Created on May 4, 2015

@author: Kevin Walters
'''

from Cards import Cards
#from GetThreshold import CARD_VALUE

STAND = 0
HIT = 1
OVER = 2
WIN = 3
LOSE = 4
PUSH = 5
RESULTS = ["STAND", "HIT", "Player loses - hand over 21", "Player wins!", "Player loses - dealer had higher hand", "It's a push! No winner"]

class BlackjackLogic(object):
    
    def getResult(self):
        if len(self.dealer_card) != 2:
            print "Dealer must have 2 cards before game ends!"
            return
        # Compute highest dealer sum without exceeding 21
        dealer_sum = 0
        for card in self.dealer_card:
            if card == Cards.ACE:
                if dealer_sum + 11 <= 21:
                    dealer_sum += 11
                else:
                    dealer_sum += 1
            else:
                dealer_sum += Cards.CARD_VALUES[card]
        
        if dealer_sum > 21:
            return WIN
        player_sum = self.card_sum
        for _ in range(self.num_ace):
            if player_sum + 11 + self.num_ace - 1 <= 21:
                player_sum += 11
                self.num_ace -= 1
            else:
                player_sum += 1
                self.num_ace -= 1
        if player_sum > 21:
            return OVER
        if player_sum < dealer_sum:
            return LOSE
        if player_sum == dealer_sum:
            return PUSH
        return WIN
    
    def getDecision(self):
        if self.card_sum + self.num_ace > 21:
            return OVER
        if self.card_sum + self.num_ace == 21:
            return WIN
        if self.card_sum > 16:
            return STAND
        if self.card_sum < 12 and self.num_ace == 0:
            return HIT
        if self.card_sum < 17 and self.num_ace == 0:
            if self.dealer_card in [Cards.TWO, Cards.THREE, Cards.FOUR, Cards.FIVE, Cards.SIX]:
                return STAND
            else:
                return HIT
        if self.num_ace == 1:
            if self.card_sum + 11 == 21:
                return WIN
            if self.card_sum < 7:
                return HIT
            if self.card_sum == 7 and self.dealer_card in [Cards.NINE, Cards.TEN, Cards.JACK, Cards.QUEEN, Cards.KING]:
                return HIT
            if self.card_sum > 7 and self.card_sum < 11:
                return STAND
            self.card_sum = self.card_sum + 1
            self.num_ace = 0
            return self.getDecision()
        # More than once Ace, need to first check if in a good position
        # If not, simulate a one-ace scenario recursively
        if self.num_ace > 1:
            tmp_sum = self.card_sum + 11 + self.num_ace - 1
            if tmp_sum == 21:
                return WIN
            if tmp_sum > 16 and tmp_sum <= 21:
                return STAND
            tmp_sum = self.card_sum + self.num_ace
            if tmp_sum == 21:
                return WIN
            if tmp_sum > 16 and tmp_sum <= 21:
                return STAND
            tmp_sum = self.card_sum + self.num_ace - 1
            if tmp_sum <= 21:
                self.num_ace = 1
                self.card_sum = tmp_sum
                return self.getDecision()
            else:
                return OVER

    # Not implemented in final version   
    def getCustomDecision(self):
        if self.card_sum + self.num_ace > 21:
            return STAND
        if self.card_sum > 14:
            return STAND
        if self.card_sum < 10 and self.num_ace == 0:
            return HIT
        if self.card_sum < 15 and self.num_ace == 0:
            if self.dealer_card in [Cards.TWO, Cards.THREE, Cards.FOUR, Cards.FIVE, Cards.SIX]:
                return STAND
            else:
                return HIT
        if self.num_ace == 1:
            if self.card_sum < 5:
                return HIT
            if self.card_sum == 5 and self.dealer_card in [Cards.NINE, Cards.TEN, Cards.JACK, Cards.QUEEN, Cards.KING]:
                return HIT
            if self.card_sum > 5:
                return STAND
        # More than once Ace, need to first check if in a good position
        # If not, simulate a one-ace scenario recursively
        if self.num_ace > 1:
            tmp_sum = self.card_sum + 11 + self.num_ace - 1
            if tmp_sum > 14 and tmp_sum <= 21:
                return STAND
            tmp_sum = self.card_sum + self.num_ace
            if tmp_sum > 14 and tmp_sum <= 21:
                return STAND
            tmp_sum = self.card_sum + self.num_ace - 1
            if tmp_sum <= 21:
                self.num_ace = 1
                self.card_sum = tmp_sum
                return self.getDecision()
            else:
                return OVER
            

    def __init__(self, cards, dealer_card, suits=None, custom=False):
        self.card_sum = 0
        self.num_ace = 0
        self.dealer_card = dealer_card
        for i in range(len(cards)):
            card = cards[i]
            if card == Cards.ACE:
                self.num_ace += 1
            else:
                if not custom:
                    self.card_sum += Cards.CARD_VALUES[card]
                else:
                    self.card_sum += Cards.CARD_VALUES + suits[i]