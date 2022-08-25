from typing import List, Optional
import pygame
import threading
import time
from config_constants import END_POINT_COLOR, START_POINT_COLOR
from node_board_object import NodeBoard
from node_object import Node
from pygame_tick_box import TickBox
from config_constants import *

BOTTOM_PANEL_HEIGHT = 50
TICK_BOX_WIDTH = 30
_TICK_BOX_CLICK_DELAY = 0.1

# TODO:
#   - reset board and window

class BoardWindow:

    def __init__(
            self, display: pygame.display, rows: int, cols: int):

        self.board = NodeBoard(display, rows, cols)

        # Initialize tick box
        self.tick_box: TickBox = TickBox(
            display, 
            DISPLAY_WIDTH - TICK_BOX_WIDTH - DISPLAY_WIDTH / 30, 
            DISPLAY_HEIGTH - BOTTOM_PANEL_HEIGHT + 5, 
            TICK_BOX_WIDTH)

        # Used for tick box threading to wait between clicks
        self._tick_box_executed: bool = False

    def get_node_board(self) -> NodeBoard:
        return self.board

    def process_mouse_events(self) -> None:

        left_pressed, middle_pressed, right_pressed = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()

        board: NodeBoard = self.board

        node: Optional[Node] = self._get_node_from_mouse_coords(mx, my)

        # Left click
        if left_pressed:
            if node is not None:
                if board.start_node is None:

                    board.start_node = node
                    node.set_color(START_POINT_COLOR)

                elif board.end_node is None and node != board.start_node:

                    board.end_node = node
                    node.set_color(END_POINT_COLOR)

                # Draw walls
                elif board.end_node is not None and node != board.end_node and node != board.start_node and not node.is_wall():
                    node.set_wall()

        # Delete walls
        if right_pressed:
            if node is not None:

                if node is board.start_node:
                    board.start_node = None

                elif node is board.end_node:
                    board.end_node = None

                elif node.is_wall():
                    node.unset_wall()

                node.clear_node()

        # Tick box collision
        if left_pressed and self.tick_box.is_mouse_collision(
                mx, my) and not self._tick_box_executed:

            self.tick_box.tick_untick_box()
            self._tick_box_executed = True
            self._wait_for_next_execution_thread()
        
    def show_steps(self) -> bool:
        return self.tick_box.is_ticked()

    def _get_node_from_mouse_coords(self, mx: int, my: int) -> Optional[Node]:

        rows, cols = self.board.rows, self.board.cols

        node_x = mx // NODE_SIZE
        node_y = my // NODE_SIZE
        node: Optional[Node] = None

        if node_y < rows and node_x < cols:
            node = self.board.board[node_y][node_x]

        return node

    # TODO
    def process_key_events() -> None:
        pass

    def _wait_for_next_execution_thread(self):
        threading.Thread(target=self._help_wait).start()

    def _help_wait(self):
        time.sleep(_TICK_BOX_CLICK_DELAY)
        self._tick_box_executed = False