class State:
    def __init__(self, grid):
        self.grid = grid
        m = len(grid)
        n = len(grid[0])
        self.dimensions = (m,n) #Records dimension of grid
        
    def __str__(self):
        return f"Dimensions: {self.dimensions}\n" + "\n\n".join("   ".join(str(x) for x in row) for row in self.grid)
    
examp = [[0,0,1,2], [1, 1, 2,0], [0, 2, 0, 1]]

s = State(examp)
print(s)