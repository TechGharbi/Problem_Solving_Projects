from __future__ import annotations # Allows a class to contain type hints that refer to itself. We use Node instead of 'Node'
from model.car import Car

class Node:  
    """
    Un nœud représente un état du jeu Rush Hour.
    Il contient :
      - la position de chaque voiture (liste de Car)
      - l'action qui a mené à cet état
      - le parent (état précédent)
      - les coûts et heuristiques pour les algorithmes de recherche
    """
      
    def __init__(self, rush_hour_puzzle: RushHourPuzzle, action=None, parent=None, cost=0, heuristic=0):
        self.state = rush_hour_puzzle  # Use RushHourPuzzle as state
        self.action = action
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
    
    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.state.board))

    def is_goal(self):
        return self.state.isGoal()

    def __eq__(self, other):
        return self.state.board == other.state.board
    
    def __str__(self) -> str:
        return "\n".join([" ".join(row) for row in self.state])

    def __lt__(self, other: Node) -> bool:
        """
        Compare with another node with f(n) = g(n) + h(n) = cost + heuristic.
        """
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
       
    def get_goal_car(self) -> Car | None:
        for car in self.cars:
            if car.id == 'X':
                return car
        return None 

    def is_valid_move(self, car: Car, name_move: str) -> bool:
        row, col = car.row, car.col 

        if name_move == "left":
            return (col > 2 and self.state[row][col - 1] == '-')
        elif name_move == "right":
            return (col + car.size <= 7 and self.state[row][col + car.size] == '-')
        elif name_move == "up":
            return (row > 2 and self.state[row - 1][col] == '-')
        else: # down
            return (row + car.size <= 7 and self.state[row + car.size][col] == '-')

        return False 
    
    def get_next_possible_moves(self):    
        h_move = [('left', 0, -1), ('right', 0, 1)]  # 'h'
        v_move = [('up', -1, 0), ('down', 1, 0)]     # 'v'
        
        for car in self.cars:
            move = h_move if car.dir == 'h' else v_move

            for name_move, drow, dcol in move:
                if self.is_valid_move(car, name_move):
                    # top-left corner
                    new_row = car.row + drow
                    new_col = car.col + dcol 

                    temp_cars = self.cars.copy()
                    new_car = Car(car.id, car.dir, new_row, new_col, car.size)

                    if car in temp_cars:
                        temp_cars.remove(car)
                        temp_cars.append(new_car)

                    action = f"Move {car.id} {name_move}"
                    yield temp_cars, action, new_car 
