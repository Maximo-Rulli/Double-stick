import numpy as np
import random

# SETUP ENVIRONMENT
# States
MONEY = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
MONEY_ZERO = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]  #Same array as before but with 0 added (only to create the states)
LIFES = 3
PROBS = {}  #List containing probabilities of losing mapped to each amount of money

#Setup the probabilities of losing to each amount of money
for i in range(len(MONEY)):
    PROBS[MONEY[i]] = 0.075*(i+1)

WON = [] #The array WON is only a combination of all possible rewards for the player to be obtained
S = []
for i in MONEY_ZERO:
    for j in MONEY_ZERO:
        WON.append(j+i)

WON = np.unique(np.array(WON))  #Clean the array to do not have repeated elements

#We setup the possible states
for i in range(LIFES):
    for j in MONEY:
        if i == 0:  #If there is 1 life ramaining there are j**k combinations
            for k in WON:
                S.append([j, i+1, k])
        elif i == 1: #If there are 2 lifes ramaining there are j**k combinations
            for k in MONEY_ZERO:
                S.append([j, i+1, k])
        elif i == 2: #If there are 3 lifes ramaining there are j combinations
            S.append([j, i+1, 0])
        
S.append([min(MONEY), 0, 0]) #We add the terminal state

S = np.array(S, dtype=int)  # The states are an array of dimensions (4621, 3) in which each row of numbers represents
                 # the current money (position 0) and the number of lifes left (position 1) the money obtained from previous games (position 2)

#Define all the possible actions to take
A = np.array([0, 1]) #stick = 0, double = 1

# DEFINE THE ENVIRONMENT
# Define the environment's dynamics
def transition(action:int, state:list, playing:bool=0):
    #The first number is the amount of money and the
    # second number of the state represents the lifes left
    # and the third number is the accumulation of money won
    money, lifes, won = state[0], state[1], state[2]  
    
    
    if (money<max(MONEY) and lifes>1) or (money==max(MONEY) and lifes>1):
        s_lose = [min(MONEY), lifes-1, won] #If the agent has more than 1 life and loses, it arrives initial state with 1 life less
    elif (money<max(MONEY) and lifes==1) or (money==max(MONEY) and lifes==1):
        if not playing:
            s_lose = [min(MONEY), 0, 0] #If the agent has only 1 life and loses, it arrives at terminal state
        else:
            s_lose = [0, 0, won]
    elif (state==[min(MONEY),0,0]):
        return [[[min(MONEY), 0, 0], 0, 1]] #If the agent is on terminal state, it will remain there until another episode starts

    if money<max(MONEY) and lifes>0:
        s_win = [money*2, lifes, won] #If the agent doubles and has more than 0 lifes it continues playing
    elif money==max(MONEY) and lifes>1:
        s_win = [min(MONEY), lifes-1, money+won] #If the agent arrives at maximum money, loses a life and keeps what it won
    elif money==max(MONEY) and lifes==1:
        s_win = [min(MONEY), 0, 0] #If the agent arrives at maximum money and has 1 life, it will always go to terminal state

    s_next = [s_lose, s_win] # In this line we set the possible next states, and if the agent 
    # is already in the maximum money it returns to 2 and loses a life as explained before

    lose = PROBS[money] #The probability of losing increases as the player's money increases
    prob = [lose, 1-lose]

    #Define the reward signal
    if action == 0:
        if not playing:
            if lifes != 1:
                return [[[min(MONEY), lifes-1, won+money], 10*won+money+(lifes-1)*100, 1]]
            else:
                return [[[min(MONEY), 0, 0], 10*won+money, 1]]
        else:
            if lifes != 1:
                return [[min(MONEY), lifes-1, won+money], 10*won+money+(lifes-1)*100]
            else:
                return [[0, 0, won+money], 10*won+money]
    elif action == 1:
        if not playing:
            return [[s_next[1], 2*money+(lifes-1)*100 if money<max(MONEY) else 0, prob[1]],
                    [s_next[0], -10*money, prob[0]]]
        else:
            outs = ['lose', 'win']
            outcome = random.choices(outs, prob, k=1)[0]
            if outcome == 'win':
                return [s_next[1], 2*money+(lifes-1)*100 if money<max(MONEY) else 0]
            else:
                return [s_next[0], -10*money]
