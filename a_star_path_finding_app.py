import pygame

# Project files
from board_window import BoardWindow
from color_constants import *
from config_constants import *


# Initialize pygame
pygame.init()

DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGTH))
pygame.display.set_caption('A* path finder')
mainClock = pygame.time.Clock()

def run_app():

    # Initialize board window object
    app_window = BoardWindow(DISPLAY, ROWS, COLS)

    while app_window.running:

        app_window.process_mouse_events()

        app_window.process_key_events()

        mainClock.tick(FPS)


if __name__ == "__main__":
    run_app()