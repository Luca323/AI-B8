"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""
from a1_state import State
from a3_agent import Agent
import time
import random

class Player(Agent):
    def __init__(self, name="Player", size: tuple = (0, 0)):
        super().__init__(name, size)

    def move(self, st: State) -> State:
        return playermove(st)

def play(st: State, agentA: Agent, agentB: Agent)->None:
    player_input = input("Would you like to play a game of Hinger? Enter Y if yes, N if no.\n")
    player = Player(name="Player", size=st.dimensions)
    player_play = False
    agent_turn = 'A'
    player_turn = False
    
    if player_input.lower() != 'y':
        print("You have chosen not to play.")
        player_play = False
    else:
        print("You are now playing the game.")
        time.sleep(0.5)
        player_name = input("Input your name \n")
        if player_name:
            player.name = player_name
            player_play = True
        
    while True:
        if player_play:
            if player_turn:
                current_agent = player
                player_move = playermove(st)
                if player_move == (-1, -1):
                    print("Illegal move. Cannot remove from a 0. You lose.")
                    time.sleep(0.5)
                    print(f"{agentA.name} wins the game.")
                    return
                else:
                    row, column = player_move
                    next_state = st.move((row, column))
            else:
                current_agent = agentA
                next_state = current_agent.move(st)
            print(f"{current_agent.name}'s move:\n" + str(next_state))
            time.sleep(1.5)
        else:
            current_agent = agentA if agent_turn == 'A' else agentB
            
            next_state = current_agent.move(st)
            
            #If no more moves are possible, it’s a draw
            if not next_state:
                print("Game Over! It's a draw.")
                return
            
            
            print(f"{current_agent.name}'s move:\n" + str(next_state))
            
        if current_agent.win(next_state, st.numRegions()):
            print(f"Game Over, player {current_agent.name} Wins!")
            return
        
        
        # Switch turns
        st = next_state
        if player_play:
            player_turn = not player_turn
        else:
            agent_turn = 'B' if agent_turn == 'A' else 'A'
            
        
def playermove(st: State) -> tuple:
    player_moved = False
    start_time = time.time()
    print("Your turn")
    time.sleep(1)
    while player_moved == False:
        column = int(input("Enter Column:\n"))
        row = int(input("Enter Row:\n"))
        if st.grid[column - 1][row - 1] < 1:
            return -1, -1
        
        print(f"Your move is ({column}), ({row})")
        player_moved = True
    return column - 1, row - 1

def randomisegrid(height: int, width: int):
    grid = []
    for x in range(height):
        gridvals = []
        for x in range(width):
            gridval = random.randint(1, 3)
            gridvals.append(gridval)
        grid.append(gridvals)
    return grid

def playtest():
    grid = randomisegrid(4,4)
    start_state = State(grid=grid)
    agentA = Agent("Jotaro Kujo", start_state.dimensions)
    agentB = Agent("Dio Brando", start_state.dimensions)
    play(start_state, agentA, agentB)
    
if __name__ == "__main__":
    playtest()
