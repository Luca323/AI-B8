"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""
from a1_state import State
from math import inf, sqrt, log
import random
import time

class Agent:
    def __init__(self, name: str,  size: tuple):
        self.name = name
        self.size = size
        self.modes = ['alphabeta', 'minimax']
        
    def __str__(self):
        return f"Agent {self.name}"
    
    def evaluate(self, st: State, parent_reg: int) -> int:
        #winning move
        if st.numRegions() != parent_reg:
            return inf
    
        active_cells = 0
        potential_hingers = 0
    
        for i in range(st.dimensions[0]):
            for j in range(st.dimensions[1]):
                val = st.grid[i][j]
                if val > 0:
                    active_cells += 1
                    if val == 1:  # hinger cell identification
                        potential_hingers += 1
    
        #fewer active cells = better, more hingers = more opportunities
        return -active_cells + (5 * potential_hingers) 
   
    
    
    def is_terminal(self, st: State, parent_reg=None) -> bool:
        if parent_reg is not None:
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
     
    def alphabeta(self, st: State, depth: int, alpha: float, beta: float, maximising: bool, parent_reg=None) -> tuple:
        r = st.numRegions()
    
        # terminal or depth limit
        effective_parent = r if parent_reg is None else parent_reg
        if depth == 0 or self.is_terminal(st, effective_parent):
            score = self.evaluate(st, effective_parent)
            return score, st
    
        best_state = None
    
        if maximising:
            max_eval = -inf
            for nxt_st in st.moves():
                eval_score, _ = self.alphabeta(nxt_st, depth-1, alpha, beta, False, r)
    
                if eval_score > max_eval:
                    max_eval, best_state = eval_score, nxt_st
    
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # prune
    
            return max_eval, best_state
    
        else:  # minimising player
            min_eval = inf
            for nxt_st in st.moves():
                eval_score, _ = self.alphabeta(nxt_st, depth-1, alpha, beta, True, r)
    
                if eval_score < min_eval:
                    min_eval, best_state = eval_score, nxt_st
    
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # prune
    
            return min_eval, best_state
         
    def mcts(self, start_state: State, time_limit=2.0) -> State:

        start_time = time.time()
        s_regions = start_state.numRegions()
        moves = []

        for m in start_state.moves():
            moves.append(m)
        
        if not moves:
            return None  

        total_scores = {id(m): 0 for m in moves}
        visit_counts = {id(m): 0 for m in moves}

        #runs simulations until the time limit expires
        while time.time() - start_time < time_limit:
            
            #random start point
            move = random.choice(moves)

            #Simulate a random playout from this move
            current = move
            depth = 0
            max_depth = 10  #limit rollout length to avoid infinite loops

            while depth < max_depth:
                next_moves = list(current.moves())
                if not next_moves:
                    break

                safe_moves = [m for m in next_moves if m.numRegions() <= s_regions]
                if not safe_moves:
                    safe_moves = next_moves  #explore unsafe moves too
                current = random.choice(safe_moves)

                current = random.choice(safe_moves)
                depth += 1

            reward = self.evaluate(current, s_regions)

            total_scores[id(move)] += reward
            visit_counts[id(move)] += 1 #record state and score

        #choose move with highest average score
        best_move, best_avg = None, -inf
        for m in moves:
            if visit_counts[id(m)] > 0:
                avg_score = total_scores[id(m)] / visit_counts[id(m)]
                if avg_score > best_avg:
                    best_avg = avg_score
                    best_move = m

        return best_move
                
                
    def move(self, st: State, mode='alphabeta') -> State: #Alpha-Beta used as primary strategy as it has best performance
        moves = []
        best_move = None
        best_score = -inf
        
        for m in st.moves():
            moves.append(m)
        
        if len(moves) > 0:
        
            #Cache all available moves
            parent_reg = st.numRegions()
            
            if mode == 'alphabeta':
                for m in moves:
                    score,_ = self.alphabeta(m, depth=4, alpha= -inf, beta=inf, maximising=False, parent_reg=parent_reg)
                    if score > best_score:
                        best_score = score
                        best_move = m
            
            if mode == 'minimax':
                for m in moves:
                    score,_ = self.minimax(m, depth=3, maximising=False, parent_reg=parent_reg)
                    if score > best_score:
                        best_score = score
                        best_move = m
                        
            if mode == 'mcts':
                return self.mcts(st) #MCTS function works slightly differently
            
        return best_move



    def win(self, st: State, parent_reg=None) -> bool:
        if parent_reg is None:
            return False
        
        return st.numRegions() > parent_reg
    
# --- Tester ---
def agent_tester():
    grid = [[1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]]
    sa = State(grid)
    r = sa.numRegions()

    print(sa, f"\nNum of Hingers: {sa.num_Hingers()}")

    agent = Agent("Monte Carlo Bobby", sa.dimensions)
    bm = agent.move(sa, mode='mcts')
    c = 1

    while True:
        if sa and not agent.win(sa, r):
            bm = agent.move(sa, mode='mcts')
            sa = bm
            c += 1
        elif agent.win(sa, r):
            print("Winning State", f"in {c} moves")
            break
        else:
            print(f"Finish in {c} moves")

        print(f"\nBest Move ({c}):\n", bm)


if __name__ == "__main__":
    agent_tester()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

