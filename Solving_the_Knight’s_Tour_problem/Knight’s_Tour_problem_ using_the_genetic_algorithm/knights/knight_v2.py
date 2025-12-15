from animation import animate

class Knight:
    def __init__(self):
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
            0 <= x < 8 and 0 <= y < 8 and position not in self.path
        )

def knight_moves(position, size=8):
    x, y = position
    moves = [
        (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
        (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)
    ]
    return [(nx, ny) for nx, ny in moves if 0 <= nx < size and 0 <= ny < size]

def count_moves(position):
    return len(knight_moves(position))

def backtracking(assignment):
    if len(assignment.path) == 64:
        return assignment 
    var = assignment.position
    for move in sorted(knight_moves(var),key=count_moves):
        if assignment.consistent(move): 
            assignment.move_forward(move)
            result = backtracking(assignment)
            if result: 
                return result
            assignment.move_backward() 
    return None 

def run_backtracking():
    knight = Knight()
    solution = backtracking(knight)
    return solution.path   
