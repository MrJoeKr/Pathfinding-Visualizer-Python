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


    def run_app(self):

        self._run_menu_window()
        self._run_board_window()


    def _run_menu_window(self):

        menu = MenuWindow(self.display)

        while menu.running:
            
            menu.process_mouse_events()
            menu.process_key_events()

            MAINCLOCK.tick(FPS)

        # Initialize functions for pathfinding
        self.algorithm: pfa.SearchFunction = menu.get_algorithm()
        self.heuristic: pfa.HeuristicFunction = menu.get_heuristic()

    def _run_board_window(self) -> None:

        # Initialize board window object
        board_window = BoardWindow(DISPLAY, ROWS, COLS, search_func=self.algorithm, heuristic_func=self.heuristic)

        while board_window.running:

            board_window.process_mouse_events()

            back_to_menu = board_window.process_key_events()

            if back_to_menu:
                self._run_menu_window()
                board_window.draw_window()

            MAINCLOCK.tick(FPS)


if __name__ == "__main__":
    Application().run_app()
