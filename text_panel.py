import pygame
from color_constants import Color

class TextPanel:

    def __init__(self, display: pygame.display, x: int, y: int, width: int, height: int, background_color: Color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.display = display
        self.background_color = background_color

        self._update_rect = pygame.Rect(x, y, width, height)
        
        # Default font
        self.font = pygame.font.SysFont('Arial', 40)

        self.draw_display()

    def update_display(self) -> None:
        pygame.display.update(self._update_rect)

    def draw_display(self) -> None:
        pygame.draw.rect(
            self.display,
            self.background_color,
            pygame.Rect(self.x, self.y, self.width, self.height),
        )

        self.update_display()

    def clear_panel(self):
        self.draw_display()

    # x and y are coords from top-left corner of the text panel
    def write_text(self, x: int, y: int, what: str, color: Color) -> None:
        the_text = self.font.render(what, False, color)
        self.display.blit(the_text, (x + self.x , y + self.y))

        self.update_display()