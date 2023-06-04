import numpy as np
import pickle
from environment import S, A, MONEY, transition


# DEFINE THE POLICY
# Define a random policy for each state
pi = {}
def create_policy(pi:dict={}):
    for i in range(len(S)):
        prob = np.random.uniform(size=1)[0]
        pi[tuple(S[i])] = [prob, 1-prob]
    return pi


# DEFINE STATE-VALUE FUNCTION
# Define the initial state-value function
V = {}
for i in range(len(S)):
    V[tuple(S[i])] = np.random.randn(1)[0]


#In this function we perform value iteration to find the optimal policy
def value_iteration(gamma:float=1.0, theta:float=0.0001):
    V = {}
    pi = {}
    for i in range(len(S)):
        V[tuple(S[i])] = np.random.randn(1)[0]
    V[(min(MONEY),0,0)] = 0
    while True:
        delta = 0
        for s in S:
            v = V[tuple(s)]
            V = bellman_optimality_update(V, s, gamma)
            delta = max(delta, abs(v - V[tuple(s)]))
        if delta < theta:
            break
    pi = create_policy(pi)
    for s in S:
        pi = q_greedify_policy(V, pi, s, gamma)
    return V, pi


#In this function we update the value function according to the Bellman equation of value iteration
def bellman_optimality_update(V:dict={}, s:list=[], gamma:float=1.0):
    """Mutate ``V`` according to the Bellman optimality update equation."""
    V_a = []
    for a in A:
        transitions = transition(a,s)
        v_temp = 0.0
        for (s_next, r, p) in transitions:
            v_temp += p*(r+gamma*V[tuple(s_next)])
        V_a.append(v_temp)
    V[tuple(s)] = max(V_a)
    return V


#Setup the function to greedify the policy with respect to current state-value function
def q_greedify_policy(V:dict={}, pi:dict={}, s:list = [], gamma:float = 1.0):
    """Mutate ``pi`` to be greedy with respect to the q-values induced by ``V``."""
    V_a = []
    for a in A:
        transitions = transition(a,s)
        v_temp = 0.0
        for (s_next, r, p) in transitions:
            v_temp += p*(r+gamma*V[tuple(s_next)])
        V_a.append(v_temp)
    pi_temp  = [0,0]
    pi_temp[np.argmax(V_a)] = 1
    pi[tuple(s)] = pi_temp
    return pi


def main():
    V, pi = value_iteration(gamma=1.0, theta=0.0001)
    with open('policy.pkl', 'wb') as p:
        pickle.dump(pi, p)
        print('Policy saved successfully!')
    with open('state_value.pkl', 'wb') as v:
        pickle.dump(V, v)
        print('State-value function saved successfully!')
        

if __name__ == '__main__':
    main()