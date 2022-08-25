from typing import List, Optional
import pygame
import time

from config_constants import *
from node_object import Node

PathList = List[Node]

class NodeBoard:

    def __init__(self, display: pygame.display, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.display = display

        self.board: List[List[Node]] = self._init_draw_board()

        self.start_node: Optional[Node] = None
        self.end_node: Optional[Node] = None

        self.path: PathList = []
        self.finding_path_finished = False

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

    def reset_board(self):
        self.start_node = None
        self.end_node = None
        self.path.clear()
        self.finding_path_finished = False
        self.board = self._init_draw_board()

    def get_board(self):
        return self.board

    def get_node(self, y: int, x: int):
        return self.board[y][x]

    def draw_path(self) -> None:

        node_color = PATH_NODES_COLOR

        for node in self.path:
            node.set_color(node_color)

            if node == self.path[0]:
                node.draw_as_circle(START_POINT_COLOR)

            elif node == self.path[-1]:
                node.draw_as_circle(END_POINT_COLOR)

            pygame.display.update()
            time.sleep(SHOW_PATH_DELAY)

    def solution_found(self) -> bool:
        return len(self.path) > 0