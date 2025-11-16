from __future__ import annotations  # Allows a class to contain type hints that refer to itself. We use Node instead of 'Node'
from model import Node
from .solution import Solution

from solution.heuristic import *
import heapq  # Importing heapq for priority queue implementation

class AStar(Solution):
    """
    A* search algorithm solution class.
    """
    def calculate_heuristic(self, current_node: Node):
        return evaluate_advanced_heuristic(current_node.cars)
    
    def solve(self) -> Node:
        priority_queue = [] 
        path_cost = {} # Store g(n) of each node and update if it's optimal

        self.initial_node.heuristic = self.calculate_heuristic(self.initial_node)
        self.initial_node.cost = 0

        f_n = self.initial_node.cost + self.initial_node.heuristic
        
        heapq.heappush(priority_queue, (f_n, self.initial_node))
        path_cost[self.initial_node] = self.initial_node.cost

        while priority_queue:
            f_cost, current_node = heapq.heappop(priority_queue)

            # Crucial
            if current_node.cost > path_cost[current_node]:
                continue
    
            self.number_expanded_nodes += 1

            if current_node.is_goal():
                self.total_cost = current_node.cost
                return current_node
        
            for neighbor in self.get_successors(current_node):
                if neighbor not in path_cost or neighbor.cost < path_cost[neighbor]:
                    path_cost[neighbor] = neighbor.cost
                    neighbor.parent = current_node
                    heapq.heappush(priority_queue, (neighbor.cost + neighbor.heuristic, neighbor))
                    
        raise ValueError("The puzzle cannot be solved. No solution found.")
    