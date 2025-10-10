"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""
from a1_state import State
from a3_agent import Agent

def play(st: State, agentA: Agent, agentB: Agent)->None:
    player1 = True
    player2 = False
    
    
    while True:
        
        if agentA.win(st, isMove=player1):
            st = agentA.move(st)
            print(agentA.name,"'s move: \n", st)
            print(f"Game Over, player {agentA.name} Wins!")
            return
        elif agentB.win(st, isMove=player2):
            st = agentB.move(st)
            print(agentB.name,"'s move: \n", st)
            print(f"Game Over, player {agentB.name} Wins!")
            return
        
        if player1:
            st = agentA.move(st)
            print(agentA.name,"'s move: \n", st)
            
            player1 = False
            player2 = True
            
        elif player2:
            st = agentB.move(st)
            print(agentB.name,"'s move: \n", st)
            
            player1 = True
            player2 = False
            
        
def playtest():
    grid = [[1,3,1,1],[1,4,2,1],[1,1,1,3],[4,1,1,1]]
    start_state = State(grid=grid)
    
    agentA = Agent("Jotaro Kujo", start_state.dimensions)
    agentB = Agent("Dio Brando", start_state.dimensions)
    
    play(start_state, agentA, agentB)
    
if __name__ == "__main__":
    playtest()
