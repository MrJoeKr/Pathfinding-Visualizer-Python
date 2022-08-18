import pygame

SQUARE_SIZE = 15
WHITE = (255,255,255)

Color = tuple[int, int, int]

class Node(): 
    # Class for nodes -> squares on the board
    def __init__(self, parent: "Node"=None, position: tuple[int, int]=None):
        self.parent = parent
        self.position = position

        self.width = SQUARE_SIZE
        self.color = WHITE

        # For A* algorithm
        # f = g + h
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: "Node") -> bool:
        # check equality with another node
        return self.position == other.position

    def draw_rect(self, display: pygame.display) -> None:
        x, y = self.position[0], self.position[1]
        pygame.draw.rect(
            display, self.color, pygame.Rect(x, y, self.width, self.width)) 

    def set_color(self, color: Color) -> None:
        self.color = color

    # TO BE REMOVED FUNCTIONS
    def get_rect(self) -> pygame.Rect:
        x = self.position[1] * 18 + 5 
        y = self.position[0] * 18 + 5
        rect = pygame.Rect(x ,y, self.width, self.width)
        return rect

    def get_pos(self):
        x = self.position[1] * 18 + 5 
        y = self.position[0] * 18 + 5
        return (x,y)