"""
Hinger Project
Coursework 001

@Authors: B8 (100415489, 100426892, 100437079)
"""

class State:
    def __init__(self, grid):
        self.grid = grid
        self.dimensions = (len(grid),len(grid[0])) 
        
    def __eq__(self, o):
        if self.grid == o.grid:
            return True
        
    def __str__(self) -> str:
        return "\n\n".join("  ".join(str(x) for x in row) for row in self.grid)
    
    def clone(self) -> 'State': 
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
    
    def moves(self) -> 'State':
        for i in range (self.dimensions[0]): 
            for j in range(self.dimensions[1]): 
                next_st = self.move([i, j])
                if next_st:
                    yield next_st
                    
                    
    def numRegions(self) -> int: 
        coords = [(i, j)
              for i in range(self.dimensions[0])
              for j in range(self.dimensions[1])
              if self.grid[i][j] != 0] 
        if not coords:
            return 0
    
        coords = set(coords)
        unvisited = set(coords) 
        regions = 0
    
        
        neighbors = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),(0, 1), (1, -1),  (1, 0), (1, 1)
            ]
    
        while unvisited: 
            regions += 1

            to_check = [unvisited.pop()]
    
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
            if s.numRegions() > self.numRegions():
                h += 1
        return h 
    
        
def tester() -> None:

    grd = [[1,1,0,0,2],
          [1,1,0,0,0],
          [0,0,1,1,1],
          [0,0,0,1,1]]
    
    sa = State(grid = grd)
    
    print(sa)
    print(f'\nNumber of Regions: {sa.numRegions()} \nNumber of Hinger Cells: {sa.num_Hingers()}')
    
    print("\nAvailable moves:")
    c = 1
    for m in sa.moves():
        print(f"Move {c}:\n" + str(m), "\n\n")
        c+=1
        
        

        
if __name__ == "__main__":
    tester()