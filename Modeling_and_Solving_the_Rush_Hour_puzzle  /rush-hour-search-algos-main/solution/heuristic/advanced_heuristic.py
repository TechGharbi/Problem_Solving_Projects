from model.car import Car

def calculate_minimum_unique_cars(dir: str, blocker: Car, visited: set[str], 
                            cell_of_cars: dict[tuple[int, int]], space: int) -> int:
    if blocker.id in visited:
        return int(1e9) # Has a cycle, cars cannot be considered twice

    new_visited = visited.copy()
    new_visited.add(blocker.id)

    row, col = blocker.row, blocker.col

    secondary_blockers = set()

    res = 0
    for i in range(1, space + 1):
        # Move to clear the way 
        if dir == "up":
            new_row = row - i
            new_col = col 
        else:
            new_row = (row + blocker.size - 1) + i
            new_col = col 

        if not (2 <= new_row <= 7 and 2 <= new_col <= 7):
            return int(1e9) 

        new_cell = (new_row, new_col)
        
        if new_cell in cell_of_cars:
            secondary_blocker = cell_of_cars[new_cell]
            secondary_blockers.add(secondary_blocker.id)
        
    return len(secondary_blockers)

def evaluate_advanced_heuristic(cars: list[Car]) -> int: 
    """
    Recursively counts the minimum number of unique cars need to move out of the goal car to clear the way to exit gate 
    """
    for car in cars:
        if car.id == 'G':
            goal_car = car 
            break 

    if goal_car is None:
        raise ValueError("Goal car not found in the node.")
    
    minimum_moves = 0 # 1 car = 1 cost
    blockers = 0
    cell_of_cars = {}

    for car in cars:
        cells = car.get_cells_of_car()
        for cell in cells:
            cell_of_cars[cell] = car

    # Try to move the blockers
    for col in range(goal_car.col + goal_car.size, 8):
        cell = (goal_car.row, col)      
        if cell in cell_of_cars:    
            blocker_car = cell_of_cars[cell]
            visited = {goal_car.id} # Check no cycle for the moving blocker 
            
            blockers += 1

            space_up = (blocker_car.row + blocker_car.size) - goal_car.row 
            space_down = (goal_car.row + 1) - blocker_car.row

            cost_down = calculate_minimum_unique_cars("down", blocker_car, visited, cell_of_cars, space_down)
            cost_up = calculate_minimum_unique_cars("up", blocker_car, visited, cell_of_cars, space_up)

            cost_move_blocker = min(cost_up, cost_down)
        
            if cost_move_blocker == int(1e9):
                return 1e9 # Impossible state
            
            minimum_moves += cost_move_blocker

    return blockers + minimum_moves

