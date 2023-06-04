import numpy as np
import random

class agent():
    def __init__(self, actions:np.array, init_state:np.array=[], states:np.array=[], reward:float=0.0, policy:dict={}, value_func:np.array=[]):
        self.A = actions
        self.s = init_state
        self.S = states
        self.r = reward
        self.pi = policy
        self.V = value_func
    
    def act(self):
        action = random.choices(self.A, self.pi[tuple(self.s)], k=1)[0] #This line selects from the probability distribution
        return action                                         # of the policy an action to take
    
    def __repr__(self):
        return f'''DPAgent(States:{self.S}, Actions:{self.A}, Current state:{self.s}, Reward:{self.r})'''
    
    def get_policy(self):
        return self.pi
    
    def get_value(self):
        return self.V
    