"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""

from a1_state import State
from collections import deque
import heapq


# Depth First Search
def path_DFS(start, end):
    visited = []

    def dfs(current, path):
        # Stop if the current state matches the goal
        if current == end:
            return path

        visited.append(current)

        # Expand next moves
        for next_state in current.moves():
            # Check if we've already seen this exact grid
            already_visited = any(next_state == v for v in visited)
            if not already_visited and next_state.numRegions == start.numRegions():
                # For now, treat all states as safe (no hinger logic yet)
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
            
    

# Iterative Deepening Depth First Search
def path_IDDFS(start, end, max_depth=20):

    # Inner recursive DFS with depth limit
    def dfs_limited(current, end, path, depth):
        if current == end:
            return path
        if depth == 0:
            return None

        for next_state in current.moves():
            # avoid cycles by not revisiting states already in current path
            if not any(next_state == p for p in path):
                # safe-state check could go here once numHinges() is ready
                result = dfs_limited(next_state, end, path + [next_state], depth - 1)
                if result is not None:
                    return result
        return None

    # Iteratively increase the allowed search depth
    for limit in range(1, max_depth + 1):
        print(f"Searching with depth limit {limit}...")
        result = dfs_limited(start, end, [start], limit)
        if result is not None:
            print(f"Solution found at depth {limit}.")
            return result

    print("No path found within the maximum depth limit.")
    return None



# A Star Algorithm
def path_astar(start, end):
    
    # Creating a heap of tuples (a priority queue)
    prioqueue = []
    heapq.heappush(prioqueue, (0, 0, start, [start] ))
    
    # Record the best g(n) found for each visited position
    visited = {start: 0}


# --- Tester ---
def tester():
    print("Running path_DFS tester...\n")
    start_grid = [
        [1, 1, 0],
        [2, 0, 1],
        [0, 1, 1]
    ]

    end_grid = [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    start = State(start_grid)
    end = State(end_grid)

    path = path_BFS(start, end)

    if path is None:
        print("No path found.")
    else:
        print(f"Path found with {len(path)} steps:\n")
        for i, step in enumerate(path):
            print(f"Step {i+1}:\n{step}\n")


if __name__ == "__main__":
    tester()
