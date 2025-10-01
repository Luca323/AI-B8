class State:
    def __init__(self, grid):
        self.grid = grid
        
    def __str__(self):
        return "\n".join(" ".join(str(x) for x in row) for row in self.grid)
    
examp = [[0,0,1,2], [1, 1, 2,0], [0, 2, 0, 1]]

s = State(examp)
print(s)