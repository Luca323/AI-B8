"""
Hinger Project
Coursework 001: CMP-6058A Artificial Intelligence

Creation of Agent class and decision-making algorithms

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
        # Reward any move that increases regions (a "winning" hinger move)
        if st.numRegions() != parent_reg:
            return inf

        # Count all active (non-zero) cells
        active_cells = sum(
            1 for i in range(st.dimensions[0]) 
            for j in range(st.dimensions[1]) 
            if st.grid[i][j] > 0
        )

        # Use the true number of hingers from the State class
        potential_hingers = st.num_Hingers()

        # Fewer active cells = better; more hingers = much better
        return -active_cells + (10 * potential_hingers)

   
    
    
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
        moves = list(start_state.moves())
        
        if not moves:
            return None

        
        total_scores = [0.0 for _ in moves]
        visit_counts = [0 for _ in moves]
        max_depth = 10

        while time.time() - start_time < time_limit:
            
            idx = random.randrange(len(moves))
            move = moves[idx]

            
            current = move
            depth = 0
            while depth < max_depth:
                next_moves = list(current.moves())
                if not next_moves:
                    break

                # Prefer moves that don’t increase regions 
                safe_moves = [m for m in next_moves if m.numRegions() <= s_regions]
                current = random.choice(safe_moves if safe_moves else next_moves)
                depth += 1

           
            reward = self.evaluate(current, s_regions)

            
            total_scores[idx] += reward
            visit_counts[idx] += 1

        # Pick move with best average reward
        best_move, best_avg = None, -inf
        for i, move in enumerate(moves):
            if visit_counts[i] > 0:
                avg_score = total_scores[i] / visit_counts[i]
                if avg_score > best_avg:
                    best_avg = avg_score
                    best_move = move

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
                return self.mcts(st) 
            
        return best_move



    def win(self, st: State, parent_reg=None) -> bool:
        if parent_reg is None:
            return False
        
        return st.numRegions() > parent_reg
    
# --- Tester ---
def agent_tester():
    grid = [[2, 4, 3, 1],
            [1, 5, 2, 0],
            [1, 2, 1, 2],
            [1, 0, 1, 2]]
    sa = State(grid)
    r = sa.numRegions()

    print(sa, f"\nNum of Hingers: {sa.num_Hingers()}")

    agent = Agent("Bobby", sa.dimensions)

    # Change the mode to test the different functions
    bm = agent.move(sa, mode='minimax')
    c = 1

    while True:
        if sa and not agent.win(sa, r):
            bm = agent.move(sa, mode='minimax')
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

# def test_mcts():
#     print("\n=== MCTS FULL GAME TEST ===")

#     grid = [
#         [3, 1, 2, 2],
#         [1, 3, 1, 4],
#         [2, 1, 2, 1],
#         [1, 2, 3, 2]
#     ]

#     sa = State(grid)
#     agent = Agent("Monte Carlo Bobby", sa.dimensions)

#     print("\nInitial State:\n", sa)
#     print(f"Regions: {sa.numRegions()} | Hingers: {sa.num_Hingers()}\n")

#     move_counter = 0
#     max_moves = 50  # safety cutoff

#     while sa.numRegions() < 2 and move_counter < max_moves:
#         move_counter += 1
#         print(f"\n--- Move {move_counter} ---")

#         best_move = agent.mcts(sa, time_limit=1.0)
#         if not best_move:
#             print("No valid move found.")
#             break

#         sa = best_move  # apply move
#         print("After Move", move_counter, ":\n", sa)
#         print(f"Regions: {sa.numRegions()} | Hingers: {sa.num_Hingers()}")

#     if sa.numRegions() > 1:
#         print("\n Winning state found")
#     else:
#         print("\nNo win found.")

#     print("\n=== MCTS TEST END ===")

# if __name__ == "__main__":
#    test_mcts()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

