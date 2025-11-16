import copy 

class RushHourPuzzle:
    """
    Represente un état du jeu Rush Hour.
    """
    def __init__(self, filename=None):
        self.board_height = 0
        self.board_width = 0
        self.vehicles = []
        self.walls = []
        self.board = []

    
        if filename:
            self.setVehicles(filename)
            self.setBoard()
    
    def setVehicles(self, filename: str):
    
        with open(filename, 'r') as file:
        # Read board dimensions from first line
            dimensions = file.readline().strip().split(',')
            self.board_width = int(dimensions[0])
            self.board_height = int(dimensions[1])
        
            self.vehicles = []
            for line in file:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 5:
                        vid, x, y, orientation, length = parts
                    # Convert orientation to match your Car class
                        dir_char = 'h' if orientation.upper() == 'H' else 'v'
                    
                        vehicle = car(
                            id=vid,
                            dir=dir_char,
                            row=int(x),  # x becomes row
                            col=int(y),  # y becomes col  
                            size=int(length)
                        )
                        self.vehicles.append(vehicle)
    
    def setBoard(self):
        """Create game board from vehicles and walls"""
        # Initialize empty board
        self.board = [["-" for _ in range(self.board_width)] for _ in range(self.board_height)]
        
        # Add walls if any
        for wall in self.walls:
            x, y = wall
            if 0 <= x < self.board_height and 0 <= y < self.board_width:
                self.board[x][y] = "#"
        
        # Add vehicles
        for vehicle in self.vehicles:
            cells = vehicle.get_cells_of_car()
            for row, col in cells:
                if 0 <= row < self.board_height and 0 <= col < self.board_width:
                    self.board[row][col] = vehicle.id

    def isGoal(self):
        """Check if red car 'X' is at exit position"""
        for vehicle in self.vehicles:
            if vehicle.id == 'X':
                # Exit is at right side, position (board_height//2 - 1, board_width - 1)
                exit_row = self.board_height // 2 - 1
                return vehicle.row == exit_row and vehicle.col + vehicle.size == self.board_width
        return False

    def successorFunction(self):
        """Generate all possible moves"""
        successors = []
      
        for i, v in enumerate(self.vehicles):
            if v.orientation == 'H':#horisental
                # gauche
                if v.x > 0 and self.board[v.y][v.x - 1] == '.':
                    etat_succes = copy.deepcopy(self)
                    etat_succes.vehicles[i].x -= 1
                    etat_succes.setBoard()
                    successors.append(((v.id, 'L'), etat_succes))
                # droite
                if v.x + v.length < self.board_width and self.board[v.y][v.x + v.length] == '.':
                    etat_succes = copy.deepcopy(self)
                    etat_succes.vehicles[i].x += 1
                    etat_succes.setBoard()
                    successors.append(((v.id, 'R'), etat_succes))
            else:  # Vertical
                # haut
                if v.y > 0 and self.board[v.y - 1][v.x] == '.':
                    etat_succes = copy.deepcopy(self)
                    etat_succes.vehicles[i].y -= 1
                    etat_succes.setBoard()
                    successors.append(((v.id, 'U'), etat_succes))
                # bas
                if v.y + v.length < self.board_height and self.board[v.y + v.length][v.x] == '.':
                    etat_succes = copy.deepcopy(self)
                    etat_succes.vehicles[i].y += 1
                    etat_succes.setBoard()
                    successors.append(((v.id, 'D'), etat_succes))
        return successors
