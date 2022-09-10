import threading
import time
import pygame
import sys

import library.constants.color as color
from library.text_panel import TextPanel
import library.pathfinding.algorithms as algorithms
import library.constants.config as config

CENTER_WIDTH = config.DISPLAY_WIDTH / 2
TITLE_HEIGHT = config.DISPLAY_HEIGTH / 6

BACKGROUND_COLOR = color.WHITE

ALGO_TEXT_HEIGHT = TITLE_HEIGHT + 90
ALGO_BUTTON_HEIGHT = ALGO_TEXT_HEIGHT + 50
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 50

HEURISTIC_TEXT_HEIGHT = ALGO_BUTTON_HEIGHT + 70
HEURISTIC_BUTTON_HEIGHT = HEURISTIC_TEXT_HEIGHT + 50

START_BUTTON_HEIGHT = HEURISTIC_TEXT_HEIGHT + 250

_ARROW_CLICK_DELAY = 0.1


class MenuWindow:
    def __init__(self, display: pygame.Surface) -> None:

        self.display = display

        self.running = True

        # Delay between clicks
        self._left_click_executed = False

        self.algo_idx = 0
        self.heuristic_idx = 0

    def draw_window(self) -> None:
        self.display.fill(BACKGROUND_COLOR)

        self._draw_title_text()

        self._init_algo_button()

        # Init algorithm selection variables
        self._update_algorithm_selection(self.algo_idx)
        
        self._init_heuristic_button()

        # Init heuristic selection variables
        self._update_heuristic_selection(self.heuristic_idx)

        self._init_start_button()

        pygame.display.update()

    def _draw_heuristic_title_text(self) -> None:
        font = pygame.font.Font(None, 40)
        text = font.render("Choose your heuristic", True, color.BLACK)

        algo_rect = text.get_rect(center=(config.DISPLAY_WIDTH / 2, HEURISTIC_TEXT_HEIGHT))

        self.display.blit(text, algo_rect)

    def _update_heuristic_selection(self, idx: int = 0) -> None:
        idx %= len(self.heuristics)

        self.heuristic_idx = idx
        self.selected_heuristic_text, self.selected_heuristic_func = self.heuristics[
            self.heuristic_idx
        ]

        
        self._draw_heuristic_button_text()

    def _draw_heuristic_button_text(self) -> None:

        font = pygame.font.Font(None, 40)
        heuristic_text = font.render(
            self.selected_heuristic_text, True, color.WHITE
        )

        # Clear text
        pygame.draw.rect(self.display, color.BLACK, self.heuristic_button)

        self._draw_text_to_middle_of_rect(heuristic_text, self.heuristic_button)

        pygame.display.update(self.heuristic_button)

    def _draw_arrow_rect(self, rect: pygame.Rect, left: bool = True) -> None:

        border_radius: int = min(rect.width, rect.height) // 4

        pygame.draw.rect(
            self.display, color.BLACK, rect, border_radius=border_radius
        )

        # Draw arrow lines
        if left:
            x1 = rect.x + rect.width - rect.width / 4
        else:
            x1 = rect.x + rect.width / 4

        x2 = rect.x + rect.width / 2

        y1 = rect.y + rect.height / 10
        y2 = rect.y + rect.height / 2
        y3 = rect.y + rect.height - (y1 - rect.y)
        points = [(x1, y1), (x2, y2), (x1, y3)]
        pygame.draw.lines(self.display, color.WHITE, False, points, width=4)

    def _init_heuristic_button(self) -> None:

        self._draw_heuristic_title_text()

        self.heuristic_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.heuristic_button.center = (CENTER_WIDTH, HEURISTIC_BUTTON_HEIGHT)

        self.heuristics = algorithms.get_heuristics_list()

        arrow_padding = 20
        arrow_width = 40

        self.left_heuristic_arrow = pygame.Rect(
            self.heuristic_button.x - arrow_padding - arrow_width,
            self.heuristic_button.y,
            arrow_width,
            self.heuristic_button.height,
        )
        self.right_heuristic_arrow = pygame.Rect(
            self.heuristic_button.x + self.heuristic_button.width + arrow_padding,
            self.heuristic_button.y,
            arrow_width,
            self.heuristic_button.height,
        )

        self._draw_arrow_rect(self.left_heuristic_arrow, left=True)
        self._draw_arrow_rect(self.right_heuristic_arrow, left=False)

    # Algo text
    def _draw_algo_title_text(self) -> None:
        algo_font = pygame.font.Font(None, 40)
        algo_text = algo_font.render(
            "Choose your algorithm", True, color.BLACK
        )

        algo_rect = algo_text.get_rect(center=(config.DISPLAY_WIDTH / 2, ALGO_TEXT_HEIGHT))

        self.display.blit(algo_text, algo_rect)

    def _init_algo_button(self):

        self._draw_algo_title_text()

        self.algo_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.algo_button.center = (CENTER_WIDTH, ALGO_BUTTON_HEIGHT)

        self.algorithms = algorithms.get_algorithms_list()

        arrow_padding = 20
        arrow_width = 40

        self.left_algo_arrow = pygame.Rect(
            self.algo_button.x - arrow_padding - arrow_width,
            self.algo_button.y,
            arrow_width,
            self.algo_button.height,
        )
        self.right_algo_arrow = pygame.Rect(
            self.algo_button.x + self.algo_button.width + arrow_padding,
            self.algo_button.y,
            arrow_width,
            self.algo_button.height,
        )

        self._draw_arrow_rect(self.left_algo_arrow, left=True)
        self._draw_arrow_rect(self.right_algo_arrow, left=False)

    def _init_start_button(self) -> None:

        self.start_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.start_button_rect.center = (CENTER_WIDTH, START_BUTTON_HEIGHT)

        pygame.draw.rect(self.display, color.BLACK, self.start_button_rect)

        # Display text
        start_font = pygame.font.Font(None, 58)
        start_text = start_font.render("Go To Board", True, color.WHITE)

        self._draw_text_to_middle_of_rect(start_text, self.start_button_rect)

    def _draw_text_to_middle_of_rect(
        self, text: pygame.Surface, rect: pygame.Rect
    ) -> None:

        text_rect = text.get_rect(
            center=(rect.x + rect.width / 2, rect.y + rect.height / 2)
        )
        self.display.blit(text, text_rect)

    def _draw_select_buttons(self) -> None:

        pass

    # Draw title text
    def _draw_title_text(self) -> None:
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("Pathfinding Visualizer", True, color.BLACK)
        # Center the text
        up_padding = config.DISPLAY_HEIGTH / 8
        text_rect = title_text.get_rect(center=(config.DISPLAY_WIDTH / 2, TITLE_HEIGHT))

        self.display.blit(title_text, text_rect)

    def get_algorithm(self) -> algorithms.SearchFunction:
        return self.selected_algo_func

    def get_heuristic(self) -> algorithms.HeuristicFunction:
        return self.selected_heuristic_func

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

    def _update_algorithm_selection(self, idx: int = 0) -> None:

        idx %= len(self.algorithms)

        self.algo_idx = idx
        self.selected_algo_text, self.selected_algo_func = self.algorithms[
            self.algo_idx
        ]

        self._draw_algo_button_text()

    def _draw_algo_button_text(self) -> None:

        algo_font = pygame.font.Font(None, 40)
        algo_text = algo_font.render(
            self.selected_algo_text, True, color.WHITE
        )

        # Clear text
        pygame.draw.rect(self.display, color.BLACK, self.algo_button)

        self._draw_text_to_middle_of_rect(algo_text, self.algo_button)

        pygame.display.update(self.algo_button)

    def _hide_heuristic_button(self) -> None:
        pygame.draw.rect(self.display, BACKGROUND_COLOR, self.heuristic_button)
        pygame.draw.rect(self.display, BACKGROUND_COLOR, self.left_heuristic_arrow)
        pygame.draw.rect(self.display, BACKGROUND_COLOR, self.right_heuristic_arrow)

        pygame.display.update([self.heuristic_button, self.left_heuristic_arrow, self.right_heuristic_arrow])


    def _process_left_right_arrow_buttons(self, mx: int, my: int) -> None:

        if self.left_algo_arrow.collidepoint(mx, my):
            self._update_algorithm_selection(self.algo_idx - 1)

        if self.right_algo_arrow.collidepoint(mx, my):
            self._update_algorithm_selection(self.algo_idx + 1)

        # # Heuristics only for A Star Search
        # if self.selected_algo_text != "A Star Search":
        #     self._hide_heuristic_button()
        # else:
        #     pass

        if self.left_heuristic_arrow.collidepoint(mx, my):
            self._update_heuristic_selection(self.heuristic_idx - 1)

        if self.right_heuristic_arrow.collidepoint(mx, my):
            self._update_heuristic_selection(self.heuristic_idx + 1)

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
