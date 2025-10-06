"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""

class State:
    def __init__(self, grid):
        self.grid = grid
        self.dimensions = (len(grid),len(grid[0])) #Records dimension of grid
        
    def __eq__(self, o):
        if self.grid == o.grid:
            return True
        
        
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
    
         
    def moves(self) -> 'State': #Yields all available moves 
        for i in range (self.dimensions[0]): 
            for j in range(self.dimensions[1]): 
                next_st = self.move([i, j])
                if next_st:
                    yield next_st
                    
                    
    def numRegions(self) -> int: #detects clusters
        coords = [(i, j)
              for i in range(self.dimensions[0])
              for j in range(self.dimensions[1])
              if self.grid[i][j] != 0] #Collect coords of all points

        if not coords:
            return 0 #Throw 0 if no regions exist
    
        coords = set(coords)
        unvisited = set(coords)
        regions = 0
    
        #all possible neighbor directions
        neighbors = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),(0, 1), (1, -1),  (1, 0), (1, 1)
            ]
    
        while unvisited:
            regions += 1
            #start from one point
            to_check = [unvisited.pop()]
            checked = set(to_check)
    
            i = 0
            while i < len(to_check):
                r, c = to_check[i]
                for dr, dc in neighbors:
                    n = (r + dr, c + dc)
                    if n in unvisited:
                        unvisited.remove(n)
                        to_check.append(n)
                i += 1
    
        return regions
    
    def num_Hingers(self) -> int:
        h = 0
        for s in self.moves():
            if s.numRegions() > self.numRegions()+1:
                h += 1
        return h
    
        

def tester() -> None:    
    examp = [[1,0,1,2], [0, 0, 1,0], [0, 2, 0, 1]]
    
    test = []
    
    s = State(grid=examp)
    print(s, "\n") 
    
    '''
    test.append(s.moves)
    for m in s.moves():
        print(m, "\n")
    '''
    print(f'Number of Regions: {s.numRegions()}')
    print(f'Number of hinger cells: {s.num_Hingers()}')
        
if __name__ == "__main__":
    tester()