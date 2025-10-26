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
     
        
    def alphabeta(self, st: State, depth: int, alpha: int, beta: int, maximising: bool, parent_reg=None) -> tuple:
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
                 eval_score ,_ = self.alphabeta(nxt_st, depth-1, alpha, beta, False, r)
                 
                 if eval_score > max_eval:
                     max_eval, best_state = eval_score, nxt_st
                     
                 alpha = max(alpha, eval_score)
                 if beta <= alpha:
                     break
                     
             return max_eval, best_state
         
         else:
             min_eval = inf
             for nxt_st in st.moves():
                 eval_score ,_ = self.alphabeta(nxt_st, depth-1, alpha, beta, True, r)
                 
                 if eval_score < min_eval:
                     min_eval, best_state = eval_score, nxt_st
                
                 beta = min(eval_score, beta)
                 if beta <= alpha:
                     break
                 
             return min_eval, best_state
         
    # ------------------------
    # MONTE CARLO TREE SEARCH 
    # ------------------------
    def mcts(self, st: State, time_limit=2.0) -> State:
        """
        Monte Carlo Tree Search (MCTS)
        This algorithm simulates many possible future moves within a time limit
        and uses the evaluation function as a quick way to measure how good each path is.
        """

        class Node:
            def __init__(self, state, parent=None):
                self.state = state
                self.parent = parent
                self.children = []
                self.visits = 0
                self.value = 0.0

        def select(node):
            """Select best child using UCB1 (explore/exploit balance)."""
            best, best_score = None, -inf
            for child in node.children:
                exploit = child.value / (child.visits + 1e-6)
                explore = sqrt(log(node.visits + 1) / (child.visits + 1e-6))
                score = exploit + 1.4 * explore
                if score > best_score:
                    best_score = score
                    best = child
            return best

        def expand(node, s_regions):
            """Add one new child (unexplored move)."""
            for nxt in node.state.moves():
                if nxt.numRegions() > s_regions:
                    continue
                if all(child.state != nxt for child in node.children):
                    new_child = Node(nxt, node)
                    node.children.append(new_child)
                    return new_child
            return None

        def simulate(state, parent_reg):
            """Quick evaluation instead of random rollout."""
            return self.evaluate(state, parent_reg)

        def backpropagate(node, reward):
            while node:
                node.visits += 1
                node.value += reward
                node = node.parent

        def best_child(node):
            if not node.children:
                return None
            return max(node.children, key=lambda c: c.visits)

        # --- Main MCTS Loop ---
        root = Node(st)
        s_regions = st.numRegions()
        start_time = time.time()
        iterations = 0

        while time.time() - start_time < time_limit:
            node = root

            # 1. Selection
            while node.children:
                node = select(node)

            # 2. Expansion
            child = expand(node, s_regions)
            if child:
                node = child

            # 3. Simulation (evaluate state quality)
            reward = simulate(node.state, s_regions)

            # 4. Backpropagation
            backpropagate(node, reward)
            iterations += 1

        print(f"[MCTS] {iterations} simulations completed.")
        best = best_child(root)
        return best.state if best else None
            
            
    def move(self, st: State, mode='alphabeta') -> State: #Alpha-Beta used as primary strategy as it has better performance
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
                    score,_ = self.alphabeta(m, depth=3, alpha= -inf, beta=inf, maximising=False, parent_reg=parent_reg)
                    if score > best_score:
                        best_score = score
                        best_move = m
            
            if mode == 'minimax':
                for m in moves:
                    score,_ = self.minimax(m, depth=3, maximising=False, parent_reg=parent_reg)
                    if score > best_score:
                        best_score = score
                        best_move = m
            
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
        else:
            print("Winning State", f"in {c} moves")
            break

        print(f"\nBest Move ({c}):\n", bm)


if __name__ == "__main__":
    agent_tester()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

