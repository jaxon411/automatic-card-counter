#This is identical to script found in root/blackjack, except these need utils.blackjack.x during imports for scope reasons
import numpy as np
from numpy import random
import utils.blackjack.blackjack as blackjack

class Player:
    
    def __init__(self,bankroll=1):
    
        self.hands = [] #list of hand
        self.bankroll = bankroll
    
    def AddHand(self,cards,bet=0):
        
        self.hands.append({'cards':cards,
                           'shown_value':blackjack.GetHandValue([cards[0]]), #for dealers only
                          'value':blackjack.GetHandValue(cards),
                          'bet':bet})
        
    def GetHands(self):
        '''
        Returns list of hands
        '''
        return self.hands
    
    def ResetHands(self):
        '''
        Deletes all hands in this object
        '''
        self.hands = []
        
    def AddCard(self,hand,card):
        hand['cards'].append(card)
        self.UpdateHandValue(hand)
    
    def UpdateHandValue(self,hand):
        '''
        Updates the hand value
        '''
        hand['value'] = blackjack.GetHandValue(hand['cards'])
        hand['shown_value'] = blackjack.GetHandValue([hand['cards'][0]])
    
    def WinLose(self,hands):
        '''
        Edits bankroll based on bets in hand dictionaries.
        The bet in hand dictionaries will be changed to positive or negative depending on if the hand wins or loses,
        so all that is needed is to add it to the bankroll.
        
        PARAMETERS:
        hands - list of hand dictionaries definined by self.AddHand()
        '''
        pass
        