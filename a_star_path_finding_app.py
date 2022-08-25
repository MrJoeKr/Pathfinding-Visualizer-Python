import pygame

# Project files
from node_board_object import NodeBoard
from board_window import BoardWindow
from color_constants import *
from config_constants import *
from path_finding_algorithm import search_path


# Initialize pygame
pygame.init()

myfont = pygame.font.SysFont('Arial', 40)
font_small = pygame.font.SysFont('Arial', 20)

DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGTH))
pygame.display.set_caption('A* path finder')
mainClock = pygame.time.Clock()


def draw_text(x,y, text, color):
    the_text = myfont.render(text, False, color)
    DISPLAY.blit(the_text,(x,y))

def draw_text_small(x,y, text, color):
    the_text = font_small.render(text, False, color)
    DISPLAY.blit(the_text,(x,y))


def run_app():
    running = True
    
    DISPLAY.fill(BLACK)

    # Initialize window object
    app_window = BoardWindow(DISPLAY, ROWS, COLS)

    board = app_window.get_node_board()

    while running:

        app_window.process_mouse_events()

        # Process keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                    
            if event.type == pygame.KEYDOWN:
                
                # Quit with escape
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()

                # Reset board
                if event.key == pygame.K_BACKSPACE:
                    
                    board.start_node = None
                    board.end_node = None
                    # TODO : Not working properly
                    board = NodeBoard(DISPLAY, ROWS, COLS)

                # Start the algorithm
                if board.end_node is not None and event.key == pygame.K_SPACE:
                    print("starting algorithm")
                    path = search_path(board, show_steps=True)
                    print("Done")

        # Texts for drawing
        # if board.start_node is None:
        #     pygame.draw.rect(DISPLAY, BLACK, pygame.Rect(0, HEIGTH - BOTTOM_PANEL_HEIGHT, WIDTH, BOTTOM_PANEL_HEIGHT))
        #     draw_text(10, 600, 'Choose your start point', GREEN)
        # elif board.end_node is None:
        #     pygame.draw.rect(DISPLAY, BLACK, pygame.Rect(0, HEIGTH - BOTTOM_PANEL_HEIGHT, WIDTH, BOTTOM_PANEL_HEIGHT))
        #     draw_text(10, 600, 'Choose your end point', RED)
        # elif board.end_node is not None:
        #     pygame.draw.rect(DISPLAY, BLACK, pygame.Rect(0, HEIGTH - BOTTOM_PANEL_HEIGHT, WIDTH, BOTTOM_PANEL_HEIGHT))
        #     draw_text(10, 600, 'Draws walls or hit SPACE to start', WHITE)


        # # draws walls
        # for wl in walls:
        #     draw_wall(wl)

        # if end_choosed: 
        #     pygame.draw.rect(DISPLAY,RED,end_rect)

        # # when showing steps
        # for child in children_rects:
        #         pygame.draw.rect(DISPLAY,BLUE,child)

        # for done in closed_rects:
        #     pygame.draw.rect(DISPLAY,(203, 253, 0),done)

        #create path in GUI
        # if not impossible:
        #     if wait: 
        #         for row in path:
        #             for num in row:
        #                 if num > 0:
        #                     y = path.index(row) * 18 + 5
        #                     x = row.index(num) * 18 + 5
        #                     path_rect = draw_point(x,y,LIGHT_GREEN)
        #                     path_list.append(path_rect)
        #             done = False
        #             count_blocks = True
            
        #     if count_blocks:
        #         draw_text(10,600,f'The shortest path is {start_value-1} blocks long.',GREEN)
        #         draw_text_small(650,600,'Press BACKSPACE',WHITE)
        #         draw_text_small(658,622,'to reset the board',WHITE)
        # else:
        #     draw_text(10,600,'Path is not possible to be found',RED)
        
        # when done
        # if path_list:
        #     pygame.draw.rect(DISPLAY,GREEN,start_rect)
        #     for rect in path_list:
        #         if rect.x == end_rect.x and rect.y == end_rect.y:
        #             pygame.draw.rect(DISPLAY,DARK_BLUE,rect)
        #         else:
        #             pygame.draw.rect(DISPLAY,GREEN,rect)
                
                
        pygame.display.update()
        mainClock.tick(60)

        # if choose_steps:
        #     # tick box
        #     tkinterWindow.tick_box_window()
        #     choose_steps = False


# TODO: REMOVE
if __name__ == "__main__":
    run_app()