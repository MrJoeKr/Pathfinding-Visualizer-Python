import time
import math
from typing import Optional, Union
import pygame
from config_constants import NODE_SIZE, NODE_BORDER_COLOR, NODE_COLOR, FOREGROUND_PADDING, WALL_COLOR


Color = tuple[int, int, int]

DEFAULT_FLAG_VALUE = 0

class Node():
    # Class for nodes -> squares on the board
    def __init__(
            self, display: pygame.Surface, parent: "Node" = None,
            position: tuple[int, int] = None):

        self.display = display

        self.parent = parent
        # x and y are positions in the maze
        self.position = position
        self.x, self.y = self.position

        self.width = NODE_SIZE
        self.default_color = NODE_COLOR
        self.border_color = NODE_BORDER_COLOR

        # Position for displaying node in window
        self.draw_position = \
            (position[0] * self.width,
             position[1] * self.width)

        self.draw_x, self.draw_y = self.draw_position

        self._update_rect = pygame.Rect(self.draw_x, self.draw_y, self.width, self.width)

        # For A* algorithm
        self.g: Union[float, int] = math.inf

        # For other algorithms
        self.flag: int = DEFAULT_FLAG_VALUE

        self._is_wall = False
        self.visited = False

    def __eq__(self, other: "Node") -> bool:
        # check equality with another node
        return self.position == other.position

    # For debugging purposes
    def __repr__(self) -> str:
        return f"Node(x={self.x}, y={self.y})"

    def clear_flags(self) -> None:
        self.g = math.inf
        self.flag = 0
        self.parent = None
        self.visited = False

    def get_rect(self) -> pygame.Rect:
        return self._update_rect

    def display_update(self):
        pygame.display.update([self._update_rect])

    def draw_node(self, color: Optional[Color]=None) -> None:
        draw_x, draw_y = self.draw_position

        if color is None:
            # Use default color
            color = self.default_color

        if self.is_wall():
            pygame.draw.rect(
                self.display, WALL_COLOR,
                pygame.Rect(draw_x, draw_y, self.width, self.width))

            self.display_update()

            return

        # Background square
        pygame.draw.rect(
            self.display, self.border_color,
            pygame.Rect(draw_x, draw_y, self.width, self.width))

        # Foreground square
        pygame.draw.rect(
            self.display, color,
            pygame.Rect(
                draw_x + FOREGROUND_PADDING,
                draw_y + FOREGROUND_PADDING,
                self.width - FOREGROUND_PADDING * 2,
                self.width - FOREGROUND_PADDING * 2))

        self.display_update()

    def draw_pop_up_animation(self, color: Color) -> None:

        start_node_size = 0.1
        pop_up_speed = 0.5

        center = \
            (self.draw_x + self.width / 2 + FOREGROUND_PADDING, 
            self.draw_y + self.width / 2 + FOREGROUND_PADDING)

        update_rect = pygame.Rect(self.draw_x, self.draw_y, self.width, self.width)
        size = start_node_size

        while size < self.width / 2 - FOREGROUND_PADDING:

            pygame.draw.circle(
                self.display,
                color,
                center,
                size
            )

            size += pop_up_speed
            pygame.display.update([update_rect])

    def draw_as_circle(self, color: Color) -> None:
        x, y = self.draw_position[0], self.draw_position[1]

        center = \
            (x + self.width / 2, 
            y + self.width / 2)

        pygame.draw.circle(
            self.display,
            color,
            center,
            self.width / 2 - FOREGROUND_PADDING,
        )

        self.display_update()

    def set_wall(self) -> None:
        self._is_wall = True
        self.draw_node()

    def unset_wall(self) -> None:
        self._is_wall = False
        self.draw_node()

    def clear_node(self) -> None:
        self.draw_node()

    def is_wall(self):
        return self._is_wall

    # TO BE REMOVED FUNCTIONS
    def get_rect(self) -> pygame.Rect:
        # x = self.position[1] * 18 + 5
        # y = self.position[0] * 18 + 5
        x, y = self.draw_position[0], self.draw_position[1]
        return pygame.Rect(x, y, self.width, self.width)

    def get_pos(self):
        x = self.position[1] * 18 + 5
        y = self.position[0] * 18 + 5
        return (x, y)
