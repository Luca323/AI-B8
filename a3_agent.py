"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""
from a1_state import State
from a2_path import *

class Agent:
    def __init__(self, name: str,  size: tuple):
        self.name = name
        self.size = size
        self.modes = ['alphabeta', 'minimax']
        
    def __str__(self):
        return f"Agent {self.name}"
    
    def move(self, st: State, mode=None) -> State:
        moves = []
        for m in st.moves():
            moves.append(m) #Cache all available moves
            
        if len(moves) > 0:
            
            if not mode:
                return moves[0] #Makes first available move
            
            if mode == 'alphabeta':
                pass
            
            if mode == 'minimax':
                pass
            
        return None
    
    
    
    def win(self, st: State) -> bool:
        if st.num_Hingers() > 0: #If a hinger cell is available, then the game can be won in one move
            
            return True
        
        return False
