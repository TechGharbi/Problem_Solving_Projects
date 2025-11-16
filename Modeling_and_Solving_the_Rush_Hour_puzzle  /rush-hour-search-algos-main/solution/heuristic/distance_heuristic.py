from model.car import Car

def evaluate_distance_heuristic(cars: list[Car]) -> int:
    """
    Counts how many number of blocker cars block goal car.
    Calculates the distance to exit gate from goal car 
    """
    for car in cars:
        if car.id == 'G':
            goal_car = car 
            
    if goal_car is None:
        raise ValueError("Goal car not found in the node.")
    
    distance_to_exit = (8 - (goal_car.col + goal_car.size - 1))
    return distance_to_exit
    
