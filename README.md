# Double-stick 💸 🤖
A game in which the player competes with an AI to see who wins the most amount of money in 3 rounds of biding (doubling) or sticking (keeping the money of the round)

# The game's rules 🎲
1. The player will start with 3 lifes
2. Each turn the player may either bid (double his money) or stick (keep his current money)
  - If he doubles: he may either double his money or lose it all. The more money the player has the higher the chances of losing are. If the player loses he will also lose a life.
  - If the sticks: the player will keep his current money and store it in his savings. If the player sticks he will also lose a life
3. The player repeats point 2 until he runs out of lifes
4. Once the player finishes, the algorithm will play a game, and the one between the player and the algorithm who achieves the highest savings wins!


# Files 📁

- agent.py: Declaration of the agent object is modeled with all its possible actions
- environment.py: Declaration of the environment (game dynamics)
- game.py: Creation of the interface and the game itself
- rl.py: Training of the RL agent using DP (dynamic programming)
- policy.pkl: Optimal policy saved from the agent training 
- state_value.pkl: Optimal state-value function saved from the agent training
- Resources: Images to be displayed in the game
