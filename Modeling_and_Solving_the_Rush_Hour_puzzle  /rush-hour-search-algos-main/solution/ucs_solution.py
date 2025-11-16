from __future__ import annotations  # Allows a class to contain type hints that refer to itself. We use Node instead of 'Node'
from model import Node
from .solution import Solution

import heapq

class UCS(Solution):
    def calculate_heuristic(self, current_node: Node):
        return 0
    
    def solve(self) -> Node:
        frontier = []
        path_cost = {} # Store g(n) of each node and update if it's optimal

        heapq.heappush(frontier, (0, self.initial_node))
        path_cost[self.initial_node] = self.initial_node.cost

        while frontier:
            f_cost, current_node = heapq.heappop(frontier)

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
                    heapq.heappush(frontier, (neighbor.cost, neighbor))
                    
        raise ValueError("The puzzle cannot be solved. No solution found.")
    
