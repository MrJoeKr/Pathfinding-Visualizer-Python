import pygame

# Project files
from board_window import BoardWindow
from menu_window import MenuWindow
import path_finding_algorithm as pfa
from color_constants import *
from config_constants import *

# Initialize pygame
pygame.init()

DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGTH))
pygame.display.set_caption('A* path finder')
MAINCLOCK = pygame.time.Clock()


class Application:

    def __init__(self):
        self.display = DISPLAY

        # Initialize menu window object
        self._menu_window = MenuWindow(self.display)
        # Initialize board window object
        self._board_window = BoardWindow(DISPLAY, ROWS, COLS)

        self.algorithm: pfa.SearchFunction = pfa.search_a_star
        self.heuristic: pfa.HeuristicFunction = pfa.euclidian_distance

    def run_app(self):

        self._run_menu_window()
        self._run_board_window()


    def _run_menu_window(self):

        self._menu_window.draw_window()
        self._menu_window.running = True

        while self._menu_window.running:
            
            self._menu_window.process_mouse_events()
            self._menu_window.process_key_events()

            MAINCLOCK.tick(FPS)

        # Initialize functions for pathfinding
        self.algorithm = self._menu_window.get_algorithm()
        self.heuristic = self._menu_window.get_heuristic()

        self._board_window.update_pathfinding_funcs(self.algorithm, self.heuristic)

    def _run_board_window(self) -> None:

        self._board_window.draw_window()
        self._board_window.running = True

        while self._board_window.running:

            self._board_window.process_mouse_events()

            back_to_menu = self._board_window.process_key_events()

            if back_to_menu:
                self._run_menu_window()
                self._board_window.draw_window()

            MAINCLOCK.tick(FPS)


if __name__ == "__main__":
    Application().run_app()
