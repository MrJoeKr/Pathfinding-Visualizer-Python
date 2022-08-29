import pygame
import color_constants


FOREGROUND_PADDING = 2
BORDER_COLOR = color_constants.LIGHT_BLUE
BACKGROUND_COLOR = color_constants.WHITE
CROSS_WIDTH = 3

class TickBox:

    # A squared tick box
    def __init__(
            self, display: pygame.Surface, x: int, y: int, width: int) -> None:
        self.display = display

        self.x = x
        self.y = y
        self.width = width

        self.ticked = False

        self.foreground_padding = FOREGROUND_PADDING

        self._update_rect = pygame.Rect(x, y, width, width)

        self.draw_tick_box()

    def is_mouse_collision(self, mx: int, my: int) -> bool:
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.width

    def update_display(self) -> None:
        pygame.display.update(self._update_rect)

    # Draw tickbox on the display
    def draw_tick_box(self) -> None:

        # Background box
        background_rect = pygame.Rect(self.x, self.y, self.width, self.width)
        pygame.draw.rect(self.display, BORDER_COLOR, background_rect)

        # Foreground box
        foreground_rect = pygame.Rect(self.x + self.foreground_padding, 
                                      self.y + self.foreground_padding, 
                                      self.width - self.foreground_padding * 2,
                                      self.width - self.foreground_padding * 2)
        pygame.draw.rect(self.display, BACKGROUND_COLOR, foreground_rect)

        self.update_display()

    # Tick / untick box and return whether it's ticked
    def tick_untick_box(self) -> bool:

        # Switch boolean
        self.ticked = not self.ticked

        if not self.ticked:
            self.draw_tick_box()

        else:
            # Draw cross
            start_pos = \
                (self.x + self.foreground_padding, self.y + self.foreground_padding)

            end_pos = \
                (self.x + self.width - self.foreground_padding, self.y + self.width - self.foreground_padding)

            pygame.draw.line(self.display, color_constants.GREEN, start_pos, end_pos, width=CROSS_WIDTH)

            start_pos = \
                (self.x + self.foreground_padding, self.y - self.foreground_padding + self.width)

            end_pos = \
                (self.x + self.width - self.foreground_padding, self.y + self.foreground_padding)

            pygame.draw.line(self.display, color_constants.GREEN, start_pos, end_pos, width=CROSS_WIDTH)

        self.update_display()

        return self.ticked

    def is_ticked(self):
        return self.ticked
