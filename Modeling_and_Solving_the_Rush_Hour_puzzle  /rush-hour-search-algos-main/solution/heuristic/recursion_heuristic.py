from model.car import Car

def calculate_minimum_unique_cars(path_to_clear: list[tuple[int, int]], moved_car: Car, visited: set[str], 
                            cell_of_cars: dict[tuple[int, int]]) -> tuple[int, set[str]]:
    """
    Calculates the min cost and min cars need to move to clear a path of cells
    """

    if moved_car.id in visited:
        return (int(1e9), set()) # Has a cycle, cars cannot be considered twice

    new_visited = visited.copy()
    new_visited.add(moved_car.id)

    blockers = {}

    # Move to clear the way 
    for cell in path_to_clear:
        row, col = cell

        if not (2 <= row <= 7 and 2 <= col <= 7):
            return (int(1e9), set())

        if cell in cell_of_cars:
            # Blocked situation -> recursion 
            new_blocker = cell_of_cars[cell]
            if new_blocker.id != moved_car.id:
                blockers[new_blocker.id] = new_blocker

    # print(moved_car, blockers)
    result = set() # 1 car = 1 cost
    
    for blocker in blockers.values():
        path_to_clear_set = set(path_to_clear) # Use a set for faster lookups
        
        max_space_1 = 0 # For UP / LEFT
        max_space_2 = 0 # For DOWN / RIGHT

        for cell in blocker.get_cells_of_car():
            if cell in path_to_clear_set:
                if blocker.dir == 'h':
                    # Space needed to move LEFT to clear this cell
                    space_left = (blocker.col + blocker.size) - cell[1]
                    max_space_1 = max(max_space_1, space_left)

                    space_right = (cell[1] + 1) - blocker.col
                    max_space_2 = max(max_space_2, space_right)

                else: # 'v'
                    space_up = (blocker.row + blocker.size) - cell[0]
                    max_space_1 = max(max_space_1, space_up)

                    space_down = (cell[0] + 1) - blocker.row
                    max_space_2 = max(max_space_2, space_down)
        
        cost_1, moved_cars_1 = (int(1e9), set())
        cost_2, moved_cars_2 = (int(1e9), set())

        if blocker.dir == 'h':
            if max_space_1 > 0: # If a left move is needed
                path_left = [(blocker.row, blocker.col - i) for i in range(1, max_space_1 + 1)]
                cost_1, moved_cars_1 = calculate_minimum_unique_cars(path_left, blocker, new_visited, cell_of_cars)

            if max_space_2 > 0: # If a right move is needed
                path_right = [(blocker.row, blocker.col + blocker.size - 1 + i) for i in range(1, max_space_2 + 1)]
                cost_2, moved_cars_2 = calculate_minimum_unique_cars(path_right, blocker, new_visited, cell_of_cars)

        else: # 'v'
            if max_space_1 > 0: # If an UP move is needed
                path_up = [(blocker.row - i, blocker.col) for i in range(1, max_space_1 + 1)]
                cost_1, moved_cars_1 = calculate_minimum_unique_cars(path_up, blocker, new_visited, cell_of_cars)

            if max_space_2 > 0: # If a DOWN move is needed
                path_down = [(blocker.row + blocker.size - 1 + i, blocker.col) for i in range(1, max_space_2 + 1)]
                cost_2, moved_cars_2 = calculate_minimum_unique_cars(path_down, blocker, new_visited, cell_of_cars)

        if cost_1 <= cost_2:
            result.update(moved_cars_1)
        else:
            result.update(moved_cars_2)
        
        if cost_1 != int(1e9) or cost_2 != int(1e9):
            result.add(blocker.id)
        
    return (len(result), result)

def evaluate_recursion_heuristic(cars: list[Car]) -> int: 
    """
    Recursively counts the minimum number of unique cars need to move out of the goal car to clear the way to exit gate 
    """
    for car in cars:
        if car.id == 'G':
            goal_car = car 
            break 

    if goal_car is None:
        raise ValueError("Goal car not found in the node.")
    
    cell_of_cars = {}

    for car in cars:
        cells = car.get_cells_of_car()
        for cell in cells:
            cell_of_cars[cell] = car

    path_exit = []
    for col in range(goal_car.col + goal_car.size, 8):
        path_exit.append((goal_car.row, col))

    cost_exit, moved_exit = calculate_minimum_unique_cars(path_exit, goal_car, set(), cell_of_cars)

    if cost_exit == int(1e9):
        return int(1e9)
        
    return cost_exit