class State:
    def __init__(self, grid):
        self.grid = grid
        self.dimensions = (len(grid),len(grid[0])) #Records dimension of grid
        
    def __str__(self) -> str:
        return f"Dimensions: {self.dimensions}\n" + "\n\n".join("   ".join(str(x) for x in row) for row in self.grid)
    
    def clone(self) -> 'State': #To create a deep copy of state
        copy = [[self.grid[i][j] for j in range(self.dimensions[1])]
                 for i in range(self.dimensions[0])]
        return State(copy)
    
    def move(self, pos: list) -> 'State':
        assert(len(pos)==2)
        i,j = pos[0],pos[1]
        st = self.clone()
        
        if st.grid[i][j] != 0:
            st.grid[i][j]-=1  
            
            return st
        
        return None
    '''
    def moves(self):
         rows, cols = self.dimensions
         for i in range(rows):
             for j in range(cols):
                 new_state = self.move([i, j])
                 if new_state is not None:
                     yield new_state
         '''            
         
    def moves(self) -> 'State': #Yields all available moves 
        for i in range (self.dimensions[0]): 
            for j in range(self.dimensions[1]): 
                next_st = self.move([i, j])
                if next_st:
                    yield next_st
    

    
examp = [[0,0,1,2], [0, 0, 2,0], [0, 2, 0, 1]]

test = []

s = State(grid=examp)

test.append(s.moves)
for m in s.moves():
    print(m, "\n")