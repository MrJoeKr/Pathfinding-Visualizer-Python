from typing import Callable, List, Optional, Tuple, Deque
# Priority queue
from heapq import heappop, heappush
from collections import deque
import threading
import time
import pygame

from node_board_object import NodeBoard
from node_object import Node
from config_constants import OPEN_NODES_COLOR, CLOSED_NODES_COLOR, SHOW_STEPS_DELAY, MOVES
from color_constants import Color

Board = List[List[Node]]
HeuristicFunction = Callable[[Node, Node], int]
PathList = List[Node]
DrawDeque = Deque[Tuple[Color, Node]]
SearchFunction = Callable[[NodeBoard, Optional[DrawDeque], HeuristicFunction], None]


def manhattan_distance(node_a: Node, node_b: Node) -> int:
    return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)

def euclidian_distance(node_a: Node, node_b: Node) -> int:
    return int((node_a.x - node_b.x)**2 + (node_a.y - node_b.y)**2)

# Find path from start to end node using A* star
def search_a_star(
        board: NodeBoard,
        draw_queue: Optional[DrawDeque],
        heuristic: HeuristicFunction) -> None:

    # Init priority queue
    # (node.f, node.y, node.x)
    heap: List[Tuple[int, int, int]] = [(0, board.start_node.y, board.start_node.x)]
    board.start_node.visited = True

    rows, cols = board.rows, board.cols

    while heap:

        tup: Tuple[int, int, int] = heappop(heap)
        _, node_y, node_x = tup

        node = board.get_node(node_y, node_x)
        
        # Best node so far
        if draw_queue is not None:
            # print("Appending node")
            draw_queue.append((CLOSED_NODES_COLOR, node))

        if node == board.end_node:
            get_path_list(board.path, node)
            return

        for add_x, add_y in MOVES:
            
            x = node.x + add_x
            y = node.y + add_y
            
            # Invalid position
            if x < 0 or x >= cols \
                    or y < 0 or y >= rows:
                continue

            child_node = board.get_node(y, x)

            # Wall or was visited before
            if child_node.is_wall() or child_node.visited:
                continue
            
            # Valid node
            child_node.parent = node
            child_node.visited = True
            child_node.g = node.g + 1
            f = child_node.g + heuristic(child_node, board.end_node)

            heappush(heap, (f, y, x))

            if draw_queue:
                draw_queue.append((OPEN_NODES_COLOR, child_node))

    # No path found
    return

# Search using DFS method
def search_dfs(
        board: NodeBoard,
        draw_queue: Optional[DrawDeque],
        heuristic: HeuristicFunction) -> None:
    
    pass

# General function for finding path between two nodes in NodeBoard
def search_path(
        board: NodeBoard,
        show_steps: bool=False,
        search_func: SearchFunction=search_a_star,
        heuristic: HeuristicFunction=euclidian_distance) -> None:

    if not show_steps:
        # Threading not needed
        search_func(board, None, heuristic)

    else:
        draw_queue: DrawDeque = deque()

        thread = threading.Thread(
            target=search_func, args=(board, draw_queue, heuristic))
        thread.start()

        # Draw nodes
        while draw_queue:
            color, node = draw_queue.popleft()

            # print(f"Color : {color}")

            # TODO -> make pop up animation better
            # node.draw_pop_up_animation(color)
            node.draw_node(color)

            # Speed of drawing
            time.sleep(SHOW_STEPS_DELAY)

    board.finding_path_finished = True


def get_path_list(out_path_list: List[Node], end_node: Node) -> None:

    node: Optional[Node] = end_node

    while node is not None:
        out_path_list.append(node)
        node = node.parent

    out_path_list.reverse()


_PATH_ALGORITHMS: List[Tuple[str, SearchFunction]] = \
    [
        ("A Star", search_a_star),
        ("DFS", search_dfs)
    ]


def get_algorithms_list() -> List[Tuple[str, SearchFunction]]:
    return _PATH_ALGORITHMS