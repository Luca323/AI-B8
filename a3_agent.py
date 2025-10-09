"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""
from a1_state import State
from a2_path import *
from math import inf

class Agent:
    def __init__(self, name: str,  size: tuple):
        self.name = name
        self.size = size
        self.modes = ['alphabeta', 'minimax']
        
    def __str__(self):
        return f"Agent {self.name}"
    
    def evaluate(self, st: State, parent_reg: int) -> int:
        if st.numRegions() > parent_reg:
            return 9999 #Adds large bias for taking hinger cells
        
        active_cells = sum(sum(1 for val in row if val != 0) for row in st.grid)
        return active_cells
    
    def is_terminal(self, st: State, parent_reg=None) -> bool:
        if parent_reg:
            return st.numRegions() > parent_reg
        return False
            
    
    def minimax(self, st: State, depth: int, maximising: bool, parent_reg=None) -> tuple:
        r = st.numRegions()
        
        if depth == 0 or self.is_terminal(st, parent_reg):
            if parent_reg:
                score = self.evaluate(st, parent_reg)
            else:
                score = self.evaluate(st, r)
            return score, st
        
        best_state = None
        
        if maximising:
            max_eval = -inf
            for nxt_st in st.moves():
                eval_score ,_ = self.minimax(nxt_st, depth-1, False, r)
                
                if eval_score > max_eval:
                    max_eval, best_state = eval_score, nxt_st
                    
            return max_eval, best_state
        
        else:
            min_eval = inf
            for nxt_st in st.moves():
                eval_score ,_ = self.minimax(nxt_st, depth-1, True, r)
                
                if eval_score < min_eval:
                    min_eval, best_state = eval_score, nxt_st
                    
            return min_eval, best_state
            
            
    def move(self, st: State, mode=None) -> State:
        moves = []
        best_move = None
        best_score = -inf
        
        for m in st.moves():
            moves.append(m) #Cache all available moves
            
        if len(moves) > 0:
            
            if not mode:
                best_move = moves[0] #Makes first available move
            
            if mode == 'alphabeta':
                pass
            
            if mode == 'minimax':
                for m in moves:
                    score,_ = self.minimax(m, depth=3, maximising=False)
                    if score > best_score:
                        best_score = score
                        best_move = m
            
        return best_move
    
    
    
    def win(self, st: State) -> bool:
        if st.num_Hingers() > 0: #If a hinger cell is available, then the game can be won in one move
            
            return True
        
        return False
    
def agent_tester():
    grid = [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
    sa = State(grid)
    
    print(sa,f"\nNum of Hingers: {sa.num_Hingers()}")
    
    
    
    minimax_agent = Agent("mm Tester", sa.dimensions)
    bm = minimax_agent.move(sa, mode='minimax')
    c = 0
    
    while True:
        if not minimax_agent.win(sa):
            bm = minimax_agent.move(sa, mode='minimax') 
            sa = bm
            c +=1
        else:
            bm = "Winning State"
            print(bm, f"in {c} moves")
            break
    
        print("\nBest Move:\n",bm)

if __name__ == "__main__":
    agent_tester()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

