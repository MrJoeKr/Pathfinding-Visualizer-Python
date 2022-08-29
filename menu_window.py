import threading
import time
import pygame
import sys

import color_constants
from text_panel import TextPanel
import path_finding_algorithm
from config_constants import DISPLAY_WIDTH, DISPLAY_HEIGTH

CENTER_WIDTH = DISPLAY_WIDTH / 2
TITLE_HEIGHT = DISPLAY_HEIGTH / 5

ALGO_TEXT_HEIGHT = TITLE_HEIGHT + 90
ALGO_BUTTON_HEIGHT = ALGO_TEXT_HEIGHT + 50
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 50

HEURISTIC_TEXT_HEIGHT = ALGO_BUTTON_HEIGHT + 90
HEURISTIC_BUTTON_HEIGHT = HEURISTIC_TEXT_HEIGHT + 50

START_BUTTON_HEIGHT = HEURISTIC_TEXT_HEIGHT + 150

_ARROW_CLICK_DELAY = 0.1

class MenuWindow:

    def __init__(self, display: pygame.Surface) -> None:

        self.display = display

        self.running = True

        # Delay between clicks
        self._left_click_executed = False

        self.display.fill(color_constants.WHITE)

        self._draw_menu()

        self._init_algo_button()

        self._init_start_button()

        pygame.display.update()


    # Algo text
    def _draw_algo_title_text(self) -> None:
        algo_font = pygame.font.Font(None, 40)
        algo_text = algo_font.render("Choose your algorithm", True, color_constants.BLACK)

        algo_rect = algo_text.get_rect(center=(DISPLAY_WIDTH / 2, ALGO_TEXT_HEIGHT))

        self.display.blit(algo_text, algo_rect)

    def _init_algo_button(self):

        self._draw_algo_title_text()

        self.algo_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.algo_button.center = (CENTER_WIDTH, ALGO_BUTTON_HEIGHT)

        self.algorithms = path_finding_algorithm.get_algorithms_list()
        # Init algorithm variables
        self._update_algorithm(0)

        arrow_padding = 20
        arrow_width = 40

        self.left_algo_arrow = pygame.Rect(self.algo_button.x - arrow_padding - arrow_width, self.algo_button.y, arrow_width, self.algo_button.height)
        self.right_algo_arrow = pygame.Rect(self.algo_button.x + self.algo_button.width + arrow_padding, self.algo_button.y, arrow_width, self.algo_button.height)

        pygame.draw.rect(self.display, color_constants.BLACK, self.left_algo_arrow)
        pygame.draw.rect(self.display, color_constants.BLACK, self.right_algo_arrow)

    def _draw_menu(self) -> None:

        self._draw_title_text()

        self._draw_select_buttons()

        self._init_start_button()


    def _init_start_button(self) -> None:

        self.start_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.start_button_rect.center = (CENTER_WIDTH, START_BUTTON_HEIGHT)

        pygame.draw.rect(self.display, color_constants.BLACK, self.start_button_rect)

        # Display text
        start_font = pygame.font.Font(None, 58)
        start_text = start_font.render("Start Drawing", True, color_constants.WHITE)

        self._draw_text_to_middle_of_rect(start_text, self.start_button_rect)

    def _draw_text_to_middle_of_rect(self, text: pygame.Surface, rect: pygame.Rect) -> None:

        text_rect = text.get_rect(center=(rect.x + rect.width / 2, rect.y + rect.height / 2))
        self.display.blit(text, text_rect)

    def _draw_select_buttons(self) -> None:

        pass

    # Draw title text
    def _draw_title_text(self) -> None:
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("Path Visualizer", True, color_constants.BLACK)
        # Center the text
        up_padding = DISPLAY_HEIGTH / 8
        text_rect = title_text.get_rect(center=(DISPLAY_WIDTH / 2, TITLE_HEIGHT))

        self.display.blit(title_text, text_rect)

    def get_algorithm(self) -> path_finding_algorithm.SearchFunction:
        return self.selected_algo_func

    def get_heuristic(self) -> path_finding_algorithm.HeuristicFunction:
        # TODO
        return path_finding_algorithm.euclidian_distance
        pass

    def process_mouse_events(self) -> None:
        
        left_pressed, _, _ = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()

        # Left click
        if left_pressed and not self._left_click_executed:

            self._left_click_executed = True
            self._wait_for_next_execution_thread()

            self._process_left_right_arrow_buttons(mx, my)

            self._process_start_button(mx, my)

    def _process_start_button(self, mx: int, my: int) -> None:
        # Stop this window if start drawing was clicked
        if self.start_button_rect.collidepoint(mx, my):
            self.running = False
            time.sleep(0.1)

    def _update_algorithm(self, idx: int) -> None:

        idx %= len(self.algorithms)

        self.algo_idx = idx
        self.selected_algo_text, self.selected_algo_func = self.algorithms[self.algo_idx]

        self._draw_algo_button_text()


    def _draw_algo_button_text(self) -> None:
        
        algo_font = pygame.font.Font(None, 40)
        algo_text = algo_font.render(self.selected_algo_text, True, color_constants.WHITE)

        # Clear text
        pygame.draw.rect(self.display, color_constants.BLACK, self.algo_button)

        self._draw_text_to_middle_of_rect(algo_text, self.algo_button)

        pygame.display.update(self.algo_button)
        

    def _process_left_right_arrow_buttons(self, mx: int, my: int) -> None:

        if self.left_algo_arrow.collidepoint(mx, my):

            self._update_algorithm(self.algo_idx - 1)
        
        if self.right_algo_arrow.collidepoint(mx, my):

            self._update_algorithm(self.algo_idx + 1)

    # Process keys
    def process_key_events(self) -> None:

        for event in pygame.event.get():
            # Quit app
            if event.type == pygame.QUIT:
                self.quit_app()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.quit_app()

    def quit_app(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()

    def _wait_for_next_execution_thread(self) -> None:
        thread = threading.Thread(target=self._help_wait)
        thread.start()

    def _help_wait(self) -> None:
        time.sleep(_ARROW_CLICK_DELAY)
        self._left_click_executed = False