class State:
    def __init__(self, grid):
        self.grid = grid
        self.dimensions = (len(grid),len(grid[0])) #Records dimension of grid
        
    def __str__(self) -> str:
        return f"Dimensions: {self.dimensions}\n" + "\n\n".join("   ".join(str(x) for x in row) for row in self.grid)
    
    def move(self, pos: list) -> None:
        assert(len(pos)==2)
        i,j = pos[0],pos[1]
        
        if self.grid[i][j] != 0:
            self.grid[i][j]-=1       
    
    
examp = [[0,0,1,2], [0, 0, 2,0], [0, 2, 0, 1]]

s = State(grid=examp)
s.move([0, 2])
print(s)