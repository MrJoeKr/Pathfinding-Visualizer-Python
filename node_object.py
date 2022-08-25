import pygame
from config_constants import NODE_SIZE, NODE_BORDER_COLOR, NODE_COLOR, FOREGROUND_PADDING, WALL_COLOR


Color = tuple[int, int, int]


class Node():
    # Class for nodes -> squares on the board
    def __init__(
            self, display: pygame.display, parent: "Node" = None,
            position: tuple[int, int] = None):

        self.display = display

        self.parent = parent
        self.position = position
        self.x = self.position[0]
        self.y = self.position[1]

        self.width = NODE_SIZE
        self.color = NODE_COLOR
        self.border_color = NODE_BORDER_COLOR

        # Position for displaying node
        self.draw_position = \
            (position[0] * self.width,
             position[1] * self.width)

        # For A* algorithm
        # f = g + h
        self.g = 0
        # self.h = 0
        # self.f = 0

        self._is_wall = False
        self.visited = False

    def __eq__(self, other: "Node") -> bool:
        # check equality with another node
        return self.position == other.position

    def draw_display(self) -> None:
        x, y = self.draw_position[0], self.draw_position[1]

        if self.is_wall():
            pygame.draw.rect(
                self.display, WALL_COLOR,
                pygame.Rect(x, y, self.width, self.width))

            return

        # Background square
        pygame.draw.rect(
            self.display, self.border_color,
            pygame.Rect(x, y, self.width, self.width))

        # Foreground square
        pygame.draw.rect(
            self.display, self.color,
            pygame.Rect(
                x + FOREGROUND_PADDING,
                y + FOREGROUND_PADDING,
                self.width - FOREGROUND_PADDING,
                self.width - FOREGROUND_PADDING))

    def set_color(self, color: Color) -> None:
        self.color = color
        self.draw_display()

    def draw_as_circle(self, color: Color) -> None:
        x, y = self.draw_position[0], self.draw_position[1]

        self.color = color
        
        center = \
            (x + self.width / 2 + FOREGROUND_PADDING, 
            y + self.width / 2 + FOREGROUND_PADDING)

        pygame.draw.circle(
            self.display,
            color,
            center,
            self.width / 2,
        )

    def set_wall(self) -> None:
        self._is_wall = True
        self.draw_display()

    def unset_wall(self) -> None:
        self._is_wall = False
        self.draw_display()

    def clear_node(self) -> None:
        self.color = NODE_COLOR
        self.draw_display()

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
