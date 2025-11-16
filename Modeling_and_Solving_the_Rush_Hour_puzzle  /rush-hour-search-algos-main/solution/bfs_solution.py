from __future__ import annotations  # Allows a class to contain type hints that refer to itself. We use Node instead of 'Node'
from model import Node
from .solution import Solution
from collections import deque

class BFS(Solution):
    def calculate_heuristic(self, current_node: Node):
        return 0
    
    def solve(self) -> Node:
        Queue = deque()           # Dùng deque hay queue đều được
        archive = {}

        # Push dô deque
        Queue.appendleft(self.initial_node)

        while len(Queue) != 0:
            # Expand node
            current_node = Queue.pop()
            self.number_expanded_nodes += 1

            # Nếu không phải trạng thái đích thì đểm các state hợp lệ
            
            for new_node in self.get_successors(current_node):          # Mỗi move là 1 list Vehicles hợp lệ -> newgameboard mới tạo ra gamestate tương ứng với list đó   
                if new_node.is_goal():
                    self.total_cost = new_node.cost 
                    new_node.parent = current_node
                    return new_node
                
                if new_node not in archive:                 # Kiểm tra state đã tồn tại trong hàng đợi hay chưa?
                    Queue.appendleft(new_node)
                    new_node.parent = current_node
                    archive[new_node] = True           

