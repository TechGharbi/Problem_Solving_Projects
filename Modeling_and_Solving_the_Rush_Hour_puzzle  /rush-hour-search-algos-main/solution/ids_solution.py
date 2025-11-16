from __future__ import annotations  # Allows a class to contain type hints that refer to itself. We use Node instead of 'Node'
from model import Node
from .solution import Solution
from collections import deque

import time
MAX_DEPTH = 100

class IDS(Solution):
    def calculate_heuristic(self, current_node: Node):
        return 0
    
    def dls(self, start_node: Node, depth_limit) -> Node:
        # Push dô stack
        Stack = deque([(start_node, 0)])          
        visited = {start_node}

        while len(Stack) != 0:
            # Expand node
            current_node, depth = Stack.popleft()

            if depth >= depth_limit:
                continue

            self.number_expanded_nodes += 1

            if current_node.is_goal():
                self.total_cost = current_node.cost
                return current_node
            
            for new_node in self.get_successors(current_node):   
                if new_node not in visited:          
                    new_node.parent = current_node

                    Stack.appendleft((new_node, depth + 1))
                    visited.add(new_node)         

        return None
                    
    def solve(self) -> Node: # IDS
        start_time = time.perf_counter()
        for depth_limit in range(MAX_DEPTH + 1):
            current_state = self.dls(self.initial_node, depth_limit)
            end_time = time.perf_counter()

            if end_time - start_time >= 30:
                return None
            # print(self.number_expanded_nodes)
            if current_state:
                return current_state
            
        return None
