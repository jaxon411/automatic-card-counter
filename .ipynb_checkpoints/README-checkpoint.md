# ♦ Blackjack ♦

Before we get into how my model and scripts work, we need to first understand the game of blackjack. Blackjack is a playing card game in which the player(s) and dealer are trying to get a hand as close to 21 as possible without going over.
<br />
<br />
Here are the values of each card in the game.
<br />
<br />
![image](https://1502298981.rsc.cdn77.org/media/1286/backjack-card-values.jpg?width=500&height=281.25)
<br />

### ♦ Player Turn Order ♦

1. Each player is dealt two cards face-up, while the dealer is dealt one card face-up and one card face-down. Any player that has 21 (an Ace and a 10-cost card) automatically wins. This is known as a Blackjack.
3. The dealer checks if they have Blackjack by looking at their face down card without revealing it.
4. If the dealer has Blackjack, everyone loses (unless a player also has Blackjack, which ties). If not, play continues.
5. All players take their turn to act in sequential order, with the dealer acting last. Each player is allowed a set of moves on their turn:
   - **Hit** &ndash; Draw a card. You can continue to hit until you either Stand or Bust (having a hand value exceeding 21)
   - **Stand** &ndash; Stop drawing cards, you hand value is now locked in for the rest of play
   - **Double Down** &ndash; Double your current bet and draw **one** additional card. You **must** draw one card and only one card.
   - **Split** &ndash; Only available when you have two cards of the same value. Split your hand into two separate hands and play them each (you must also match your bet with your new hand). If you continue to draw cards of the same value on your split hands, you can continue to split up to four times.
   - **Surrender** &ndash; Concede the hand, but only lose half your initial bet
<br />
6. Finally, once all player hands are locked in, the dealer acts.

### ♦ The Dealer ♦
Unlike the plyaers, the Dealer does not get to decide what to do with their hand. Instead, the dealer **must** follow a specific play pattern. This play pattern, coupled with the fact that players only see one of the dealers cards during their turn, is what gives the casino it's advantage over the players. Dealer play patterns vary depending on a few factors (minimum/maxiumum bet, Blackjack payout ration, Blackjack version being played, etc.), but generally these are the rules that govern how the Dealer plays their turn:

- The dealer flips over their face-down card, revealing their hand value to the players.
- The dealer continues to hit until either their hand has a value of 17, or they Bust.
- Once either condition is met, the Dealer compares their hand value to the rest of the players.
- If any players have a hand closer to 21 than the dealer (without Busting) they win.
- If the Dealer busts, every player who did not Bust on their turn wins.

Play then resets with new bets from the player(s).

### ♦ Basic Strategy ♦

Since players know **exactly** what play pattern the Dealer must follow before any hand is actually played, we're able to calculate the probability of winning based on the players hand and the dealers hand. Then, we can find the mathmatically optimal actions the player should take during their turn given those hand values.
<br />
<br />
This is called **Basic Strategy**, and players have translated these probabilities into convenient charts that we can use to play.
<br />
<br />
![image](https://i.imgur.com/zclr6WN.jpg)
<br />
*Note: "DAS" mentioned in the Key stands for Double After Split*
<br />
<br />
There is  a problem with basic stratgety, however...the Casino still has the edge. This is why, despite players using basic strategy, Casinos still make money at Blackjack tables.
<br />
<br />
But there is something that players can do to tilt the game in their favor...

### ♦ Card Counting ♦
In 1962, Edward O. Thorp published his book *Beat the Dealer*, in which he outlines a strategy players can employ to give them an advantage: **Card Counting**.
<br />
<br />
In it's most basic form, card counting is a stragetgy that assigns a +1, -1, or 0 value to various cards depending on how benificial they are for the player.
<br />
<br />
![image](https://www.wikihow.com/images/thumb/d/d5/Win-at-Blackjack-Step-9-Version-3.jpg/v4-460px-Win-at-Blackjack-Step-9-Version-3.jpg)
<br />
<br />

This method words because Blackjack is a dependent variable game, meaning that cards that have been drawn inform us about which cards are still left in the deck/shoe. A high count tells us that more high-value cards (Tens and Aces) are in the deck, whereas a low count tells us that more low-value cards are in the deck.
<br />
<br />
As players, this doesn't make it more likely that we will win. After all, the dealer can draw those high value cards to. Instead, it informs us **how we should bet**. When the count is high, bet high. When the count is low, bet low. This means that over time, our winnings will offset our losses monetarily, even though we lose individual hands more often than we win.
<br />
<br />
This is the system I programmed into this repo.

> For more information on the math behind black jack and card counting, you can visit these resources:<br />
https://www.888casino.com/blog/blackjack-strategy-guide/basic-blackjack-strategy<br />
https://www.vegas-aces.com/site/articles/card-counting-101.html
