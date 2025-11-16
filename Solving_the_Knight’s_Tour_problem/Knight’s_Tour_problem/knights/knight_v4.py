class CSP:
    def __init__(self, variables, domains, constraints, size):
        self.variables = variables  # List of variables (positions on the board)
        self.domains = domains  # Dictionary mapping variables to their domains
        self.constraints = constraints  # Dictionary mapping variable pairs to constraints
        self.size = size  # Chessboard size

    def get_arcs(self):
        """Return all arcs in the CSP as pairs of variables."""
        arcs = []
        for (var1, var2) in self.constraints.keys():
            arcs.append((var1, var2))
        return arcs


class Knight:
    def __init__(self, size):
        self.size = size
        self.position = (0, 0)  # Start position at the top-left corner
        self.assignment = []  # List of moves (sequence of directions)
        self.path = [self.position]  # Path of visited positions

    def move_forward(self, position):
        """Move to the given position and update the path."""
        self.position = position
        self.path.append(position)

    def move_backward(self):
        """Revert to the previous position."""
        self.path.pop()
        self.position = self.path[-1]

    def consistent(self, position):
        """Check if a position is valid (within bounds and not visited)."""
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


def ac_3(csp):
    """AC-3 algorithm to enforce arc consistency."""
    agenda = csp.get_arcs()
    while agenda:
        (xi, xj) = agenda.pop(0)
        if revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False 
            for xk in [neighbor for neighbor in csp.variables if neighbor != xj]:
                agenda.append((xk, xi))
    return True


def revise(csp, xi, xj):
    """Revise the domain of xi by removing inconsistent values."""
    revised = False
    to_remove = []
    for vi in csp.domains[xi]:
        satisfies_constraint = any(
            csp.constraints.get((xi, xj), lambda a, b: True)(vi, vj)
            for vj in csp.domains[xj]
        )
        if not satisfies_constraint:
            to_remove.append(vi)
    for vi in to_remove:
        csp.domains[xi].remove(vi)
        revised = True
    return revised


def backtracking(assignment, csp):
    """Recursive backtracking algorithm to find a solution."""
    # Base case: All positions are visited
    if len(assignment.path) == csp.size ** 2:
        return assignment  # Return the completed assignment

    var = assignment.position  # Current position of the knight
    # Try each move, prioritizing those with fewer subsequent options
    for move in sorted(knight_moves(var, csp.size), key=lambda m: len(knight_moves(m, csp.size))):
        if assignment.consistent(move):  # Check if move is consistent
            assignment.move_forward(move)  # Make the move
            result = backtracking(assignment, csp)  # Recursive call
            if result:  # If solution is found, return it
                return result
            assignment.move_backward()  # Backtrack if the move leads to failure

    return None  # Return None if no valid moves are found


def main():
    size = 8  # Chessboard size
    variables = [(x, y) for x in range(size) for y in range(size)]
    domains = {var: knight_moves(var, size) for var in variables}
    constraints = {}

    # Define constraints for all pairs of variables
    for xi in variables:
        for xj in knight_moves(xi, size):
            constraints[(xi, xj)] = lambda vi, vj: vj in knight_moves(vi, size)

    csp = CSP(variables, domains, constraints, size)
    knight = Knight(size)

    print("Applying AC-3 preprocessing...")
    if ac_3(csp):
        print("Preprocessing complete. Proceeding with backtracking...")
        solution = backtracking(knight, csp)
        if solution:
            print("Solution found:")
            print("Assignment (sequence of moves):", solution.assignment)
            print("Path (visited positions):", solution.path)
        else:
            print("No solution found during backtracking.")
    else:
        print("No solution found during preprocessing.")


if __name__ == "__main__":
    main()
