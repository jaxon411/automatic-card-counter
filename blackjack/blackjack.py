import numpy as np
from numpy import random
import shoe

#Dictionary of Blackjack Cards
cards = {'two':2,
        'three':3,
        'four':4,
        'five':5,
        'six':6,
        'seven':7,
        'eight':8,
        'nine':9,
        'ten':10,
        'jack':10,
        'queen':10,
        'king':10,
        'ace':[11,1]}

def CreateDeck():
    #RETURNS: deck - list of str of cards making a standard 52 card deck
    deck = list(cards.keys())*4
    
    #shoe.CreateShoe() will already shuffle before placing in shoe
#     random.shuffle(deck) #inplace shuffle
    
    return deck

def GetHandValue(hand):
    '''
    Gets the value of a single blackjack hand
    
    PARAMETERS:
    hand - list of cards as str corresponding with cards dictionary
    
    RETURNS:
    hand_value - int in hand value (highest possible hand value if aces are present)
    '''
    
    
    hand_value = 0
    num_aces = hand.count('ace') #gets number of aces
    aces_value = num_aces #assumes all aces are 1's for initial calculation
    
    hand.sort(reverse=True) #sorts all aces to back of array
    for card in hand[:len(hand)-num_aces]: #iterates through list without aces
        hand_value += cards[card] #calculates hand value pre-aces
    
    for i in range(num_aces+1): #iterates +1 in case there is only 1 ace
        if hand_value + ((i*11) + (num_aces-i)) <= 21: #checks combinations of 11s and 1s
            aces_value = (i*11) + (num_aces-i) #sets combination of 11s and 1s if not a bust
        else: #breaks out of loop once the maximum 11s:1s ratio is found
            break
        
    hand_value += aces_value
    
    if hand_value > 21:
        return -1 #-1 is read as a bust when returned
    else:
        return hand_value
    
    