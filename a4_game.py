"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""
from a1_state import State
from a3_agent import Agent

def play(st: State, agentA: Agent, agentB: Agent)->None:
    player_turn = True  #True = agentA's turn, False = agentB's turn
    
    while True:
        
        current_agent = agentA if player_turn else agentB
        
        next_state = current_agent.move(st)
        
        #If no more moves are possible, it’s a draw
        if not next_state:
            print("Game Over! It's a draw.")
            return
        
        
        print(f"{current_agent.name}'s move: \n", next_state)
        
        if current_agent.win(next_state):
            print(f"Game Over, player {current_agent.name} Wins!")
            return
        
        
        # Switch turns
        st = next_state
        player_turn = not player_turn
            
        
def playtest():
    grid = [[1,3,1,1],[1,0,2,1],[1,1,1,3],[4,1,1,1]]
    start_state = State(grid=grid)
    
    agentA = Agent("Jotaro Kujo", start_state.dimensions)
    agentB = Agent("Dio Brando", start_state.dimensions)
    
    play(start_state, agentA, agentB)
    
if __name__ == "__main__":
    playtest()
