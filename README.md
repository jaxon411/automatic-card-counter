# ♦ Automated Blackjack Card-Counting Neural Network ♦

![Image](https://i.imgur.com/yZyI7BS.png)

### By:<br />Jackson Hall

## ♦ Motivation and Goal ♦

This project was born from the combination of my love of Blackjack with my love of neural netwokrs. Image classifcation has always been a fun an interesting persuit for me, but this was my first time attempting object classification.

> “Object detection is a computer vision technique that allows us to identify and locate objects in an image or video.”<br />
Source: https://www.fritz.ai/object-detection/

My ultimate goal was to create a playing card detection model trained to recognize cards on a table, count cards based on a proven card counting system, and display what the player should do given the current hand. I'm happy to report that I was successful!

### Application Pipeline
![Image](https://i.imgur.com/lxMtN9l.png)

PARAMETERS:
bankroll = float of players current dollar count
betsize = int of the baseline bet a player will make every hand

No returns. This is a self-contained method
that plays blackjack with while loops for user input and dealer decisions.
'''
#Play blackjack manually
blackjack.PlayBlackjack(bankroll=500,betsize=5)

## ♦ Blackjack ♦

Before we get into how my model and scripts work, we need to first understand the game of blackjack. Blackjack is a playing card game in which the player(s) and dealer are trying to get a hand as close to 21 as possible without going over.
<br />
<br />
Here are the values of each card in the game.
<br />
<br />
![image](https://1502298981.rsc.cdn77.org/media/1286/backjack-card-values.jpg?width=500&height=281.25)
<br />

For a more in depth explination about Blackjack and Card Counting rules, I've put together a document here:<br />
https://github.com/jaxon411/automatic-card-counter/tree/main/blackjack
<br />
<br />
Otherwise, you can read on for how to use this repo.

## ♦ My Blackjack Program ♦
In my repository, you can find a fully functional Blackjack game in the `automatic-card-counter/blackjack` folder. To use it, follow these instructions:
<br />
<br />
- In a Ipython terminal, navigate to `automatic-card-counter/blackjack`.
- Run `blackjack.PlayBlackjack(bankroll=500,betsize=5)`
<br />
<br />
`bankroll` is your starting pool of chips/dollars/units, and `betsize` determines what you bet for each hand.
<br />
<br />
There is also an autmated version of blackjack found in the same `blackjack.py` script. You can have the computer play blackjack with basic strategy or card counting and return various values.
<br />
<br />

- In an Ipython terminal, navigate to `automatic-card-counter/blackjack`.
- Run `blackjack.AutomatedBlackjack(nhands=2500,shoesize=2,counting=False,even_money=True,bankroll=10_000,betsize=13)`
- This will return 4 values: 
  - final_bankroll = float of the final bankroll the player has
  - bank_history = a numpy array of the players bankroll every hand
  - WL_history = a numpy array record of the win-loss for every hand (1=win, 0=loss)
  - bj_history = a numpy array record of player blackjacks for every hand (1=blackjack, 0=not blackjack)
- So it would be useful to set those to variables with something like <br />
`final_bankroll,bank_history,WL_history,blackjacks_history = blackjack.AutomatedBlackjack(nhands=2500,shoesize=2,counting=False,even_money=True,bankroll=10_000,betsize=13)`
- You can also turn card counting on and off via the `coutning` variable
  - Note that card counters never take even money on Blackjack, so `even_money` will be turned to `False` automatically if `counting=True`.
