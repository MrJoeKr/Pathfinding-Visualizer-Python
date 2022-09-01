from typing import Callable, List, Optional, Tuple, Deque
# Priority queue
from heapq import heappop, heappush
from collections import deque
import threading
import time
import math

from node_board_object import NodeBoard
from node_object import Node, DEFAULT_FLAG_VALUE
from config_constants import OPEN_NODES_COLOR, CLOSED_NODES_COLOR, SHOW_STEPS_DELAY, MOVES
from config_constants import START_POINT_COLOR, END_POINT_COLOR
from color_constants import Color

Board = List[List[Node]]
HeuristicFunction = Callable[[Node, Node], int]
PathList = List[Node]
DrawDeque = Deque[Tuple[Color, Node]]
SearchFunction = Callable[[NodeBoard, Optional[DrawDeque], HeuristicFunction], None]

# Flags for DFS
WHITE = DEFAULT_FLAG_VALUE
GRAY = 1
BLACK = 2

def manhattan_distance(node_a: Node, node_b: Node) -> int:
    return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)

def euclidian_distance(node_a: Node, node_b: Node) -> float:
    return math.sqrt((node_a.x - node_b.x)**2 + (node_a.y - node_b.y)**2)

# Return different bits of x and y coordinates
def hamming_distance(a: Node, b: Node) -> int:
    return different_bits_count(a.x, b.x) + different_bits_count(a.y, b.y)

def different_bits_count(n: int, m: int) -> int:
    return str(bin(n ^ m)).count("1")

# Find path from start to end node using A* star
def search_a_star(
        board: NodeBoard,
        draw_queue: Optional[DrawDeque],
        heuristic: HeuristicFunction) -> None:

    # Init priority queue
    # (node.f, node.y, node.x)
    heap: List[Tuple[int, int, int]] = [(0, board.start_node.y, board.start_node.x)]
    board.start_node.g = 0

    while heap:

        tup: Tuple[int, int, int] = heappop(heap)
        _, node_y, node_x = tup

        node = board.get_node(node_y, node_x)
        
        # Best node so far
        if draw_queue is not None:
            draw_queue.append((CLOSED_NODES_COLOR, node))

        if node == board.end_node:
            board.process_path_list()
            return

        child_nodes: List[Node] = \
            board.get_node_neighbours(
                node, 
                predicate=lambda child: child.g > node.g + 1 and not child.is_wall())

        # Valid nodes
        for child_node in child_nodes:

            child_node.parent = node
            child_node.g = node.g + 1
            f = child_node.g + heuristic(child_node, board.end_node)

            heappush(heap, (f, child_node.y, child_node.x))

            if draw_queue is not None:
                draw_queue.append((OPEN_NODES_COLOR, child_node))

    # No path found
    return

# Search using DFS method
def search_dfs(
        board: NodeBoard,
        draw_queue: Optional[DrawDeque],
        _: HeuristicFunction) -> None:

    _dfs_stack(board, draw_queue)


def _dfs_stack(
    board: NodeBoard,
    draw_queue: Optional[DrawDeque]) -> None:
    
    # Help lambda function
    get_children = \
        lambda node: board.get_node_neighbours(node, lambda child: not child.is_wall())

    # [(node, children left)]
    stack: List[Tuple[Node, List[Node]]] = \
        [(board.start_node, get_children(board.start_node))]

    while stack:

        node, children_left = stack[-1]

        if node is board.end_node:
            board.process_path_list()
            return

        node.flag = GRAY

        # No children -> end node traversing
        if not children_left:
            node.flag = BLACK
            stack.pop()

            if draw_queue is not None:
                draw_queue.append((CLOSED_NODES_COLOR, node))

            continue
        
        if draw_queue is not None:
            draw_queue.append((OPEN_NODES_COLOR, node))

        # Traverse child
        while children_left:

            child = children_left.pop()

            if child.flag == WHITE and not child.is_wall():

                child.parent = node
                stack.append((child, get_children(child)))
                break

# Recursive method -> not used (exceeds default recursion limit)
def _dfs_help(
    node: Node,
    board: NodeBoard,
    draw_queue: Optional[DrawDeque]) -> bool:

    if node is board.end_node:
        board.process_path_list()
        return True

    node.flag = GRAY

    if draw_queue is not None:
        draw_queue.append((OPEN_NODES_COLOR, node))

    for child in board.get_node_neighbours(node):

        if child.is_wall() or child.flag != WHITE:
            continue

        child.parent = node

        if _dfs_help(child, board, draw_queue):
            return True

    node.flag = BLACK

    if draw_queue is not None:
        draw_queue.append((CLOSED_NODES_COLOR, node))


    return False


# Search using BFS method
def search_bfs(
        board: NodeBoard,
        draw_queue: Optional[DrawDeque],
        # Heuristic not used
        _: HeuristicFunction) -> None:

    queue: Deque[Node] = deque()

    queue.append(board.start_node)
    board.start_node.visited = True

    while queue:

        node = queue.popleft()

        if node is board.end_node:
            board.process_path_list()
            return

        if draw_queue is not None:
            draw_queue.append((CLOSED_NODES_COLOR, node))

        child_nodes = \
            board.get_node_neighbours(
                node,
                lambda child: not child.visited and not child.is_wall()
            ) 

        for child_node in child_nodes:

            child_node.parent = node
            child_node.visited = True

            queue.append(child_node)

            if draw_queue is not None:
                draw_queue.append((OPEN_NODES_COLOR, child_node))


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

            # TODO -> make pop up animation better
            # node.draw_pop_up_animation(color)

            node.draw_node(color)

            if node is board.start_node:
                node.draw_as_circle(START_POINT_COLOR)

            if node is board.end_node:
                node.draw_as_circle(END_POINT_COLOR)

            # Speed of drawing
            time.sleep(SHOW_STEPS_DELAY)

    board.finding_path_finished = True


_PATH_ALGORITHMS: List[Tuple[str, SearchFunction]] = \
    [
        ("A Star", search_a_star),
        ("Breadth First Search", search_bfs),
        ("Depth First Search", search_dfs),
    ]

_HEURISTICS: List[Tuple[str, HeuristicFunction]] = \
    [
        ("Euclidian Distance", euclidian_distance),
        ("Manhattan Distance", manhattan_distance),
        ("Hamming Distance", hamming_distance),
    ]


def get_algorithms_list() -> List[Tuple[str, SearchFunction]]:
    return _PATH_ALGORITHMS


def get_heuristics_list() -> List[Tuple[str, HeuristicFunction]]:
    return _HEURISTICS