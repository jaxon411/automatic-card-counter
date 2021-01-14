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

## ♦ Automatic Card Counting ♦
My card detection uses a YOLOv5m model trained on about ~150 card images (found in `automatic-card-counter/imgs_raw`). More information about YOLOv5 can be found here:<br />
https://github.com/ultralytics/yolov5
<br />
<br />
I trained for 500 epocs, and saw a validation accuracy of 94%. To us my model, you can follow these steps:<br />
1. **Video file detection**
   - In a terminal, navigate to `automatic-card-counter/yolov5`
   - Run `!python detect.py --weights runs/train/exp5/weights/best.pt --img 1024 --conf 0.93 --exist --source PATH/TO/VIDEOFILE.mp4
   - The detect script will automatically output a video to `automatic-card-counter/yolov5/runs/detect/exp`
   - If you would like to mess around with the `detect.py` parameters, here is a list of arguments I found useful:
```
--weights
    default='yolov5s.pt', help='model.pt path(s)
--source'
    default='data/images', help='source')  # file/folder, 0 for webcam
--img
    default=640, help='inference size (pixels)
--conf
    default=0.25, help='object confidence threshold
--iou
    default=0.45, help='IOU threshold for NMS
--view-img
    help='display results')
--save-txt
    save results to *.txt
--save-conf
    save confidences in --save-txt labels
--exist
    existing project/name ok, do not increment directory
   ```
2. **Live video feed detection**
   - In a terminal, navigate to `automatic-card-counter/yolov5`
   - Run `!python detect.py --weights runs/train/exp5/weights/best.pt --img 1024 --conf 0.93 --exist --source 0`
     - `source 0` indicates a webcam on your computer. If you have multiple webcams, incrementing the source number will use different webcams 
   - There will be no video exports, 
   - Again, you can use the same parameters listed above.
## ♦ Citations ♦
![image](https://i.imgur.com/f1rWEFt.png)
<br />
<br />
Resources I used to learn about Blackjack and card counting:<br />
Blackjack 101<br />
https://www.888casino.com/blog/blackjack-strategy-guide/basic-blackjack-strategy
<br />
<br />
Blackjack Basic Strategy<br />
https://www.blackjackonline.com/wp-content/uploads/2020/01/bj-strategy-double-deck-hits-soft17-min.png
<br />
<br />
Card Counting 101<br />
https://www.vegas-aces.com/site/articles/card-counting-101.html
<br />
<br />
Card Counting Betting Spread Guide<br />
https://www.instructables.com/Card-Counting-and-Ranging-Bet-Sizes/
<br />
<br />
<br />
Utah State University paper on card counting:<br />
*The Expected Value of an Advantage Blackjack Player*<br />
https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=1528&context=gradreports
<br />
<br />
<br />
YOLOv5 github:<br />
Github<br />
https://github.com/ultralytics/yolov5
