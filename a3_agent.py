"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""
from a1_state import State

class Agent:
    def __init__(self, name: str,  size: tuple):
        self.name = name
        self.size = size
        
    def __str__(self):
        return f"Agent {self.name}"
    
    def move(self, st: State, mode=None) -> State:
        moves = []
        for m in st.moves():
            moves.append(m) #Cache all available moves
            
        if len(moves) > 0:
            
            if mode == None:
                return moves[0] #Makes first available move
            
        return None