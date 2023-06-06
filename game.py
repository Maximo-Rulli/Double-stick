# Make essential imports
import tkinter as tk
from PIL import Image, ImageTk
from agent import agent
import pickle
from environment import S, A, MONEY, transition, LIFES


# Create the main Tkinter root
root = tk.Tk()
root.title("Doble o nada!")
root.geometry('550x300')
root.config(bg='#1f1f1f')
root.resizable(False, False)

# Create a label to display the money earned
earn_label = tk.Label(root, text="Dinero ganado: $0", fg='white', bg='#1f1f1f', font=('Times 14'), height=15)
earn_label.place(x=320, y=-125)

money_label = tk.Label(root, text= f"Dinero actual: ${min(MONEY)}", fg='white', bg='#1f1f1f', font=('Times 14'), height=15)
money_label.place(x=165, y=-125)

life_label = tk.Label(root, text= f"Vidas: {LIFES}", fg='white', bg='#1f1f1f', font=('Times 14'), height=15)
life_label.place(x=50, y=-125)

# Setup global variables (only the state)
init_state = [min(MONEY), LIFES, 0]
state = init_state

# LOAD POLICY 
# Load policy for RL agent
pi = {}
with open('policy.pkl', 'rb') as p:
    pi = pickle.load(p)
    print('Policy loaded!')
    

# Create the agent
Agent = agent(actions=A, init_state=[min(MONEY),3,0], states=S, reward=2, policy=pi)


def main():
    # Run the Tkinter event loop
    root.mainloop()
        


# Define the function to play the game as the agent
def play_agent():
    global state
    if state[1] > 0:
        Agent.s = state
        action = Agent.act()
        change = transition(action=action, state=Agent.s, playing=True)
        Agent.s = change[0]
        Agent.r = change[1]
        state = Agent.s
        earn_label.config(text=f'Dinero ganado: ${state[2]}')
        money_label.config(text=f'Dinero actual: ${state[0]}')
        life_label.config(text=f'Vidas: {state[1]}')
        root.after(2000, play_agent)

# Define the function to bid
def bid():
    global state
    state = transition(action=1, state=state, playing=True)[0]
    earn_label.config(text = f'Dinero ganado: ${state[2]}')
    money_label.config(text = f'Dinero actual: ${state[0]}')
    life_label.config(text = f'Vidas: {state[1]}')

# Define the function to stick
def stick():
    global state
    state = transition(action=0, state=state, playing=True)[0]
    earn_label.config(text = f'Dinero ganado: ${state[2]}')
    money_label.config(text = f'Dinero actual: ${state[0]}')
    life_label.config(text = f'Vidas: {state[1]}')

# Define the function to play the game as a human
def reset():
    global state
    earn_label.config(text = 'Dinero ganado: $0')
    money_label.config(text = 'Dinero actual: $2')
    life_label.config(text = 'Vidas: 3')
    state = init_state


# Create buttons for agent and human play
agent_button = tk.Button(root, text="IA", height= 2, width=15, bg='black', fg='white', bd=6, command=play_agent)
agent_button.place(x=50, y=200)

# Create label for the image of the machine
machine = Image.open("./resources/machine.png")
machine = machine.resize((50, 50), Image.Resampling.LANCZOS)
machine_tk = ImageTk.PhotoImage(machine)
label_machine = tk.Label(image=machine_tk, bg='#1f1f1f')
label_machine.image = machine_tk
label_machine.place(x=85, y=135)

# Button to double as a human
bid_button = tk.Button(root, text="Doble!", height= 2, width=15,bg='orange', fg='white', bd=6, command=bid)
bid_button.place(x=265, y=200)

# Create label for the image of the bid icon
bid_icon = Image.open("./resources/bid.png")
bid_icon = bid_icon.resize((50, 50), Image.Resampling.LANCZOS)
bid_tk = ImageTk.PhotoImage(bid_icon)
bid_label = tk.Label(image=bid_tk, bg='#1f1f1f')
bid_label.image = machine_tk
bid_label.place(x=295, y=135)


# Button to stick as a human
stick_button = tk.Button(root, text="Quedarse", height= 2, width=15,bg='green', fg='white', bd=6, command=stick)
stick_button.place(x=400, y=200)

# Create label for the image of the sitck icon
stick_icon = Image.open("./resources/stick.png")
stick_icon = stick_icon.resize((50, 50), Image.Resampling.LANCZOS)
stick_tk = ImageTk.PhotoImage(stick_icon)
stick_label = tk.Label(image=stick_tk, bg='#1f1f1f')
stick_label.image = stick_tk
stick_label.place(x=420, y=135)

# Button to reset everything
reset_button = tk.Button(root, text="Reset", height= 2, width=15,bg='red', fg='white', bd=6, command=reset)
reset_button.place(x=200, y=80)

if __name__ == '__main__':
    main()
