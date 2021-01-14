#This is identical to script found in root/blackjack, except these need utils.blackjack.x during imports for scope reasons
import numpy as np
from numpy import random
import utils.blackjack.shoe as shoe
import utils.blackjack.player as player
import utils.blackjack.cardcounting as cardcounting

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
    aces = boolean; True if any aces are still able to be 11, False if all aces are 1s or no aces exist
    '''
    
    hand_value = 0
    num_aces = hand.count('ace') #gets number of aces
    aces_value = num_aces #assumes all aces are 1's for initial calculation
    
    hand_sorted = sorted(hand) #sorts all aces to back of array
    for card in hand_sorted[num_aces:]: #iterates through list without aces
        hand_value += cards[card] #calculates hand value pre-aces
    
    if 'ace' in hand_sorted:
        for i in range(num_aces+1): #iterates +1 in case there is only 1 ace
            if hand_value + ((i*11) + (num_aces-i)) <= 21: #checks combinations of 11s and 1s
                aces_value = (i*11) + (num_aces-i) #sets combination of 11s and 1s if not a bust
            else: #breaks out of loop once the maximum 11s:1s ratio is found
                break
        
    hand_value += aces_value
    
    return hand_value
    
def CheckAces(hand):
    '''
    Checks if aces are usable as 11s or if they must all be 1s
    
    PARAMETERS:
    hand - list of cards as str corresponding with cards dictionary
    
    RETURNS:
    aces = boolean; True if any aces are still able to be 11, False if all aces are 1s or no aces exist
    '''
    
    hand_value = 0
    num_aces = hand.count('ace') #gets number of aces
    aces_value = num_aces #assumes all aces are 1's for initial calculation
    aces = False
    
    hand_sorted = sorted(hand) #sorts all aces to back of array
    for card in hand_sorted[num_aces:]: #iterates through list without aces
        hand_value += cards[card] #calculates hand value pre-aces
        
    if 'ace' in hand_sorted:
        for i in range(num_aces+1): #iterates +1 in case there is only 1 ace
            if hand_value + (i + ((num_aces-i)*11)) <= 21 and i != num_aces: #checks if 11s are possible
                aces = True #aces can be 11s
    
    return aces
    
def HandAction(shoe_obj,current_player):
    '''
    Case statement of blackjack plays.
    1=Stand, 2=Hit, 3=Double Down, 4= Split, 5=Surrender

    PARAMETERS:
    shoe_obj = current shoe being drawn from
    current_player = Player object of current player containing hand(s) and bankroll
    '''

    for hand in current_player.GetHands():        
        #flag to tell when to stop prompting for current hand
        acting = True
        while acting:

            #assumes you're splitting, every other option turns this off
            splitting = True
            while splitting:

                if len(current_player.GetHands()) > 1:
                    for i,hand_to_display in enumerate(current_player.GetHands()):
                        print(f"Split Hand {i}: {hand_to_display['cards']}\nSplit Hand {i} value: {hand_to_display['value']}")

                    print(f"\nCurrent Split Hand is: {hand['cards']}\nCurrent Hand value: {hand['value']}")

                else:
                    print(f"\nCurrent Hand: {hand['cards']}\nCurrent Hand value: {hand['value']}")

                print('What would you like to do?')
                _input = input('1 = Stand\n2 = Hit\n3 = Double Down\n4 = Split\n5 = Surrender\n')

                if _input == '1':
                    #stand
                    print('Stand')
                    acting = False
                    splitting = False

                elif _input == '2':
                    #hit
                    print('Hit')
                    current_player.AddCard(hand,shoe_obj.DrawCard())
                    acting = True
                    splitting = False

                elif _input == '3':
                    print('Double Down')
                    #double down
                    #add below if block when money is implemented
                    if current_player.bankroll < hand['bet']*2:
                        print('Not enough money to double down')
                    else:
                        hand['bet'] *= 2
                        current_player.AddCard(hand,shoe_obj.DrawCard())
                        print(f"\nCurrent Hand: {hand['cards']}\nCurrent Hand value: {hand['value']}")
                        acting = False
                        splitting = False

                elif _input == '4':
                    #split
                    print('Split')
                    if len(hand['cards']) > 2 or cards[hand['cards'][0]] != cards[hand['cards'][1]]:
                        print('You can only split pairs. Select another option.')
                    elif current_player.bankroll < hand['bet'] * 2:
                        print('Not enough money to split')

                    elif len(current_player.hands) == 4:
                        print('You can only split 3 times.')

                    else:
                        #splits hand into two hands, but WON'T interate to the next one until splitting = False
                        current_player.AddHand([hand['cards'][0],shoe_obj.DrawCard()],hand['bet']) #adding the hand['bet'] effectively doubles the bet
                        hand['cards'] = [hand['cards'][1]] #since only ['cards'] and ['value'] gets edited in the original hand, ['bet'] is retained
                        current_player.AddCard(hand,shoe_obj.DrawCard())

                elif _input == '5':
                    #surrender
                    hand['bet'] = hand['bet']/2
                    hand['value'] = 22
                    print('Surrender (hand value will be set to 22)')

                    acting = False
                    splitting = False

                else:
                    #invalid input
                    print('Please select a valid input.')
                    splitting = False

                    
                if hand['value'] > 21:
                    print(f"\nCurrent Hand: {hand['cards']}\nCurrent Hand value: {hand['value']}")
                    print('Bust.')
                    acting = False
                    splitting = False
                elif hand['value'] == 21: #automatically stops if value is 21
                    print('Value is 21.')
                    acting = False
                    splitting = False

def HandActionAutomated(shoe_obj,current_player,count_obj=None,counting=False,d_hand=None):
    '''
    Automated version of HandAction that uses AutomatedBlackjack to play.
    1=Stand, 2=Hit, 3=Double Down, 4= Split, 5=Surrender
    
    PARAMETERS:
    shoe_obj = current shoe being drawn from
    current_player = Player object of current player containing hand(s) and bankroll
    d_hand = dictionary of dealers hand (only needed for automated blackjack)
    '''
    
    maxsplit = False #bool to check if maximum splits are reached so this doesn't loop forever
    
    for hand in current_player.GetHands():        
        #flag to tell when to stop prompting for current hand
        acting = True
        while acting:
            
            #assumes you're splitting, every other option turns this off
            splitting = True
            while splitting:
                _input = GetInput(p_hand = hand,
                                  d_hand = d_hand,
                                  maxsplit = maxsplit,
                                  count_obj=count_obj,
                                  counting=counting)
                
                if _input == 1:
                    #stand
                    acting = False
                    splitting = False

                elif _input == 2:
                    #hit
                    current_player.AddCard(hand,shoe_obj.DrawCard(count_obj,counting))
                    acting = True
                    splitting = False

                elif _input == 3:
                    #double down
                    hand['bet'] *= 2
                    current_player.AddCard(hand,shoe_obj.DrawCard(count_obj,counting))
                    acting = False
                    splitting = False

                elif _input == 4:
                    #split
                    if len(hand['cards']) > 2 or cards[hand['cards'][0]] != cards[hand['cards'][1]]:
                        print('FAILSAFE: TRYING TO SPLIT NON-PAIRS')
                        maxsplit = True
            
                    elif len(current_player.hands) == 4 and maxsplit == False: #check if maximum splits have been reached
#                         print('You can only split 3 times.')
                        maxsplit = True #flip maxsplit bool so this doesn't loop forever
                        
                    else:
                        #splits hand into two hands, but WON'T interate to the next one until splitting = False
                        current_player.AddHand([hand['cards'][0],shoe_obj.DrawCard(count_obj,counting)],hand['bet']) #adding the hand['bet'] effectively doubles the bet
                        hand['cards'] = [hand['cards'][1]] #since only ['cards'] and ['value'] gets edited in the original hand, ['bet'] is retained
                        current_player.AddCard(hand,shoe_obj.DrawCard(count_obj,counting))

                elif _input == 5:
                    #surrender
                    hand['bet'] = hand['bet']/2
                    hand['value'] = 22
#                     print('Surrender (hand value will be set to 22)')
                    acting = False
                    splitting = False

                else:
                    #invalid input
                    print('Please select a valid input.')
                    print(_input)
                    splitting = False

                if hand['value'] > 21:
                    acting = False
                    splitting = False
                elif hand['value'] == 21: #automatically stops if value is 21
                    acting = False
                    splitting = False

def GetInput(p_hand,d_hand,maxsplit,count_obj=None,counting=False):
    '''
    Gets the input int to feed into HandAction
    
    PARAMETERS:
    p_hand = dictionary; players hand
    d_hand = dictionary; dealers hand
    
    RETURNS:
    int corresponding to: 1=Stand, 2=Hit, 3=Double Down, 4= Split, 5=Surrender
    '''
    strategy = {}
    #1=Stand, 2=Hit, 3=Double Down, 4= Split, 5=Surrender
    #The None values are to buffer indexes so that the indexes match dealer hand values
    #i.e. 2-11 values are indexes 2-11 respectively
    
        #Dealers hand:   None,None,2,3,4,5,6,7,8,9,10,A
    strategy_basic = {4:[None,None,2,2,2,2,2,2,2,2,2,2],#in case of of maxsplit
            5:[None,None,2,2,2,2,2,2,2,2,2,2],
            6:[None,None,2,2,2,2,2,2,2,2,2,2],
            7:[None,None,2,2,2,2,2,2,2,2,2,2],
            8:[None,None,2,2,2,2,2,2,2,2,2,2],
            9:[None,None,2,3,3,3,3,2,2,2,2,2],
            10:[None,None,3,3,3,3,3,3,3,3,2,2],
            11:[None,None,3,3,3,3,3,3,3,3,3,3],
            12:[None,None,2,2,1,1,1,2,2,2,2,2],
            13:[None,None,1,1,1,1,1,2,2,2,2,2],
            14:[None,None,1,1,1,1,1,2,2,2,2,2],
            15:[None,None,1,1,1,1,1,2,2,2,5,5],
            16:[None,None,1,1,1,1,1,2,2,5,5,5],
            17:[None,None,1,1,1,1,1,1,1,1,1,5],
            18:[None,None,1,1,1,1,1,1,1,1,1,5],
            19:[None,None,1,1,1,1,1,1,1,1,1,5],
            20:[None,None,1,1,1,1,1,1,1,1,1,5],
            21:[None,None,1,1,1,1,1,1,1,1,1,1]}

    strategy_ace = {12:[None,None,2,2,2,3,3,2,2,2,2,2],#in case of of maxsplit
                    13:[None,None,2,2,2,3,3,2,2,2,2,2],
                    14:[None,None,2,2,2,3,3,2,2,2,2,2],
                    15:[None,None,2,2,3,3,3,2,2,2,2,2],
                    16:[None,None,2,2,3,3,3,2,2,2,2,2],
                    17:[None,None,2,3,3,3,3,1,1,2,2,2],
                    18:[None,None,1,1,1,1,3,1,1,1,1,1],
                    19:[None,None,1,1,1,1,1,1,1,1,1,1],
                    20:[None,None,1,1,1,1,1,1,1,1,1,1],
                    21:[None,None,1,1,1,1,1,1,1,1,1,1]}

    strategy_pair = {'AA':[None,None,4,4,4,4,4,4,4,4,4,4], #pair of aces
                     20:[None,None,1,1,1,1,1,1,1,1,1,1],
                     18:[None,None,4,4,4,4,4,1,4,4,1,1],
                     16:[None,None,4,4,4,4,4,4,4,4,4,5],
                     14:[None,None,4,4,4,4,4,4,2,2,2,2],
                     12:[None,None,4,4,4,4,4,2,2,2,2,2],
                     10:[None,None,3,3,3,3,3,3,3,3,2,2],
                     8:[None,None,2,2,2,4,4,2,2,2,2,2],
                     6:[None,None,4,4,4,4,4,4,2,2,2,2],
                     4:[None,None,4,4,4,4,4,4,2,2,2,2]}
    
    #Deviation block
    #1=Stand, 2=Hit, 3=Double Down, 4= Split, 5=Surrender
    if counting:
        if p_hand['cards'][0] == p_hand['cards'][1] and len(p_hand['cards']) == 2 and maxsplit == False: #hand is pair and maxsplit=False
            strategy = strategy_pair.copy() #use this dict in case no deviations are found
            #splitting deviations
            if p_hand['value'] == 20:
                if d_hand['shown_value'] == 4 and count_obj.true_count >= 6:
                    return 4
                elif d_hand['shown_value'] == 5 and count_obj.true_count >= 5:
                    return 4
                elif d_hand['shown_value'] == 6 and count_obj.true_count >= 4:
                    return 4
            elif 'ace' in p_hand['cards']:
                strategy_key = 'AA'

        elif CheckAces(p_hand['cards']): #checks if aces can still be 11s. if not, it's treated as a non-ace hand
            strategy = strategy_ace.copy() #use this dict in case no deviations are found
            #soft deviations
            if p_hand['value'] == 19:
                if d_hand['shown_value'] == 4 and count_obj.true_count >= 3:
                    return 3
                elif (d_hand['shown_value'] == 5 or d_hand['shown_value'] == 5) and count_obj.true_count >= 1:
                    return 3
            elif p_hand['value'] == 17:
                if d_hand['shown_value'] == 2 and count_obj.true_count >= 1:
                    return 3
        else:
            strategy = strategy_basic.copy() #use this dict in case no deviations are found
            #hard deviations
            if p_hand['value'] == 17 and d_hand['shown_value'] == 11:
                return 5
            elif p_hand['value'] == 16:
                if d_hand['shown_value'] == 9 and count_obj.true_count >= 4:
                    return 5
                elif d_hand['shown_value'] == 10 or d_hand['shown_value'] == 11:
                    return 1 ####################################################################################
                elif d_hand['shown_value'] == 8 and count_obj.true_count >= 4:
                    return 5
                elif d_hand['shown_value'] == 9 and count_obj.true_count <= -1:
                    return 2
                
            elif p_hand['value'] == 15:
                if d_hand['shown_value'] == 10 and count_obj.true_count >= 4:
                    return 5
                elif d_hand['shown_value'] == 10 and count_obj.true_count <= 0:
                    return 2
                elif d_hand['shown_value'] == 11 and count_obj.true_count >= -1:
                    return 5
                elif d_hand['shown_value'] == 9 and count_obj.true_count >= 2:
                    return 5
            elif p_hand['value'] == 13:
                if d_hand['shown_value'] == 2 and count_obj.true_count <= -1:
                    return 2
            elif p_hand['value'] == 12:
                if d_hand['shown_value'] == 2 and count_obj.true_count >= 3:
                    return 1
                elif d_hand['shown_value'] == 3 and count_obj.true_count >= 2:
                    return 1
                elif d_hand['shown_value'] == 4 and count_obj.true_count <= -1:
                    return 2                    
            elif p_hand['value'] == 10:
                if d_hand['shown_value'] == 10 and count_obj.true_count >= 4:
                    return 3
                elif d_hand['shown_value'] == 11 and count_obj.true_count >= 3:
                    return 3
            elif p_hand['value'] == 9:
                if d_hand['shown_value'] == 2 and count_obj.true_count >= 1:
                    return 3
                elif d_hand['shown_value'] == 7 and count_obj.true_count >= 3:
                    return 3
            elif p_hand['value'] == 8:
                if d_hand['shown_value'] == 6 and count_obj.true_count >= 2:
                    return 3
    else:
        strategy_key = p_hand['value']
    #     strategy_text = '' #uncomment for debugging
        if p_hand['cards'][0] == p_hand['cards'][1] and len(p_hand['cards']) == 2 and maxsplit == False:
            strategy = strategy_pair.copy()
    #         strategy_text = 'Pair Strat' #uncomment for debugging
            if 'ace' in p_hand['cards']:
                strategy_key = 'AA'
        elif CheckAces(p_hand['cards']): #checks if aces can still be 11s. if not, it's treated as a non-ace hand
            strategy = strategy_ace.copy()
    #         strategy_text = 'Ace Strat' #uncomment for debugging
        else:
            strategy = strategy_basic.copy()
    #         strategy_text = 'Basic Strat' #uncomment for debugging

            #uncomment for debugging
    #     try:
    #         strategy[strategy_key][d_hand['shown_value']]
    #     except:
    #         print(f'Player: {p_hand}')
    #         print(f'Dealer: {d_hand}')
    #         print(f'Key: {strategy_key}')
    #         print(f'Maxsplit: {maxsplit}')
    #         print(strategy_text)
    #         print(strategy)
    
    strategy_key = p_hand['value']
    return strategy[strategy_key][d_hand['shown_value']]
                    
def PlayBlackjack(bankroll,betsize=5):
    '''
    Plays blackjack
    
    PARAMETERS:
    bankroll = float of players current dollar count
    betsize = int of the baseline bet a player will make every hand
    
    No returns. This is a self-contained method
    that plays blackjack with while loops for user input and dealer decisions.
    '''
    
    #verbose statement
    print('Creating shoe...')
    deck = CreateDeck()
    shoe_obj = shoe.Shoe()
    
    #creates player object with bankroll
    print(f'Player created with bankroll of ${bankroll}')
    player_obj = player.Player(bankroll)
    dealer_obj = player.Player()
    
    playing = True
    while playing:
        #checks to see if shoe in the shoe class is empty
        #if empty, it will create a new shoe
        ### ONLY UNCOMMENT WHEN LOOP ISN'T INFINITE ###
        if len(shoe_obj._shoe) == 0:
            shoe_obj.CreateShoe(deck)
        
        #verbose statement
        print('New hand start!')
        #removes all hands from previous rounds
        player_obj.ResetHands()
        dealer_obj.ResetHands()
        
        print('Initial draw...')
        
        player_obj.AddHand([shoe_obj.DrawCard(),shoe_obj.DrawCard()],betsize)
        dealer_obj.AddHand([shoe_obj.DrawCard(),shoe_obj.DrawCard()])
        
        p_hand = player_obj.GetHands()[0] #gets 0th hand because we only have 1 hand right now
        d_hand = dealer_obj.GetHands()[0]

        print(f"Players hand: {p_hand['cards']}\nPlayers hand value: {p_hand['value']}")
        print(f"Dealers hand: {[d_hand['cards'][0]]}\nDealers hand value: {d_hand['shown_value']}")    

        player_acting = True #for while loop below if block
        '''
        Below is a huge block of if statements that are checking
        for player and dealer blackjack cases.
        '''
        if p_hand['value'] == 21:
            print('Blackjack!')
            
            #checks if dealer has blackjack from an ace up-card and player has blackjack
            if d_hand['shown_value'] == 11:
                even_money = input('Take even money? (y/n)\n')
                if even_money == 'y':
                    print(f"Player wins {p_hand['bet']}!")
                    player_obj.bankroll += _hand['bet']
                    player_obj.ResetHands()
                    player_acting = False
                else:
                    print("We're playing!")
                    if d_hand['value'] == 21:
                        print(f"Dealer also has blackjack with {d_hand['cards']}.\nPlayer pushes.")
                        player_obj.ResetHands()
                        player_acting = False
                        
            #checks if dealer has blackjack from a 10 up-card and player has blackjack
            elif d_hand['value'] == 21:
                print(f"Dealer also has blackjack with {d_hand['cards']}.\nPlayer pushes.")
                player_obj.ResetHands()
                player_acting = False
            else:
                print(f"Player wins {p_hand['bet']*1.5}!")
                player_obj.bankroll += (_hand['bet']*1.5)
                player_obj.ResetHands()
                player_acting = False
        
        #checks if dealer has blackjack from a 10 up-card but player doesn't have blackjack
        if d_hand['shown_value'] == 10 and d_hand['value'] == 21:
            print(f"Dealer has blackjack with {d_hand['cards']}.")
            print(f"Player loses ${p_hand['bet']}.")
            player_obj.bankroll -= p_hand['bet']
            player_obj.ResetHands()
            player_acting = False
        else:
            print('Dealaer does not have blackjack.')
        
        #checks if dealer has blackjack from an ace up-card and offers player insurance if they don't have blackjack
        if d_hand['shown_value'] == 11 and p_hand['value'] != 21:
            insurance = input('Insurance? (y/n) ')
            
            if d_hand['value'] == 21:
                print(f'Dealer has blackjack with {d_hand["cards"]}.')
                
                if insurance == 'y':
                    print("Player has insurance. Bet is lost, but insurance covers it.")
                    #since insurance is effectively a push, nothing happens.
                    player_obj.ResetHands()
                else:
                    print(f"Player loses ${p_hand['bet']}.")
                    player_obj.bankroll -= p_hand['bet']
                    player_obj.ResetHands()
                    
                player_acting = False
                
            else:
                print('Dealer does not have blackjack!')
                player_acting = True
        '''
        End of blackjack-checking if statements.
        '''

        '''
        Player decisions
        '''
        if player_acting:
            HandAction(shoe_obj,player_obj)
        
        '''
        Dealer decisions
        '''
        #if player busted out all their hands, dealer doesn't play
        #this for loop checks for any unbusted player hands
        #if blackjack/insurance/dealer blackjack has occurred, player_obj.GetHands() returns an empty list
        dealer_acting = False
        for _hand in player_obj.GetHands():
            if player_acting and _hand['value'] < 22:
                dealer_acting = True
                ##############################
                #COUNT DEALERS DOWN CARD HERE
                ##############################
            
        while dealer_acting:
            print(f"Dealers hand: {d_hand['cards']}\nDealers hand value: {d_hand['value']}")
            
            d_hand = dealer_obj.GetHands()[0]
            if d_hand['value'] == 17 and 'ace' in d_hand['cards']:
                #hit soft 17
                print('Dealer hits soft 17')
                dealer_obj.AddCard(d_hand,shoe_obj.DrawCard())
                
            elif d_hand['value'] < 17:
                #hit
                print('Dealer Hits')
                dealer_obj.AddCard(d_hand,shoe_obj.DrawCard())
                
            else:
                #stand
                print(f"Dealers hand: {d_hand['cards']}\nDealers hand value: {d_hand['value']}")
                print('Dealer Stands')
                dealer_acting = False
        
            if d_hand['value'] > 21:
                print(f"Dealers hand: {d_hand['cards']}\nDealers hand value: {d_hand['value']}")
                print('Dealer bust!')
                dealer_acting = False
        
        '''
        Payout block
        '''
        #if blackjack/insurance/dealer blackjack has occurred, player_obj.GetHands() returns an empty list
        for _hand in player_obj.GetHands():
            if _hand['value'] < 22 and d_hand['value'] > 21:
                print(f"Player has {_hand['cards']} ({_hand['value']}).")
                print(f"Player wins ${_hand['bet']} from dealer bust!")
                player_obj.bankroll += _hand['bet']

            elif _hand['value'] < 22 and _hand['value'] > d_hand['value']:
                print(f"Player has {_hand['cards']} ({_hand['value']}).")
                print(f"Dealer has {d_hand['cards']} ({d_hand['value']}).")
                print(f"Player wins ${_hand['bet']}!")
                player_obj.bankroll += _hand['bet']

            elif _hand['value'] == d_hand['value']:
                print(f"Player's {_hand['cards']} ({_hand['value']}) pushes with Dealer's {d_hand['cards']} ({d_hand['value']}).")
            
            else:
                print(f"Player loses ${_hand['bet']}.")
                player_obj.bankroll -= _hand['bet']
        
        print(f'\nCurrent Bankroll: ${player_obj.bankroll}')
        
        if player_obj.bankroll < betsize:
            print('OUT OF MONEY')
            playing = False        
        elif input('Continue playing? (y/n)') == 'n':
            playing = False
    
def AutomatedBlackjack(nhands,shoesize,bankroll,counting=False,even_money=False,betsize=5,verbose=False):
    '''
    Plays automated version of PlayBlackjack.
    Uses dictionaries defined in GetInput to employ basic strategy.
    
    PARAMETERS:
    nhands = int of number of hands to play and record
    counting = boolean to turn card counting on (True) or off (False)
    bankroll = float of players current dollar count
    betsize = int of the baseline bet a player will make every hand
    
    RETURNS:
    bank_history = a numpy array of the players bankroll every hand
    WL_history = a numpy array record of the win-loss for every hand (1=win, 0=loss)
    bj_history = a numpy array record of player blackjacks for every hand (1=blackjack, 0=not blackjack)
    '''

    if counting:
        thecount = cardcounting.TheCount(shoesize=shoesize)
        even_money = False #card counters never take even money
    else:
        thecount = None
    
    deck = CreateDeck()
    shoe_obj = shoe.Shoe(shoe_size=shoesize,verbose=verbose)
    
    
    #creates player object with bankroll
    if verbose:
        print(f'Player created with bankroll of ${bankroll}')
    player_obj = player.Player(bankroll)
    dealer_obj = player.Player()
    
    bank_history = np.array([player_obj.bankroll])
    WL_history = np.zeros(0)
    bj_history = np.zeros(0)

    if verbose:
        print("Playing...")
    for i in range(nhands):
        #checks to see if shoe in the shoe class is empty
        #if empty, it will create a new shoe
        ### ONLY UNCOMMENT WHEN LOOP ISN'T INFINITE ###
        if len(shoe_obj._shoe) == 0:
            shoe_obj.CreateShoe(deck)
            if counting:
                thecount.ResetCount()
                
        
        #removes all hands from previous rounds
        player_obj.ResetHands()
        dealer_obj.ResetHands()
        
        if counting:
            if thecount.true_count >= 2:
                #(70% of advantage)*original bankroll
                #%advantage is a linear progression as follows:
                #round(true_count//2)
                new_bet = (((round(thecount.true_count)//2)*0.7)/100)*bankroll #(70% of advantage)*original bankroll
#                 print(f'True Count = {thecount.true_count}, bet = {new_bet}')
            else:
                new_bet = betsize
        else:
            new_bet = betsize
        
        player_obj.AddHand([shoe_obj.DrawCard(thecount,counting),shoe_obj.DrawCard(thecount,counting)],new_bet)
        dealer_obj.AddHand([shoe_obj.DrawCard(thecount,counting),shoe_obj.DrawCard()]) #only count the dealers up-card
        
        p_hand = player_obj.GetHands()[0] #gets 0th hand because we only have 1 hand right now
        d_hand = dealer_obj.GetHands()[0]  

        player_acting = True #for while loop below if block
        '''
        Below is a huge block of if statements that are checking
        for player and dealer blackjack cases.
        '''
        if p_hand['value'] == 21:
            #records blackjack history
            bj_history = np.append(bj_history,1)
            
            #checks if dealer has blackjack from an ace up-card and player has blackjack
            if d_hand['shown_value'] == 11:
#                 even_money = input('Take even money? (y/n)\n')
                if even_money:
#                     print(f"Player wins {p_hand['bet']}!")
                    player_obj.bankroll += p_hand['bet']
                    player_obj.ResetHands()
                    player_acting = False
                else:
#                     print("We're playing!")
                    if d_hand['value'] == 21:
#                         print(f"Dealer also has blackjack with {d_hand['cards']}.\nPlayer pushes.")
                        player_obj.ResetHands()
                        player_acting = False
                        
            #checks if dealer has blackjack from a 10 up-card and player has blackjack
            elif d_hand['value'] == 21:
#                 print(f"Dealer also has blackjack with {d_hand['cards']}.\nPlayer pushes.")
                player_obj.ResetHands()
                player_acting = False
            else:
#                 print(f"Player wins {p_hand['bet']*1.5}!")
                player_obj.bankroll += (p_hand['bet']*1.5)
                player_obj.ResetHands()
                player_acting = False
        else:
            #records blackjack history
            bj_history = np.append(bj_history,0)
        
        #checks if dealer has blackjack from a 10 up-card but player doesn't have blackjack
        if d_hand['shown_value'] == 10 and d_hand['value'] == 21:
#             print(f"Dealer has blackjack with {d_hand['cards']}.")
#             print(f"Player loses ${p_hand['bet']}.")
            player_obj.bankroll -= p_hand['bet']
            player_obj.ResetHands()
            player_acting = False
        
        #checks if dealer has blackjack from an ace up-card and offers player insurance if they don't have blackjack
        if d_hand['shown_value'] == 11 and p_hand['value'] != 21:
#             insurance = input('Insurance? (y/n) ')
            if counting and thecount.true_count > 3: #if the counting is > 3, counters take insurance
                insurance = True
            else:
                insurance = False #normal players never take insurance
    
            if d_hand['value'] == 21:
#                 print(f'Dealer has blackjack with {d_hand["cards"]}.')
                
                if insurance:
#                     print("Player has insurance. Bet is lost, but insurance covers it.")
                    #since insurance is effectively a push, nothing happens.
                    player_obj.ResetHands()
                else:
#                     print(f"Player loses")
                    player_obj.bankroll -= p_hand['bet']
                    player_obj.ResetHands()
                    
                player_acting = False
                
            else:
#                 print('Dealer does not have blackjack!')
                if insurance:
                    player_obj.bankroll -= (p_hand['bet']/2)
                player_acting = True
        '''
        End of blackjack-checking if statements.
        '''

        '''
        Player decisions
        '''
        if player_acting:
            #HandActionAutomated parameters: shoe_obj,current_player,count_obj=None,counting=False,d_hand=None
            HandActionAutomated(shoe_obj=shoe_obj,
                                current_player=player_obj,
                                count_obj=thecount,
                                counting=counting,
                                d_hand=d_hand)
        
        '''
        Dealer decisions
        '''
        #if player busted out all their hands, dealer doesn't play
        #this for loop checks for any unbusted player hands
        #if blackjack/insurance/dealer blackjack has occurred, player_obj.GetHands() returns an empty list
        dealer_acting = False
        if counting:
            thecount.UpdateCount(d_hand['cards'][1]) #update count with dealers down-card
        for _hand in player_obj.GetHands():
            if player_acting and _hand['value'] < 22:
                dealer_acting = True
            
        while dealer_acting:
#             print(f"Dealers hand: {d_hand['cards']}\nDealers hand value: {d_hand['value']}")
            
            d_hand = dealer_obj.GetHands()[0]
            if d_hand['value'] == 17 and 'ace' in d_hand['cards']:
                #hit soft 17
                dealer_obj.AddCard(d_hand,shoe_obj.DrawCard(thecount,counting))
                
            elif d_hand['value'] < 17:
                #hit
                dealer_obj.AddCard(d_hand,shoe_obj.DrawCard(thecount,counting))
                
            else:
                #stand
                dealer_acting = False
        
            if d_hand['value'] > 21:
                #Dealer bust
                dealer_acting = False
        
        '''
        Payout block
        '''
        #if blackjack/insurance/dealer blackjack has occurred, player_obj.GetHands() returns an empty list
        for _hand in player_obj.GetHands():
            if _hand['value'] < 22 and d_hand['value'] > 21:
                player_obj.bankroll += _hand['bet']

            elif _hand['value'] < 22 and _hand['value'] > d_hand['value']:
                player_obj.bankroll += _hand['bet']

            elif _hand['value'] == d_hand['value']:
                #push
                pass
            else:
                player_obj.bankroll -= _hand['bet']
        
        #records bankroll changes
        bank_history = np.append(bank_history,player_obj.bankroll)
        #records wins/losses
        if bank_history[i] >= bank_history[i-1]:
            WL_history = np.append(WL_history,1)
        else:
            WL_history = np.append(WL_history,0)
            
        #considers you out of money if you can't split the maximum amount of times (4)
        if counting and player_obj.bankroll < bankroll/4:
            if verbose:
                print(f'OUT OF MONEY AFTER {i} HANDS')
            break
        elif player_obj.bankroll < betsize*4:
            if verbose:
                print(f'OUT OF MONEY AFTER {i} HANDS')
            break
            
        #debuging
#         if counting:
#             if abs(thecount.true_count) > 3:
#                 print(f"Runnig count = {thecount.running_count}")
#                 print(f"True count = {thecount.true_count}")
    if verbose:
        print("Finished!")
        print(player_obj.bankroll,len(bank_history),len(WL_history),len(bj_history))
    return player_obj.bankroll,bank_history,WL_history,bj_history
    


if __name__ == '__main__':
    print("Welcome to Jackson's Blackjack!\nLoading game elements...")
    
    PlayBlackjack(5000,5)