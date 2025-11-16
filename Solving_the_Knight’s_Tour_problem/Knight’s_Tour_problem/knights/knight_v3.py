
class Knight:
    def __init__(self, size=8):
        self.size = size
        self.position = (0, 0)
        self.assignment = []  
        self.path = [self.position]  

    def move_forward(self, position):
        
        self.position = position
        self.path.append(position)

    def move_backward(self):
       
        self.path.pop()
        self.position = self.path[-1]

    def consistent(self, position):
        
        x, y = position
        return (
            0 <= x < self.size and 0 <= y < self.size and position not in self.path
        )


def knight_moves(position, size):
    """Generate all valid knight moves from a given position."""
    x, y = position
    moves = [
        (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
        (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)
    ]
    return [(nx, ny) for nx, ny in moves if 0 <= nx < size and 0 <= ny < size]



def backtracking(assignment):
    if len(assignment.path) == 64:
        return assignment  
    var = assignment.position 
    for move in sorted(knight_moves(var, 8), key=lambda m: len(knight_moves(m, 8))):
        if assignment.consistent(move): 
            assignment.move_forward(move)  
            result = backtracking(assignment)
            if result:  
                return result
            assignment.move_backward() 
    return None  

def main():
    
    knight = Knight()
    print("Applying AC-3 preprocessing...")
    solution = backtracking(knight)  
    print("Solution found:")      
    print("Path (visited positions):", solution.path)
        

if __name__ == "__main__":
    main()
