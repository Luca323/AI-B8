"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""

from a1_state import State

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
            if not already_visited:
                # For now, treat all states as safe (no hinger logic yet)
                result = dfs(next_state, path + [next_state])
                if result is not None:
                    return result
        return None

    return dfs(start, [])


# --- Tester ---
def tester():
    print("Running path_DFS tester...\n")
    start_grid = [
        [1, 1, 0],
        [2, 0, 1],
        [0, 1, 1]
    ]

    end_grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    start = State(start_grid)
    end = State(end_grid)

    path = path_DFS(start, end)

    if path is None:
        print("No path found.")
    else:
        print(f"Path found with {len(path)} steps:\n")
        for i, step in enumerate(path):
            print(f"Step {i+1}:\n{step}\n")


if __name__ == "__main__":
    tester()
