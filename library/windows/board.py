from typing import Any, Callable, Iterable, Optional
import pygame
import threading
import time
import sys

from library.constants.config import *
from library.node.board import NodeBoard
from library.node.node import Node
from library.pathfinding.pathfinder import PathFinder
import library.pathfinding.algorithms as path_algorithms
from library.text_panel import TextPanel
from library.tick_box import TickBox
from library.maze.generator import MazeGenerator
import library.maze.algorithms as maze_algorithms


BOTTOM_PANEL_HEIGHT = 50
BOTTOM_PANEL_WIDTH = DISPLAY_WIDTH - 100
TICK_BOX_WIDTH = 30
_TICK_BOX_CLICK_DELAY = 0.1


class BoardWindow:
    def __init__(
        self,
        display: pygame.Surface,
        rows: int,
        cols: int,
        search_func: path_algorithms.SearchFunction = path_algorithms.search_a_star,
        heuristic_func: path_algorithms.HeuristicFunction = path_algorithms.euclidian_distance,
    ):

        self.display = display

        self.board = NodeBoard(display, rows, cols)

        self.path_algorithm = search_func
        self.heuristic = heuristic_func

        # Text panel
        self.text_panel = TextPanel(
            display,
            0,
            DISPLAY_HEIGTH - BOTTOM_PANEL_HEIGHT,
            BOTTOM_PANEL_WIDTH,
            BOTTOM_PANEL_HEIGHT,
            color.BLACK,
        )

        # Initialize tick box
        self.tick_box: TickBox = TickBox(
            display,
            DISPLAY_WIDTH - TICK_BOX_WIDTH - DISPLAY_WIDTH / 30,
            DISPLAY_HEIGTH - BOTTOM_PANEL_HEIGHT + 5,
            TICK_BOX_WIDTH,
        )

        # Used for tick box threading to wait between clicks
        self._tick_box_executed: bool = False

        # If stops running is set to False
        self.running = True

        self.user_wants_menu = False

        # To visualize only once per key press
        self._visualizing_started = False

    def draw_window(self) -> None:
        self.display.fill(color.BLACK)

        self.board.draw_board()

        self.text_panel.draw_display()

        self.tick_box.draw_tick_box()

        self._update_text()
        pygame.display.update()

    def update_pathfinding_funcs(
        self,
        search: path_algorithms.SearchFunction,
        heuristic: path_algorithms.HeuristicFunction,
    ) -> None:

        self.path_algorithm = search
        self.heuristic = heuristic

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
                elif (
                    board.end_node is not None
                    and node != board.end_node
                    and node != board.start_node
                    and not node.is_wall()
                ):
                    node.set_wall(update_screen=True)

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
        if (
            left_pressed
            and self.tick_box.is_mouse_collision(mx, my)
            and not self._tick_box_executed
        ):

            self.tick_box.tick_untick_box()
            self._tick_box_executed = True
            self._wait_for_next_execution_thread()

        return left_pressed or middle_pressed or right_pressed


    # Update text when some progress happened
    def _update_text(self) -> None:

        self.text_panel.clear_panel()
        text_margin_left = 5

        if self.board.start_node is None:
            self.text_panel.write_text(
                0 + text_margin_left, 0, "Choose start point", START_POINT_COLOR
            )

        elif self.board.end_node is None:
            self.text_panel.write_text(
                0 + text_margin_left, 0, "Choose end point", END_POINT_COLOR
            )

        elif self.board.end_node is not None and not self.board.finding_path_finished:
            self.text_panel.write_text(
                0 + text_margin_left,
                0,
                "Draw walls or press SPACE to start",
                color.WHITE,
            )

        elif self.board.finding_path_finished and self.board.solution_found():
            length = len(self.board.path) - 1
            plural = "s" if length > 1 else ""
            self.text_panel.write_text(
                0 + text_margin_left,
                0,
                f"Solution found! Path is {length} node{plural} long",
                START_POINT_COLOR,
            )

        elif self.board.finding_path_finished and not self.board.solution_found():
            self.text_panel.write_text(
                0 + text_margin_left, 0, "No path was found", END_POINT_COLOR
            )

    def _get_node_from_mouse_coords(self, mx: int, my: int) -> Optional[Node]:

        rows, cols = self.board.rows, self.board.cols

        node_x = mx // NODE_SIZE
        node_y = my // NODE_SIZE
        node: Optional[Node] = None

        if node_y < rows and node_x < cols:
            node = self.board.get_node(node_y, node_x)

        return node

    # Process keys
    # Returns true if user pressed any valid key
    def process_key_events(self) -> bool:

        for event in pygame.event.get():
            # Quit app
            if event.type == pygame.QUIT:
                self.quit_app()

                return True

            elif event.type == pygame.KEYDOWN:

                # Back to main menu
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    self.user_wants_menu = True

                    return True

                # Reset board
                elif event.key == pygame.K_r:
                    self.reset_board_window()

                    return True

                # Start the algorithm (can be started more than once)
                elif self.board.end_node is not None and event.key == pygame.K_SPACE:

                    if not self._visualizing_started:
                        self._visualizing_started = True
                        self._process_pathfinding()

                    return True

                # Generate maze
                elif event.key == pygame.K_m:
                    self._process_maze_generation(maze_algorithms.recursive_division)

                elif event.key == pygame.K_n:
                    self._process_maze_generation(maze_algorithms.randomized_dfs)

        return False

    def _process_maze_generation(self, algorithm: maze_algorithms.MazeFunction):
        show_steps = self.tick_box.is_ticked()

        maze_gen = MazeGenerator(algorithm, show_steps=show_steps)

        not_interrupted = self._start_function_async(maze_gen.generate_maze, args=(self.board,))

        if not not_interrupted:
            maze_gen.stop_visualize()

    def _process_pathfinding(self):

        # Clear every time it starts
        self.board.clear_solution()

        self._search_path_async()
        # self._search_path_sync()

        self._visualizing_started = False

    def _search_path_async(self) -> None:

        show_steps = self.tick_box.is_ticked()

        path_finder = PathFinder(
            search_func=self.path_algorithm,
            heuristic=self.heuristic,
            show_steps=show_steps,
        )

        success = self._start_function_async(path_finder.start_search, args=(self.board,))

        if not success:
            path_finder.stop_visualizing()

        if success:
            # Show path length
            self._update_text()

            self._draw_path_async()


    def _draw_path_async(self) -> None:

        self._start_function_async(self.board.draw_path)

        # To stop the draw_path thread
        self.board.drawing_path_finished = True

    
    def _start_function_async(self, target: Callable[[Any], None], args: Iterable = []) -> bool:
        """
        Brief
        ---
        Starts function asynchronously and if key or mouse event occurs, it stops the function

        Returns
        ---
        True if not stopped by key / mouse event else False
        """

        thread = threading.Thread(target=target, args=[a for a in args])
        thread.start()

        success = True
        while thread.is_alive():

            key_pressed = self.process_key_events()
            mouse_pressed = self.process_mouse_events()

            if key_pressed or mouse_pressed:
                success = False
                break

            # Prevent lag
            time.sleep(0.1)

        return success


    def _search_path_sync(self) -> None:

        show_steps = self.tick_box.is_ticked()

        path_finder = PathFinder(
            search_func=self.path_algorithm,
            heuristic=self.heuristic,
            show_steps=show_steps,
        )

        path_finder.start_search(self.board)

        self.board.draw_path()

    def quit_app(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()

    def reset_board_window(self) -> None:
        self.board.reset_board()
        self._update_text()

    def update_window(self) -> None:
        if pygame.display.get_init():
            pygame.display.update()

    def _wait_for_next_execution_thread(self) -> None:
        thread = threading.Thread(target=self._help_wait)
        thread.start()

    def _help_wait(self) -> None:
        time.sleep(_TICK_BOX_CLICK_DELAY)
        self._tick_box_executed = False
