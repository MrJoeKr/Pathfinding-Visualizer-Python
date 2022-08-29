import pygame

# Project files
from board_window import BoardWindow
from menu_window import MenuWindow
import path_finding_algorithm
from color_constants import *
from config_constants import *


# Initialize pygame
pygame.init()

DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGTH))
pygame.display.set_caption('A* path finder')
MAINCLOCK = pygame.time.Clock()


def run_app():

    algorithm, heuristic = run_menu_window()
    run_board_window(algorithm, heuristic)


def run_menu_window():

    menu = MenuWindow(DISPLAY)

    while menu.running:
        
        menu.process_mouse_events()
        menu.process_key_events()

        MAINCLOCK.tick(FPS)

    algorithm = menu.get_algorithm()
    heuristic = menu.get_heuristic()

    return algorithm, heuristic

def run_board_window(
    algorithm: path_finding_algorithm.SearchFunction,
    heuristic: path_finding_algorithm.HeuristicFunction) -> None:

    # Initialize board window object
    app_window = BoardWindow(DISPLAY, ROWS, COLS, search_func=algorithm, heuristic_func=heuristic)

    while app_window.running:

        app_window.process_mouse_events()

        app_window.process_key_events()

        MAINCLOCK.tick(FPS)


if __name__ == "__main__":
    run_app()