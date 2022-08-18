import pygame
import numpy as np
import time
import threading
from typing import List, Optional
# Project files
import tkinterWindow
from NodeObject import Node
import NodeObject

pygame.init() # initializing

myfont = pygame.font.SysFont('Arial', 40)
font_small = pygame.font.SysFont('Arial', 20)

WIDTH = 800
HEIGTH = 650
DISPLAY = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption('A* path finder')
mainClock = pygame.time.Clock()

BOTTOM_PANEL_HEIGHT = 50

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,242,0)
RED = (231,0,0)
LIGHT_GREEN = (126, 186, 0)
BLUE = (94, 182, 202)
LIGHTER_GREEN = (15, 216, 92)
DARK_BLUE = (0, 0, 111)

# global variables
children_rects = []
closed_rects = []
show_steps = False
show_steps_choosed = False
impossible = False
start_value = 0
wait = False
path = []

def draw_text(x,y, text, color):
    the_text = myfont.render(text, False, color)
    DISPLAY.blit(the_text,(x,y))

def draw_text_small(x,y, text, color):
    the_text = font_small.render(text, False, color)
    DISPLAY.blit(the_text,(x,y))

# A* algorithm  
def return_path(current_node, maze):
    global start_value
    global wait
    global path
    # returns the path of the search function
    path = []
    num_rows, num_cols = np.shape(maze) # the shape of maze
    result = [[-1 for i in range(num_cols)] for j in range(num_rows)]
    current = current_node
    while current is not None: # loops until the end node
        path.append(current.position)
        current = current.parent

    path = path[::-1] # reverse path - we went from end to start so we have to reverse it
    start_value = 0

    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1

    # global variables
    path = list(result)
    wait = True
    return result

