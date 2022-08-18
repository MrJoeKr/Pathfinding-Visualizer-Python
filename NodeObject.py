import pygame

SQUARE_SIZE = 15
FOREGROUND_PADDING = 1
WHITE = (255,255,255)
BLACK = (0,0,0)

Color = tuple[int, int, int]

class Node(): 
    # Class for nodes -> squares on the board
    def __init__(self, parent: "Node"=None, position: tuple[int, int]=None):
        self.parent = parent
        self.position = position

        self.width = SQUARE_SIZE
        self.color = WHITE

        self.draw_position = \
            (position[0] * self.width, 
            position[1] * self.width)

        # For A* algorithm
        # f = g + h
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: "Node") -> bool:
        # check equality with another node
        return self.position == other.position

    def draw_display(self, display: pygame.display) -> None:
        x, y = self.draw_position[0], self.draw_position[1]

        # Background square
        pygame.draw.rect(
            display, BLACK,
            pygame.Rect(x, y, self.width, self.width))

        # Foreground square
        pygame.draw.rect(
            display, self.color, 
            pygame.Rect(
                x + FOREGROUND_PADDING, 
                y + FOREGROUND_PADDING,
                self.width - FOREGROUND_PADDING, 
                self.width - FOREGROUND_PADDING))

    def set_color(self, color: Color) -> None:
        self.color = color

    # TO BE REMOVED FUNCTIONS
    def get_rect(self) -> pygame.Rect:
        # x = self.position[1] * 18 + 5 
        # y = self.position[0] * 18 + 5
        x, y = self.draw_position[0], self.draw_position[1]
        return pygame.Rect(x ,y, self.width, self.width)

    def get_pos(self):
        x = self.position[1] * 18 + 5 
        y = self.position[0] * 18 + 5
        return (x,y)