"""
Hinger Project
Coursework 001: CMP-6058A Artificial Intelligence

Game-playing functionality

@Authors: B8 (100415489, 100426892, 100437079)
"""
from a1_state import State
from a3_agent import Agent
import time
import random

class Player(Agent): #Creates class for Player to utilise win-condition function
    def __init__(self, name="Player", size: tuple = (0, 0)):
        super().__init__(name, size)

    def move(self, st: State) -> State:
        return playermove(st)

def play(st: State, agentA: Agent, agentB: Agent) -> None:
    player_input = input("Would you like to play a game of Hinger? Enter Y if yes, N if no.\n")
    player = Player(name="Player", size=st.dimensions)
    
    player_play = False
    agent_turn = 'A' #Determines whose turn it is
    player_turn = False
    moveNum = 0
    
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
                if player_move == (-2, -2):
                    print(f"Out of bounds, illegal move. You lose.\n{agentA.name} wins the game.\nTurns taken: {moveNum}")
                    return
                elif player_move == (-1, -1):
                    print(f"Illegal move. Cannot remove from a 0. You lose.\n{agentA.name} wins the game.\nTurns taken: {moveNum}")
                    return
                else:
                    row, column = player_move
                    next_state = st.move((row, column))
            else:
                current_agent = agentA
                next_state = current_agent.move(st)
            time.sleep(1)
            moveNum += 1
            print(f"Move: {moveNum}")
            print(f"{current_agent.name}'s turn:\n" + str(next_state))
        else:
            current_agent = agentA if agent_turn == 'A' else agentB
            
            next_state = current_agent.move(st)
            moveNum += 1
            
            if not next_state:
                print("Game Over! It's a draw.")
                print(f"Turns taken: {moveNum - 1}")
                return
            
            print(f"Move: {moveNum}")
            print(f"{current_agent.name}'s move:\n" + str(next_state))
        if current_agent.win(next_state, st.numRegions()):
            print(f"Game Over, {current_agent.name} Wins!")
            print(f"Turns taken: {moveNum}")
            return
        
        
        # Switch turns between player and agent or between two agents
        st = next_state
        if player_play:
            player_turn = not player_turn
        else:
            agent_turn = 'B' if agent_turn == 'A' else 'A'
            
        
def playermove(st: State) -> tuple:
    player_moved = False
    print("Your turn")
    bounds = st.dimensions
    while player_moved == False:
        
        column = int(input("Enter Row:\n"))
        row = int(input("Enter Column:\n"))
        if (row, column) > bounds or (column, row) > bounds: #Checks comments are within the board
            return -2, -2
        elif st.grid[column - 1][row - 1] < 1:
            return -1, -1
        print(f"Your move is ({column},{row})")
        player_moved = True
    return column - 1, row - 1

def randomisegrid(height: int, width: int): #Creates random non-binary grid
    grid = []
    for x in range(height):
        gridvals = []
        for x in range(width):
            gridval = random.randint(0, 4)
            gridvals.append(gridval)
        grid.append(gridvals)
    return grid

def playtest():
    grid = randomisegrid(4,4)
    start_state = State(grid=grid)
    print(f"\nStarting grid: \n\n{start_state}")
    agentA = Agent("Jotaro Kujo", start_state.dimensions)
    agentB = Agent("Dio Brando", start_state.dimensions)
    
    play(start_state, agentA, agentB)
    
if __name__ == "__main__": 
    playtest()