def search(maze, start, end): # cost -> value of one transition
    global impossible

    start = [start[1],start[0]]
    end = [end[1],end[0]]
    start_node = Node(None, tuple(start))
    start_node.g = start_node.f = start_node.h = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.f = end_node.h = 0

    open_list = [] # list with unvisited nodes 
    closed_list = [] # list with visited nodes

    open_list.append(start_node)

    num_rows, num_cols = np.shape(maze) # number of rows and columns of maze

    # all possible moves from one square to another
    moves = [
    [0,-1], # up
    [1,0], # right
    [0,1], # down
    [-1,0], # left
    [1,-1], # up right
    [1,1], # down right
    [-1,1], # down left
    [-1,-1] # up left
    ]

    # loop to end node
    while len(open_list) > 0:
                
        current_node = open_list[0]
        current_index = 0
        for index,item in enumerate(open_list): # find 'the best' node
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        if current_node not in closed_list:
            closed_list.append(current_node)

        if current_node == end_node: # found end node
            return return_path(current_node, maze)

        # create children from all adjacent squares
        children = []

        for move in moves:
            
            node_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

            # check if possible (boundaries)
            if (node_position[0] > (num_rows - 1)) or node_position[0] < 0 \
            or node_position[1] > ((num_cols - 1) or node_position[1] < 0):
                continue

            if node_position[0] < 0 or node_position[1] < 0:
                continue

            # walls -> 1-s
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # create new children node
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:

            # check if in closed list
            if child in closed_list:
                continue

            #change the value of cost when diagonal child
            cost = 1
            if current_node.position[0] - child.position[0] != 0 and current_node.position[1] - child.position[1] != 0:
                cost = 2

            # otherwise create initialize values
            child.g = current_node.g + cost
            #child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            #child.h = max([abs(current_node.position[0] - end_node.position[0]),abs(current_node.position[1] - end_node.position[1])])
            child.h = abs(current_node.position[0] - end_node.position[0]) + abs(current_node.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # check if child is already in open_list and g is already lower
            #if len([i for i in open_list if child == i and child.g > i.g]) > 0:
            #    continue

            # add children to open list and loop again
            if child not in open_list:
                open_list.append(child)

    if len(open_list) == 0:
        impossible = True

def search_with_steps(maze,start,end):

    global children_rects
    global closed_rects
    global impossible

    start = [start[1],start[0]]
    end = [end[1],end[0]]
    start_node = Node(None, tuple(start))
    start_node.g = start_node.f = start_node.h = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.f = end_node.h = 0

    open_list = [] # list with unvisited nodes 
    closed_list = [] # list with visited nodes
    child_pos_list = []
    done_pos_list = []


    open_list.append(start_node)

    num_rows, num_cols = np.shape(maze) # number of rows and columns of maze

    # all possible moves from one square to another
    moves = [
    [0,-1], # up
    [1,0], # right
    [0,1], # down
    [-1,0], # left
    [1,-1], # up right
    [1,1], # down right
    [-1,1], # down left
    [-1,-1] # up left
    ]

    children_rects = [] # for drawing possible children
    closed_rects = []

    # loop to end node
    while len(open_list) > 0:
                
        current_node = open_list[0]
        current_index = 0
        for index,item in enumerate(open_list): # find 'the best' node
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        if current_node not in closed_list:
            closed_list.append(current_node)

        if current_node == end_node: # found end node
            return return_path(current_node, maze)

        # create children from all adjacent squares
        children = []

        for move in moves:
            
            node_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

            # check if possible (boundaries)
            if (node_position[0] > (num_rows - 1)) or node_position[0] < 0 \
            or node_position[1] > ((num_cols - 1) or node_position[1] < 0):
                continue

            if node_position[0] < 0 or node_position[1] < 0:
                continue

            # walls -> 1-s
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # create new children node
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:

            # check if in closed list
            if child in closed_list:
                continue

            #change the value of cost when diagonal child
            cost = 1
            if current_node.position[0] - child.position[0] != 0 and current_node.position[1] - child.position[1] != 0:
                cost = 2

            # otherwise create initialize values
            child.g = current_node.g + cost
            #child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            child.h = max([abs(current_node.position[0] - end_node.position[0]),abs(current_node.position[1] - end_node.position[1])])
            #child.h = abs(current_node.position[0] - end_node.position[0]) + abs(current_node.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # check if child is already in open_list and g is already lower
            #if len([i for i in open_list if child == i and child.g > i.g]) > 0:
            #    continue

            # add children to open list and loop again
            if child not in open_list:
                open_list.append(child)


        # draw children and closed rectangles
        for child in open_list:
            rect = child.get_rect()
            child_pos = child.get_pos()
            if child_pos not in child_pos_list:
                child_pos_list.append(child_pos)
                children_rects.append(rect)

        for done in closed_list:
            done_rect = done.get_rect()
            done_pos = done.get_pos()
            
            if done_pos not in done_pos_list:
                done_pos_list.append(done_pos)
                closed_rects.append(done_rect)
            else:
                pass

        time.sleep(0.01)

    if len(open_list) == 0:
        impossible = True
    


# environment

def plain(x,y):
    a = 15
    plain_rect = pygame.Rect(x,y,a,a)
    return plain_rect

def draw_plain(plain_rect):
    pygame.draw.rect(DISPLAY,WHITE,plain_rect)

def wall(x,y):
    a = 15
    wall_rect = pygame.Rect(x,y,a,a)
    return wall_rect

def draw_wall(wall_rect):
    pygame.draw.rect(DISPLAY,BLACK,wall_rect)

def draw_point(x, y, color):
    a = 15
    point_rect = pygame.Rect(x,y,a,a)
    pygame.draw.rect(DISPLAY,color,point_rect)
    return point_rect

def get_point_pos(point_rect):
    x = (point_rect.x-5) // 18
    y = (point_rect.y-5) // 18
    return (x,y)

def init_draw_board(rows: int, cols: int) -> List[List[Node]]:
    out = []
    for y in range(rows):
        sub = []
        out.append(sub)
        for x in range(cols):
            node = Node(parent=None, position=(x, y))
            sub.append(node)
            node.draw_display(DISPLAY)
    
    return out

def run_app():
    global children_rects
    global closed_rects
    global show_steps
    global show_steps_choosed
    global impossible
    global start_value
    global wait

    running = True
    plains = []
    sub_plains = []
    walls = []
    points = []
    path_list = []
    CLEAR = True
    choose_start = True
    choose_end = False
    choose_walls = False
    choose_steps = True
    start_choosed = False
    end_choosed = False
    once = True
    show_steps = False
    second = False
    count_blocks = False
    
    rows = 40
    cols = 53
    # Initialize board
    DISPLAY.fill(BLACK)
    node_list = init_draw_board(rows, cols)

    while running:

        left_pressed, middle_pressed, right_pressed = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        
        # Create a list of plain rects and then draws them
        if CLEAR:
            for i in range(33):
                for j in range(44):
                    plain_rect = plain(5+j*18,5+i*18)
                    sub_plains.append(plain_rect)

            maze_1d = [0 for i in range(44*33)]
            plains = list(sub_plains)
            CLEAR = False

        #draws them
        # for rect in plains:
        #     draw_plain(rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if left_pressed: 
                # Choose start and end point
                node_x = mx // NodeObject.SQUARE_SIZE
                node_y = my // NodeObject.SQUARE_SIZE
                node: Optional[Node] = None

                if node_y < rows and node_x < cols:
                    node = node_list[node_y][node_x]

                if node is not None:
                    if choose_start: # renders text 'Choose starting point', gives ability to choose it
                        choose_start = False
                        choose_end = True
                        # start_rect = draw_point(node.x,node.y,GREEN)
                        # start_rect_pos = plains.index(node)
                        # plains[start_rect_pos] = start_rect

                        start_rect = node.get_rect()
                        node.set_color(GREEN)
                        node.draw_display(DISPLAY)

                    elif choose_end:
                        # end_rect_pos = plains.index(node)
                        end_rect = node.get_rect()
                        if start_rect != end_rect:
                            choose_end = False
                            end_choosed = True
                            choose_walls = True
                            # end_rect = draw_point(node.x,node.y,RED)
                            # plains[end_rect_pos] = end_rect

                            node.set_color(RED)
                            node.draw_display(DISPLAY)
                                

                    # left click - drawing walls
                    # TODO -> Finish
                    elif choose_walls:
                        node.set_color(BLACK)
                        node.draw_display(DISPLAY)

                        # for pl in plains:
                        #     if pl.collidepoint(mx,my):
                                # wall_pos = plains.index(pl)

                                # if wall_pos != end_rect_pos and wall_pos != start_rect_pos:
                                #     maze_1d[wall_pos] = 1
                                #     wall_rect = wall(pl.x,pl.y)
                                #     walls.append(wall_rect)
                                #     left_pressed = False
                                
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: # clear walls and remake plains - list
                    walls.clear()
                    plains.clear()
                    path_list.clear()
                    children_rects.clear()
                    closed_rects.clear()
                    global path
                    CLEAR = True

                    choose_start = True
                    choose_end = False
                    once = True
                    start_choosed = False
                    end_choosed = False
                    choose_steps = True
                    show_steps_choosed = False
                    show_steps = False
                    path = None
                    wait = False
                    impossible = False
                    start_value = 0
                    count_blocks = False

                if end_choosed and show_steps_choosed:
                    if event.key == pygame.K_SPACE: # Start A* algorithm
                        
                        #shape the maze
                        start = get_point_pos(start_rect)
                        end = get_point_pos(end_rect)
                        maze_2d = np.reshape(maze_1d,(33,44))

                        # algorithm
                        if show_steps:
                            path = threading.Thread(target=search_with_steps,args=(maze_2d, start, end))
                            path.start()
                            choose_walls = False
                        else:
                            choose_walls = False
                            path = search(maze_2d, start, end)


        # texts
        if choose_start:
            pygame.draw.rect(DISPLAY, BLACK, pygame.Rect(0, HEIGTH - BOTTOM_PANEL_HEIGHT, WIDTH, BOTTOM_PANEL_HEIGHT))
            draw_text(10,600,'Choose your start point',GREEN)
        if choose_end:
            pygame.draw.rect(DISPLAY, BLACK, pygame.Rect(0, HEIGTH - BOTTOM_PANEL_HEIGHT, WIDTH, BOTTOM_PANEL_HEIGHT))
            draw_text(10,600,'Choose your end point',RED)
        if choose_walls:
            pygame.draw.rect(DISPLAY, BLACK, pygame.Rect(0, HEIGTH - BOTTOM_PANEL_HEIGHT, WIDTH, BOTTOM_PANEL_HEIGHT))
            draw_text(10,600,'Draws walls or hit SPACE to start',WHITE)


        # draws walls
        for wl in walls:
            draw_wall(wl)

        # if end_choosed: 
        #     pygame.draw.rect(DISPLAY,RED,end_rect)

        # when showing steps
        for child in children_rects:
                pygame.draw.rect(DISPLAY,BLUE,child)

        for done in closed_rects:
            pygame.draw.rect(DISPLAY,(203, 253, 0),done)

        #create path in GUI
        if not impossible:
            if wait: 
                for row in path:
                    for num in row:
                        if num > 0:
                            y = path.index(row) * 18 + 5
                            x = row.index(num) * 18 + 5
                            path_rect = draw_point(x,y,LIGHT_GREEN)
                            path_list.append(path_rect)
                    done = False
                    count_blocks = True
            
            if count_blocks:
                draw_text(10,600,f'The shortest path is {start_value-1} blocks long.',GREEN)
                draw_text_small(650,600,'Press BACKSPACE',WHITE)
                draw_text_small(658,622,'to reset the board',WHITE)
        else:
            draw_text(10,600,'Path is not possible to be found',RED)
        
        # when done
        if path_list:
            pygame.draw.rect(DISPLAY,GREEN,start_rect)
            for rect in path_list:
                if rect.x == end_rect.x and rect.y == end_rect.y:
                    pygame.draw.rect(DISPLAY,DARK_BLUE,rect)
                else:
                    pygame.draw.rect(DISPLAY,GREEN,rect)
                
                

        pygame.display.update()
        mainClock.tick(60)

        if choose_steps:
            # tick box
            tkinterWindow.tick_box_window()
            choose_steps = False


# TODO: REMOVE
if __name__ == "__main__":
    run_app()