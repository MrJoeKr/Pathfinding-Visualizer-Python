from typing import Callable, List, Optional, Tuple, Deque

# Priority queue
from heapq import heappop, heappush
from collections import deque
import random
import math

from library.node.board import NodeBoard
from library.node.draw_queue import NodeQueue
from library.node.node import Node, DEFAULT_FLAG_VALUE

Board = List[List[Node]]
HeuristicFunction = Callable[[Node, Node], float]
PathList = List[Node]
SearchFunction = Callable[[NodeBoard, Optional[NodeQueue], HeuristicFunction], None]

# Flags for DFS
WHITE = DEFAULT_FLAG_VALUE
GRAY = 1
BLACK = 2


def manhattan_distance(a: Node, b: Node) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def euclidian_distance(node_a: Node, node_b: Node) -> float:
    return math.sqrt((node_a.x - node_b.x) ** 2 + (node_a.y - node_b.y) ** 2)


# Return different bits of x and y coordinates
def hamming_distance(a: Node, b: Node) -> int:
    return different_bits_count(a.x, b.x) + different_bits_count(a.y, b.y)


def different_bits_count(n: int, m: int) -> int:
    return str(bin(n ^ m)).count("1")


# Find path from start to end node using A* star
def search_a_star(
    board: NodeBoard, draw_queue: Optional[NodeQueue], heuristic: HeuristicFunction
) -> None:

    # Depth is variable that ensures if f-values are same,
    # nodes in bigger depth (smaller value) are traversed first
    depth = board.rows * board.cols

    # Init priority queue
    # (node.f, depth, node.y, node.x)
    heap: List[Tuple[int, int, int]] = [
        (0, depth, board.start_node.y, board.start_node.x)
    ]
    board.start_node.g = 0

    while heap:

        tup: Tuple[int, int, int] = heappop(heap)
        _, _, node_y, node_x = tup

        # Inverted -> decrease to prioritize more
        depth -= 1

        node = board.get_node(node_y, node_x)

        # Best node so far
        if draw_queue is not None:
            draw_queue.push_closed_node(node)

        if node == board.end_node:
            board.process_path_list()
            return

        child_nodes: List[Node] = board.get_node_neighbours(
            node, predicate=lambda child: child.g > node.g + 1 and not child.is_wall()
        )

        # Valid nodes
        for child_node in child_nodes:

            child_node.parent = node
            child_node.g = node.g + 1
            f = child_node.g + heuristic(child_node, board.end_node)

            # print(f"Pushing: {(f, child_node.y, child_node.x)}")

            heappush(heap, (f, depth, child_node.y, child_node.x))

            if draw_queue is not None:
                draw_queue.push_open_node(child_node)

    # No path found
    return


def search_dijkstra(
    board: NodeBoard, draw_queue: Optional[NodeQueue], _: HeuristicFunction
) -> None:

    search_dijkstra_help(board, draw_queue, lambda: 1)


def bogo_search(
    board: NodeBoard, draw_queue: Optional[NodeQueue], _: HeuristicFunction
) -> None:

    search_dijkstra_help(board, draw_queue, lambda: random.randrange(1, 10**6))


def search_dijkstra_help(
    board: NodeBoard, draw_queue: Optional[NodeQueue], cost_to_next: Callable[[], int]
) -> None:

    # (cost_so_far, x, y)
    min_heap: List[Tuple[int, int, int]] = [(0, board.start_node.x, board.start_node.y)]

    board.start_node.visited = True

    while min_heap:
        
        cost, x, y = heappop(min_heap)

        node = board.get_node(y, x)

        if node is board.end_node:
            board.process_path_list()
            return

        _push_closed_node(draw_queue, node)

        children = board.get_node_neighbours(node, lambda child: not child.is_wall() and not child.visited)

        for child in children:
            
            child.visited = True
            child.parent = node

            heappush(min_heap, (cost + cost_to_next(), child.x, child.y))

            _push_open_node(draw_queue, child)


# Search using DFS method
def search_dfs(
    board: NodeBoard, draw_queue: Optional[NodeQueue], _: HeuristicFunction
) -> None:

    _dfs_stack(board, draw_queue)


def _dfs_stack(board: NodeBoard, draw_queue: Optional[NodeQueue]) -> None:

    # Help lambda function
    get_children = lambda node: board.get_node_neighbours(
        node, lambda child: not child.is_wall()
    )

    # [(node, children left)]
    stack: List[Tuple[Node, List[Node]]] = [
        (board.start_node, get_children(board.start_node))
    ]

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
                draw_queue.push_closed_node(node)

            continue

        if draw_queue is not None:
            draw_queue.push_open_node(node)

        # Traverse child
        while children_left:

            child = children_left.pop()

            if child.flag == WHITE and not child.is_wall():

                child.parent = node
                stack.append((child, get_children(child)))
                break


# Recursive method -> not used (exceeds default recursion limit)
def _dfs_help(node: Node, board: NodeBoard, draw_queue: Optional[NodeQueue]) -> bool:

    if node is board.end_node:
        board.process_path_list()
        return True

    node.flag = GRAY

    if draw_queue is not None:
        draw_queue.push_open_node(node)

    for child in board.get_node_neighbours(node):

        if child.is_wall() or child.flag != WHITE:
            continue

        child.parent = node

        if _dfs_help(child, board, draw_queue):
            return True

    node.flag = BLACK

    if draw_queue is not None:
        draw_queue.push_closed_node(node)

    return False


# Search using BFS method
def search_bfs(
    board: NodeBoard,
    draw_queue: Optional[NodeQueue],
    # Heuristic not used
    _: HeuristicFunction,
) -> None:

    queue: Deque[Node] = deque()

    queue.append(board.start_node)
    board.start_node.visited = True

    while queue:

        node = queue.popleft()

        if node is board.end_node:
            board.process_path_list()
            return

        if draw_queue is not None:
            draw_queue.push_closed_node(node)

        child_nodes = board.get_node_neighbours(
            node, lambda child: not child.visited and not child.is_wall()
        )

        for child_node in child_nodes:

            child_node.parent = node
            child_node.visited = True

            queue.append(child_node)

            if draw_queue is not None:
                draw_queue.push_open_node(child_node)


def _push_open_node(draw_queue: Optional[NodeQueue], node: Node):
    if draw_queue is None:
        return

    draw_queue.push_open_node(node)


def _push_closed_node(draw_queue: Optional[NodeQueue], node: Node):
    if draw_queue is None:
        return

    draw_queue.push_closed_node(node)


_PATH_ALGORITHMS: List[Tuple[str, SearchFunction]] = [
    ("A Star Search", search_a_star),
    ("Dijkstra's Algorithm", search_dijkstra),
    ("Breadth First Search", search_bfs),
    ("Depth First Search", search_dfs),
    ("Bogo Search", bogo_search),
]

_HEURISTICS: List[Tuple[str, HeuristicFunction]] = [
    ("Manhattan Distance", manhattan_distance),
    ("Euclidian Distance", euclidian_distance),
    ("Hamming Distance", hamming_distance),
]


def get_algorithms_list() -> List[Tuple[str, SearchFunction]]:
    return _PATH_ALGORITHMS


def get_heuristics_list() -> List[Tuple[str, HeuristicFunction]]:
    return _HEURISTICS
