import numpy as np
from numpy import random

class Shoe:
    
    def __init__(self,verbose=False,shoe_size=6):
        
        #initializes _shoe with emty _shoe and _reserve variables
        self._shoe_size = shoe_size
        self._shoe = []
        self._reserve = []
        self._verbose = verbose
        self._emergency_reserve = []
        
    def CreateShoe(self,deck):
        '''
        PARAMETERS:
        _shoe_size - int of number of decks in _shoe

        RETURNS:
        nothing

        STORES:
        self._shoe - list of [_shoe_size * deck] cards minus random penetration
        self._reserve - list of cards equal to penetration (_reserve cards for dealing last hand)
        '''
        
        if self._shoe_size > 2:
            pen_range = [(52/(52*self._shoe_size)), ((52*1.5)/(52*self._shoe_size))]
        else:
            #single and double deck penetrate from 10 to 15 cards
            pen_range = [10/(52*self._shoe_size), 15/(52*self._shoe_size)]
        
        #verbose statement
        if self._verbose:
            print(f'Shuffling {self._shoe_size} decks into shoe...')
        
        #ensures that each deck added to the _shoe is shuffled
        #this might just be gamblers superstition on my part...
        for _ in range(self._shoe_size):
            random.shuffle(deck)
            self._shoe += deck

        random.shuffle(self._shoe) #in-place shuffle
        
        #random deck of emergency cards in case self._reserve is empty
        self._emergency_reserve = deck.copy()
        random.shuffle(self._emergency_reserve)
        
        #generates penetration at a random specific card based on pen_range
        penetration = round(len(self._shoe)*random.uniform(pen_range[0],pen_range[1]))
        #generates playbale _shoe with cards equal to penetration taken out

        #verbose statement
        if self._verbose:
            print('Cutting...')
        #stores playable__shoe and _reserve
        self._reserve = self._shoe[-penetration:]
        self._shoe = self._shoe[:-penetration]
        
        self.DrawCard() #burn fisrt card
        #verbose statement
        if self._verbose:
            print('Burning first card...')
            print('Shoe is read to play!')

    def DrawCard(self,thecount=None,count_card=False):
        '''
        takes first element off of self._shoe and returns it as a str
        PARAMETERS:
        count_card - bool flag to hide dealer's down card from the count before it's shown
        
        RETURNS:
        str - card
        '''
        if len(self._shoe)>0:
            #verbose statement
            if self._verbose:
                print('Drawing card from shoe...')
            card = self._shoe.pop(0) #pops first element off of _shoe and removes from list in-place    
        elif len(self._reserve)>0:
            #verbose statement
            if self._verbose:
                print('Shoe is now empty. Drawing from cut reserve...')
            card = self._reserve.pop(0) #pops first element off of _reserve and removes from list in-place
        else:
            if self._verbose:
                print('EMERGENCY RESERVE DRAW')
            card = self._emergency_reserve.pop(0) #pops first element off of _reserve and removes from list in-place 
        
        if count_card:
            thecount.UpdateCount(card)
    
        return card
        
        