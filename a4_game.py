"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""
from a1_state import State
from a3_agent import Agent
import time
import sys

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
        player_play = True
    
    
    while True:
        if player_play:
            if player_turn:
                current_agent = player
                player_move = playermove(st)
                if player_move == (-1, -1):
                    print("Illegal move. Cannot remove from a 0. You lose.")
                    print(f"{agentA.name} wins the game.")
                    return
                else:
                    row, column = player_move
                    next_state = st.move((row, column))
            else:
                current_agent = agentA
                next_state = current_agent.move(st)
            print(f"{current_agent.name}'s move:\n" + str(next_state))
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
    while player_moved == False:
        row = int(input("Enter Column:\n"))
        column = int(input("Enter Row:\n"))
        if st.grid[row - 1][column - 1] < 1:
            return -1, -1
        
        print(f"Your move is ({row}), ({column})")
        player_moved = True
    return column - 1, row - 1



def playtest():
    grid = [[1,3,1,1],[1,0,2,1],[1,1,1,3],[4,1,1,1]]
    start_state = State(grid=grid)
    
    agentA = Agent("Jotaro Kujo", start_state.dimensions)
    agentB = Agent("Dio Brando", start_state.dimensions)
    
    play(start_state, agentA, agentB)
    
if __name__ == "__main__":
    playtest()
