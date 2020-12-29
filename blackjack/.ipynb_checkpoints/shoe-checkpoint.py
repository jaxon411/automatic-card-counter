import numpy as np
from numpy import random

class Shoe:
    
    def __init__(self,shoe_size=6):
        
        #initializes shoe with emty shoe and reserve variables
        self.shoe_size = shoe_size
        self.shoe = []
        self.reserve = []
        
    def CreateShoe(self,deck):
        '''
        PARAMETERS:
        shoe_size - int of number of decks in shoe

        RETURNS:
        nothing

        STORES:
        self.shoe - list of [shoe_size * deck] cards minus random penetration
        self.reserve - list of cards equal to penetration (reserve cards for dealing last hand)
        '''
        
        if self.shoe_size > 2:
            pen_range = [(52/(52*self.shoe_size)), ((52*1.5)/(52*self.shoe_size))]
        else:
            #single and double deck penetrate from 10 to 15 cards
            pen_range = [10/(52*self.shoe_size), 15/(52*self.shoe_size)]

        #ensures that each deck added to the shoe is shuffled
        #this might just be gamblers superstition on my part...
        for _ in range(self.shoe_size):
            random.shuffle(deck)
            self.shoe += deck

        random.shuffle(self.shoe) #in-place shuffle

        #generates penetration at a random specific card based on pen_range
        penetration = round(len(self.shoe)*random.uniform(pen_range[0],pen_range[1]))
        #generates playbale shoe with cards equal to penetration taken out

        #stores playable_shoe and reserve
        self.reserve = self.shoe[-penetration:]
        self.shoe = self.shoe[:-penetration]
    

    def DrawCard(self):
        '''
        takes first element off of self.shoe and returns it as a str
        
        RETURNS:
        str - card
        '''
        if len(self.shoe)>0:
            return self.shoe.pop(0) #pops first element off of shoe and removes from list in-place
        else:
            return self.reserve.pop(0) #uses reserve deck for last hand if shoe is empty
        
        