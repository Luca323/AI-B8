"""
Hinger Project
Coursework 001: CMP-6058A Artificial Intelligence

Collection and comparison of pathfinding algorithms

@Authors: B8 (100415489, 100426892, 100437079)
"""

from a1_state import State
from collections import deque
import heapq
import itertools
import time


def path_DFS(start, end):
    visited = []
    s_regions = start.numRegions()

    def dfs(current, path):
    
        if current == end: #Base Case
            return path

        visited.append(current)

        #Expand open moves
        for next_state in current.moves():
            #Check if we've already seen this grid
            if next_state.numRegions() > s_regions:
                continue
            already_visited = any(next_state == v for v in visited)
            if not already_visited:
                result = dfs(next_state, path + [next_state])
                if result is not None:
                    return result
        return None

    return dfs(start, [])


def path_BFS(start: State, end: State): 
    queue = deque([(start, [start])])
    closed = [start]
    start_regions = start.numRegions()
    
    while queue:
        current, path = queue.popleft()
        
        if current == end:
            return path
        
        
        for nxt_st in current.moves():
            if nxt_st.numRegions() > start_regions:
                continue #Ignores any unsafe moves i.e taking hinger cells
            
            if all(nxt_st != v for v in closed):
                closed.append(nxt_st)
                queue.append((nxt_st, path + [nxt_st]))
                
    return None
            

def path_IDDFS(start, end, max_depth=20):
    s_regions = start.numRegions()

    #Inner recursive DFS with depth limit
    def dfs_limited(current, end, path, depth):
        if current == end:
            return path
        if depth == 0:
            return None

        for next_state in current.moves():
            
            if next_state.numRegions() > s_regions: 
                continue #Disallows unsafe moves

            if not any(next_state == p for p in path):
                #Safe-state check could go here once numHinges() is ready
                result = dfs_limited(next_state, end, path + [next_state], depth - 1)
                if result is not None:
                    return result
        return None

    #Iteratively increase the allowed search depth
    for limit in range(1, max_depth + 1):
        result = dfs_limited(start, end, [start], limit)
        if result is not None:

            return result

    print("No path found within the maximum depth limit.")
    return None


'''
A* Algorithm 

The heurisitc within A* estimates how far the current state is from the goal
It does so by counting how many cells are different between them


It essentially guesses how many changes are needed to reach the goal
This helps the algorithm focus on states that are closer to the goal instead of exploring randomly
This makes the search faster and more efficient without sacrificing efficiency
'''

def path_astar(start, end):
    
    s_regions = start.numRegions()  #number of regions in the start state

    prioqueue = []
    counter = itertools.count()  # unique sequence count for tie-breaking
    heapq.heappush(prioqueue, (0, next(counter), 0, start, [start]))
    visited = [start]

    #Heuristic: count how many cells differ between two grids
    def heuristic(a, b):
        return sum(
            cell_a != cell_b
            for row_a, row_b in zip(a.grid, b.grid)
            for cell_a, cell_b in zip(row_a, row_b)
        )

    while prioqueue:
        f_score, _, g_score, current, path = heapq.heappop(prioqueue)

        if current == end:
            return path

        for next_state in current.moves():
            if next_state.numRegions() > s_regions:
                continue

            if any(next_state == v for v in visited):
                continue

            new_g = g_score + 1
            h = heuristic(next_state, end)

            f = new_g + h
            visited.append(next_state)
            heapq.heappush(prioqueue, (f, next(counter), new_g, next_state, path + [next_state]))

    return None

def compare(start, end, bfs_fn, dfs_fn, iddfs_fn, astar_fn, max_depth=20):
    
    algorithms = {
        "BFS": bfs_fn,
        "DFS": dfs_fn,
        "IDDFS": lambda s, e: iddfs_fn(s, e, max_depth=max_depth),
        "A*": astar_fn
    }
    
    results = []

    for name, fn in algorithms.items():
        start_time = time.time()
        path = fn(start, end)
        end_time = time.time()
        
        runtime = end_time - start_time
        correctness = path is not None
        
        path_length = len(path) if path else None
        
        results.append({
            "Algorithm": name,
            "Correct": correctness,
            "Runtime (s)": round(runtime, 6),
            "Path Length": path_length
        })
    
    #print results in a readable table
    print("{:<10} {:<10} {:<12} {:<12}".format("Algorithm", "Correct", "Runtime (s)", "Path Length"))
    print("-" * 46)
    for r in results:
        print("{:<10} {:<10} {:<12} {:<12}".format(
            r["Algorithm"], str(r["Correct"]), r["Runtime (s)"], str(r["Path Length"])
        ))

    def min_safe(start, end):
        
        return None
    

'''
We used Dijkstra's algorithm for min safe

The reason we use Dijkstra's algorithm is because we need to find a SAFE path with LOWEST total cost
Unlike other algorithms (BFS and DFS etc.) that minimise the steps, Dijkstra's minimises the total move cost
 
Essentially, Dijkstra's will return the cheapest overall path

Since each move in hinger can have a different cost (for example, reducing a higher number may cost more);
Dijkstra's is the most efficient and reliable choice
It expands paths in order of their total cost, guaranteeing the minimal- cost safe path if one exists
 
'''
def min_safe(start, end):
    s_regions = start.numRegions()
    
    #Priority queue stores (total_cost, counter, state, path)
    prioqueue = []
    counter = itertools.count()
    heapq.heappush(prioqueue, (0, next(counter), start, [start]))

    visited = []

    while prioqueue:
        total_cost, _, current, path = heapq.heappop(prioqueue)

        if current == end:
            return path

        if any(current == v[0] and total_cost >= v[1] for v in visited):
            continue #Ignore if the state has already been visited with lower cost
            
        visited.append((current, total_cost))

        for next_state in current.moves():
            
            #skip unsafe moves (those that increase the number of regions)
            if next_state.numRegions() > s_regions:
                continue

            move_cost = 1  #each move costs 1 step
            new_cost = total_cost + move_cost

            #push if we haven’t found a cheaper way to reach this state
            if not any(next_state == v[0] and new_cost >= v[1] for v in visited):
                heapq.heappush(prioqueue, (new_cost, next(counter), next_state, path + [next_state]))

    return None

# --- Tester ---
def tester():
    print("Running path tester...\n")
    start_grid = [[1,1,0,0,2],
          [1,1,0,0,0],
          [0,0,1,1,1],
          [0,0,0,1,1]]

    end_grid = [[0,0,0,0,0],
          [0,0,0,0,0],
          [0,0,0,0,1],
          [0,0,0,1,1]]

    start = State(start_grid)
    end = State(end_grid)

    print("DFS Path:")
    path = path_DFS(start, end)
    for i, step in enumerate(path):
        print(f"Step {i+1}:\n{step}\n")
    
    print("BFS Path: ")
    path = path_BFS(start, end)
    for i, step in enumerate(path):
        print(f"Step {i+1}:\n{step}\n")
    
    print("A* Path: ")
    path = path_astar(start, end)
    for i, step in enumerate(path):
        print(f"Step {i+1}:\n{step}\n")
        

    path = min_safe(start, end)
    if path:
        print(f"\nMin-safe path found with {len(path)} steps:")
        for i, step in enumerate(path):
            print(f"Step {i+1}:\n{step}\n")
    else:
        print("\nNo safe path found.")
    
    
    compare(start, end, path_BFS, path_DFS, path_IDDFS, path_astar, max_depth=20)



if __name__ == "__main__":
    tester()
