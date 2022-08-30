from typing import Callable, List, Optional
import pygame
import time

from config_constants import *
from node_object import Node

PathList = List[Node]

class NodeBoard:

    def __init__(self, display: pygame.Surface, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.display = display

        self.board: List[List[Node]] = self._init_board()

        self.start_node: Optional[Node] = None
        self.end_node: Optional[Node] = None

        self.path: PathList = []
        self.finding_path_finished = False

    def _init_board(self) -> List[List[Node]]:
        out = []
        for y in range(self.rows):
            sub = []
            out.append(sub)
            for x in range(self.cols):
                node = Node(self.display, parent=None, position=(x, y))
                sub.append(node)
        
        return out

    def draw_board(self) -> None:
        for row in self.board:
            for node in row:
                
                node.draw_node(NODE_COLOR)

                if node is self.start_node:
                    node.draw_as_circle(START_POINT_COLOR)

                elif node is self.end_node:
                    node.draw_as_circle(END_POINT_COLOR)

    def reset_board(self):
        self.start_node = None
        self.end_node = None
        self.board = self._init_board()

        self.clear_solution()

        self.draw_board()

    # Resets node flags and removes found path
    def clear_solution(self) -> None:
        self.path.clear()
        self.finding_path_finished = False

        for row in self.board:
            for node in row:
                node.clear_flags()

                if node is not self.start_node and node is not self.end_node:
                    node.draw_node()

    def get_board(self):
        return self.board

    def get_node(self, y: int, x: int):
        return self.board[y][x]

    # Get all node neighbours (including walls)
    # Predicate can be used to select specific node neigbours
    # If predicate is True, node is selected
    def get_node_neighbours(self, node: Node, predicate: Callable[[Node], bool]=lambda _: True) -> List[Node]:

        out = []

        for add_x, add_y in MOVES:
            
            x = node.x + add_x
            y = node.y + add_y 

            # Invalid position
            if x < 0 or x >= self.cols \
                    or y < 0 or y >= self.rows:
                continue
            
            child = self.get_node(y, x)

            if predicate(child):
                out.append(child)

        return out

    def draw_path(self) -> None:

        node_color = PATH_NODES_COLOR

        for node in self.path:

            if node == self.path[0]:
                node.draw_as_circle(START_POINT_COLOR)

            elif node == self.path[-1]:
                node.draw_as_circle(END_POINT_COLOR)

            else:
                node.draw_pop_up_animation(node_color)
                # node.set_color(node_color)

            pygame.display.update()
            time.sleep(SHOW_PATH_DELAY)

    def solution_found(self) -> bool:
        return len(self.path) > 0
