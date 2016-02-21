import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

scriptStart = time.time()

#yeah, simply roll dice
def roll_dice(win_rate):
    roll = random.randrange(0, 100)    
    
    wR = 100 - win_rate 
    
    if roll > wR:
        return True
    if roll < wR:
        return False
    
#generate path
def bet_machine(starting_capital, risk_amount, trades, win_rate, id, bankrupt):
    value = starting_capital
    risk = risk_amount

    global bankruptcies
    global bets
    global inarowcounter
    global cnt
    if cnt != 0:
        cnt = 0
    do_count = True
    X = []
    Y = []
    i = 1
    
    #make trading
    while i <= trades:
        if roll_dice(win_rate):
            value += risk*0.81
            X.append(i)
            Y.append(value)
            do_count == False
            cnt = 0
        else:
            value -= risk
            X.append(i)
            Y.append(value)
            #count losers in a row
            if do_count == False:
                cnt += 1
                do_count == True
            else:
                cnt += 1
            
            #what if we broke?
            if value <= 0:
                bets.append(i)
                bankruptcies += 1
                if bankrupt:
                    break
            
        i += 1
        
    inarowcounter.append(cnt)
    
    #default
    if id == 0:
        plt.plot(X, Y)
    if id == 1:
        plt.plot(X, Y, "r")
    if id == 2:
        plt.plot(X, Y, "c")

if __name__ == "__main__":
    
    x = 0
    bets = []
    inarowcounter = []
    bankruptcies = 0
    cnt = 0
    
    #you define it
    paths = 1000
    risk_per_trade = 20

    # make paths
    while x < paths:
        bet_machine(starting_capital=1000, risk_amount=risk_per_trade, trades=10000, win_rate=55, id=0, bankrupt=True)
        print "Generated path no. %s" %x
        x += 1
    
    if len(bets) == 0:
        bets.append(0)
        
    data = ((bankruptcies/float(paths))*100.0,
           float(np.mean(bets)),
           float(np.min(bets)),
           max(inarowcounter),
           max(inarowcounter)*risk_per_trade)
    print "We got %s percent sold their home broke. \nLosing on average after %s moves. \n Unluckiest member broke after %s bets.\nLosses in a row %s or $%s. \n" %data
    
    plt.grid(True)
    plt.axhline(0, color = 'r')
    plt.ylabel('Wallet Value')
    plt.xlabel('Trades Count')
    plt.show()
        
    timeused = (time.time()-scriptStart)/60

    print("Done in ",timeused, " minutes")