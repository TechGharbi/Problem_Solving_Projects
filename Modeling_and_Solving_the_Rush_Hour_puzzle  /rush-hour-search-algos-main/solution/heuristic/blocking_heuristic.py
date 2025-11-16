from model.car import Car

def evaluate_blocking_heuristic(cars: list[Car]) -> int:
    for car in cars:
        if car.id == 'G':
            goal_car = car 
            
    if goal_car is None:
        raise ValueError("Goal car not found in the node.")
    
    blockers = 0
    cell_of_cars = {}

    for car in cars:
        cells = car.get_cells_of_car()
        for cell in cells:
            cell_of_cars[cell] = car

    for col in range(goal_car.col + goal_car.size, 8):
        cell = (goal_car.row, col)      
        if cell in cell_of_cars:    
            blockers += 1
    
    return blockers 
    
