from abc import ABC, abstractmethod
from model.node import Node
import time 

class Solution(ABC):
    """
    Abstract base class for solution strategies.
    """

    def __init__(self, initial_node: Node, memory_usage: int = 0, number_expanded_nodes: int = 0, 
                 total_cost: int = 0, search_time: time = 0, step_count: int = 0):
        """
        Initialize the solution with the initial node.
        """
        self.initial_node = initial_node 
        self.memory_usage = memory_usage 
        self.number_expanded_nodes = number_expanded_nodes
        self.total_cost = total_cost
        self.search_time = search_time
        self.step_count = step_count

    def calculate_cost(self, parent_cost: int = 0, new_cost: int = 0):
        return parent_cost + new_cost

    @abstractmethod
    def calculate_heuristic(self, current_node: Node):
        pass

    def get_successors(self, current_node: Node) -> list[Node]:
        successors = []
        for temp_cars, action, new_car in current_node.get_next_possible_moves():
            new_cost = self.calculate_cost(current_node.cost, new_car.size)
            h_cost = self.calculate_heuristic(current_node)
            
            new_node = Node(cars = temp_cars, action = action, parent = current_node, cost = new_cost, heuristic = h_cost)
            successors.append(new_node)

        return successors
    
    @abstractmethod
    def solve(self) -> Node: # Return Goal Node
        """
        Abstract method to solve the problem and return the goal node.
        """
        pass
    
    def print_informations(self, goal_node: Node):
        print(f"Number of Expanded Nodes: {self.number_expanded_nodes}")
        print(f"Search Time: {self.search_time:.2f} seconds")
        print(f"Memory Usage: {self.memory_usage} MB")
        print(f"Total Cost: {self.total_cost}")
        print(f"Step count:  {self.step_count}")

    def find_path(self, goal_node: Node) -> list:
        path = []

        while goal_node:
            path.append(goal_node)
            goal_node = goal_node.parent
        
        self.step_count = len(path) - 1

        path = reversed(path)

        return path
    