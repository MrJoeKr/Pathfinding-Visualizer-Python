from typing import List, Optional
import pygame

from node_object import Node

class NodeBoard:

    def __init__(self, display: pygame.display, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.display = display

        self.board: List[List[Node]] = self._init_draw_board()

        self.start_node: Optional[Node] = None
        self.end_node: Optional[Node] = None

    def _init_draw_board(self) -> List[List[Node]]:
        out = []
        for y in range(self.rows):
            sub = []
            out.append(sub)
            for x in range(self.cols):
                node = Node(self.display, parent=None, position=(x, y))
                sub.append(node)
                node.draw_display()
        
        return out

    def get_board(self):
        return self.board