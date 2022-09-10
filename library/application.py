import pygame

# Project files
from library.windows.board import BoardWindow
from library.windows.menu import MenuWindow
import library.pathfinding.algorithms as path_algorithms
import library.constants.config as config

# Initialize pygame
pygame.init()

DISPLAY = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGTH))
pygame.display.set_caption("Pathfinding Visualizer by MrJoeKr")
MAINCLOCK = pygame.time.Clock()


class Application:
    def __init__(self):
        self.display = DISPLAY

        # Initialize menu window object
        self._menu_window = MenuWindow(self.display)
        # Initialize board window object
        self._board_window = BoardWindow(DISPLAY, config.ROWS, config.COLS)

        self.algorithm: path_algorithms.SearchFunction = path_algorithms.search_a_star
        self.heuristic: path_algorithms.HeuristicFunction = path_algorithms.manhattan_distance

    def run_app(self):

        self._run_menu_window()
        self._run_board_window()

    def _run_menu_window(self):

        self._menu_window.draw_window()
        self._menu_window.running = True

        while self._menu_window.running:

            self._menu_window.process_mouse_events()
            self._menu_window.process_key_events()

            MAINCLOCK.tick(config.FPS)

        # Initialize functions for pathfinding
        self.algorithm = self._menu_window.get_algorithm()
        self.heuristic = self._menu_window.get_heuristic()

        self._board_window.update_pathfinding_funcs(self.algorithm, self.heuristic)

    def _run_board_window(self) -> None:

        self._board_window.draw_window()
        self._board_window.running = True

        while self._board_window.running:

            self._board_window.process_mouse_events()

            self._board_window.process_key_events()

            if self._board_window.user_wants_menu:
                self._run_menu_window()
                self._board_window.draw_window()

                self._board_window.user_wants_menu = False

            MAINCLOCK.tick(config.FPS)


if __name__ == "__main__":
    Application().run_app()
