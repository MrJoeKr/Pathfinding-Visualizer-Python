from typing import Callable, List, Optional, Tuple, Deque
# Priority queue
from heapq import heappop, heappush
from collections import deque
import threading
import time
import pygame

from node_board_object import NodeBoard
from node_object import Node
from config_constants import OPEN_NODES_COLOR, CLOSED_NODES_COLOR
from color_constants import Color

# all possible moves from one square to another
MOVES = [
    (0, -1),  # up
    (1, 0),  # right
    (0, 1),  # down
    (-1, 0),  # left
    (1, -1),  # up right
    (1, 1),  # down right
    (-1, 1),  # down left
    (-1, -1)  # up left
]

# The delay needs to be bigger than the time of the path-finding algorithm
SHOW_STEPS_DELAY = 0.008

Board = List[List[Node]]
Heuristic_Function = Callable[[Node, Node], int]
Path_List = List[Node]
Draw_Deque = Deque[Tuple[Color, Node]]
Search_Function = Callable[[NodeBoard, Path_List, Optional[Draw_Deque], Heuristic_Function], None]

def manhattan_distance(node_a: Node, node_b: Node) -> int:
    return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)


# # A thread function for drawing nodes
# def draw_steps(deque: Deque[Node], flag: List[bool]) -> None:

#     while True:
#         print("running")
#         while deque:
#             node = deque.popleft()

#             print(node.x, node.y)

#             node.draw_display()

#         if flag:
#             print(flag)
#             break


# Find path from start to end node using A* star
# Return path list
def search_a_star(
        board: NodeBoard,
        out_path_list: Path_List,
        draw_queue: Optional[Draw_Deque],
        heuristic: Heuristic_Function) -> None:

    # Init priority queue
    # (node.f, node.y, node.x)
    heap: List[Tuple[int, int, int]] = [(0, board.start_node.y, board.start_node.x)]
    board.start_node.visited = True

    rows, cols = len(board.get_board()), len(board.get_board()[0])

    while heap:

        tup: Tuple[int, int, int] = heappop(heap)
        _, node_y, node_x = tup

        node = board.get_board()[node_y][node_x]
        
        # Best node so far
        if draw_queue is not None:
            # print("Appending node")
            draw_queue.append((OPEN_NODES_COLOR, node))

        if node == board.end_node:
            get_path_list(out_path_list, node)
            return

        for add_x, add_y in MOVES:
            
            x = node.x + add_x
            y = node.y + add_y
            
            # Invalid position
            if x < 0 or x >= cols \
                    or y < 0 or y >= rows:
                continue

            child_node = board.get_board()[y][x]

            # Wall or was visited before
            if child_node.is_wall() or child_node.visited:
                continue
            
            # Valid node
            child_node.parent = node
            child_node.visited = True
            child_node.g = node.g + 1
            f = child_node.g + heuristic(node, board.end_node)
            heappush(heap, (f, child_node.y, child_node.x))

            if draw_queue:
                draw_queue.append((CLOSED_NODES_COLOR, child_node))

    # No path found
    return


def search_path(
        board: NodeBoard,
        show_steps: bool=False,
        search_func: Search_Function=search_a_star,
        heuristic: Heuristic_Function=manhattan_distance) -> List[Node]:

    path: Path_List = []

    if not show_steps:
        # Threading not needed
        search_func(board, path, None, heuristic)
        return path

    draw_queue: Draw_Deque = deque()

    thread = threading.Thread(
        target=search_func, args=(board, path, draw_queue, heuristic))
    thread.start()

    # Draw nodes
    while draw_queue:
        # print(f"Drawing node")
        color, node = draw_queue.popleft()

        node.set_color(color)

        # Update display
        pygame.display.update()

        # Speed of drawing
        time.sleep(SHOW_STEPS_DELAY)
    
    # print("Leaving search function")
    return path


def get_path_list(out_path_list: List[Node], end_node: Node) -> None:

    node: Optional[Node] = end_node

    while node is not None:
        out_path_list.append(node)
        node = node.parent

    out_path_list.reverse()