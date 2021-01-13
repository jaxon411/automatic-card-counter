from numpy import random

class TheCount:
    
    def __init__(self,shoesize=6):
        self.running_count = 0
        self.true_count = 0
        self.shoesize = shoesize
        self.penetration = self.GeneratePenetration(self.shoesize)
        self.hi = ['ten','jack','queen','king','ace']
        self.lo = ['two','three','four','five','six']
        
    def GeneratePenetration(self,shoesize):
        #since the player doesn't know the exact penetration, we have to generate our own estimate
        
        if shoesize > 2:
            #greater than 2 decks penetrate from 1 to 1.5 decks
            pen_range = [(52/(52*shoesize)), ((52*1.5)/(52*shoesize))]
        else:
            #single and double deck penetrate from 10 to 15 cards
            pen_range = [10/(52*shoesize), 15/(52*shoesize)]
        
        penetration = round(52*shoesize*random.uniform(pen_range[0],pen_range[1]))
            
        return penetration
    
    def UpdateCount(self,card):
        if card in self.lo:
            self.running_count += 1
        elif card in self.hi:
            self.running_count -= 1

        decks_left = round(((52*self.shoesize)-self.penetration)/52,1)
        print('DECKS LEFT: '+str(decks_left))
        print('DECKS LEFT: '+str(decks_left))
        print('DECKS LEFT: '+str(decks_left))
        print('DECKS LEFT: '+str(decks_left))
        print('DECKS LEFT: '+str(decks_left))
        print('DECKS LEFT: '+str(decks_left))
        print('DECKS LEFT: '+str(decks_left))
        self.true_count = round(self.running_count/decks_left,1)
     
    def ResetCount(self):
        self.running_count = 0
        self.true_count = 0
        self.penetration = self.GeneratePenetration(self.shoesize)
        