import numpy as np
from numpy import random

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
    random.shuffle(deck) #inplace shuffle
    
    return deck

def CreateShoe(deck,shoe_size = 6):
    '''
    PARAMETERS:
    shoe_size - int of number of decks in shoe

    RETURNS:
    tuple - list of [shoe_size * deck] cards minus random penetration
            and
            list of cards equal to penetration (reserve cards for dealing last hand)
    '''

    if shoe_size > 2:
        pen_range = [(52/(52*shoe_size)), ((52*1.5)/(52*shoe_size))]
    else:
        #single and double deck penetrate from 10 to 15 cards
        pen_range = [10/(52*shoe_size), 15/(52*shoe_size)]

    #ensures that each deck added to the shoe is shuffled
    #this might just be gamblers superstition on my part...
    shoe = []
    for _ in range(shoe_size):
        random.shuffle(deck)
        shoe += deck
        
    random.shuffle(shoe) #in-place shuffle
    
    #generates penetration at a random specific card based on pen_range
    penetration = round(len(shoe)*random.uniform(pen_range[0],pen_range[1]))
    #generates playbale shoe with cards equal to penetration taken out
    
    return shoe[:-penetration],shoe[-penetration:]

