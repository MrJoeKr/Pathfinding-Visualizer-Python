from typing import List, Optional
import pygame
import threading
import time
import sys

from config_constants import *
from color_constants import Color
from node_board_object import NodeBoard
from node_object import Node
from path_finding_algorithm import search_path
from text_panel import TextPanel
from tick_box import TickBox

BOTTOM_PANEL_HEIGHT = 50
BOTTOM_PANEL_WIDTH = DISPLAY_WIDTH - 100
TICK_BOX_WIDTH = 30
_TICK_BOX_CLICK_DELAY = 0.1

# TODO:
#   - Deleting start / end / wall nodes could be dynamic
#   - Path would be updated according to change

class BoardWindow:

    def __init__(
            self, display: pygame.display, rows: int, cols: int):

        display.fill(color_constants.BLACK)

        self.board = NodeBoard(display, rows, cols)

        # Text panel
        self.text_panel = TextPanel(
            display, 0, DISPLAY_HEIGTH - BOTTOM_PANEL_HEIGHT, BOTTOM_PANEL_WIDTH,
            BOTTOM_PANEL_HEIGHT, color_constants.BLACK)

        # Initialize tick box
        self.tick_box: TickBox = TickBox(
            display,
            DISPLAY_WIDTH - TICK_BOX_WIDTH - DISPLAY_WIDTH / 30,
            DISPLAY_HEIGTH - BOTTOM_PANEL_HEIGHT + 5,
            TICK_BOX_WIDTH)

        # Used for tick box threading to wait between clicks
        self._tick_box_executed: bool = False

        self.running = True

        self._update_text()
        pygame.display.update()

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
                    node.draw_as_circle(START_POINT_COLOR)

                    self._update_text()

                elif board.end_node is None and node != board.start_node:

                    board.end_node = node
                    node.draw_as_circle(END_POINT_COLOR)

                    self._update_text()

                # Draw walls
                elif board.end_node is not None and node != board.end_node and node != board.start_node and not node.is_wall():
                    node.set_wall()

        # Delete walls
        if right_pressed:
            if node is not None:

                if node is board.start_node:
                    board.start_node = None

                    self._update_text()

                elif node is board.end_node:
                    board.end_node = None

                    self._update_text()

                elif node.is_wall():
                    node.unset_wall()

                node.clear_node()

        # Tick box collision
        if left_pressed and self.tick_box.is_mouse_collision(
                mx, my) and not self._tick_box_executed:

            self.tick_box.tick_untick_box()
            self._tick_box_executed = True
            self._wait_for_next_execution_thread()

    # Update text when some progress happened
    def _update_text(self) -> None:
        
        self.text_panel.clear_panel()
        text_margin_left = 5

        if self.board.start_node is None:
            self.text_panel.write_text(0 + text_margin_left, 0, "Choose start point", START_POINT_COLOR)
        
        elif self.board.end_node is None:
            self.text_panel.write_text(0 + text_margin_left, 0, "Choose end point", END_POINT_COLOR)
        
        elif self.board.end_node is not None and not self.board.finding_path_finished:
            self.text_panel.write_text(0 + text_margin_left, 0, "Draw walls or press SPACE to start", color_constants.WHITE)

        elif self.board.finding_path_finished and self.board.solution_found():
            length = len(self.board.path) - 1
            plural = "s" if length > 1 else ""
            self.text_panel.write_text(0 + text_margin_left, 0, f"Solution found! Path is {length} node{plural} long", START_POINT_COLOR)

        elif self.board.finding_path_finished and not self.board.solution_found():
            self.text_panel.write_text(0 + text_margin_left, 0, "No path was found", END_POINT_COLOR)



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

    # Process keys
    def process_key_events(self) -> None:

        for event in pygame.event.get():
            # Quit app
            if event.type == pygame.QUIT:
                self.quit_app()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.quit_app()

                # Reset board
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_r:
                    self.reset_board_window()

                # Start the algorithm (only once in this version - dynamically updated later)
                if not self.board.finding_path_finished and self.board.end_node is not None and event.key == pygame.K_SPACE:

                    show_steps = self.tick_box.is_ticked()

                    # print("Starting algorithm")
                    search_path(self.board, show_steps=show_steps)
                    # print("Done")

                    self._update_text()

                    self.board.draw_path()

    def quit_app(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()

    def reset_board_window(self) -> None:
        self.board.reset_board()

    def update_window(self) -> None:
        if pygame.display.get_init():
            pygame.display.update()

    def _wait_for_next_execution_thread(self) -> None:
        thread = threading.Thread(target=self._help_wait)
        thread.start()

    def _help_wait(self) -> None:
        time.sleep(_TICK_BOX_CLICK_DELAY)
        self._tick_box_executed = False
