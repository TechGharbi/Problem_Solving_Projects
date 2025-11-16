from dataclasses import dataclass 

@dataclass (frozen=True) # make it imutable and automatically generate __init__, __repr__, __eq__, and __hash__ methods
class Car:
    """
    A car has its attributes such as id_number, direction, position (top-left corner), and size.
    """
    id: str # unique identifier for the car ('A', 'B', 'C', etc.) ('X' for the exit car)
    dir: str # 'h' for horizontal, 'v' for vertical
    row: int 
    col: int 
    size: int # 2 for car, 3 for truck
    
    def __post_init__(self):
        if self.dir not in ['h', 'v']:
            raise ValueError("Direction must be 'h' for horizontal or 'v' for vertical.")
    
    def get_cells_of_car(self) -> list[tuple[int, int]]:
        """
        Get and list all tuple (row, col) of the cells occupied by the car in the matrix. 
        """
        cells = []
        if self.dir == 'h':
            for i in range(self.size):
                cells.append((self.row, self.col + i))

        elif self.dir == 'v':
            for i in range(self.size):
                cells.append((self.row + i, self.col))

        return cells