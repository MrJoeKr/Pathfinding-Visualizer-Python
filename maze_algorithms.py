import time
from typing import Callable, Deque, List, Optional, Tuple
from color_constants import Color
from node_board_object import NodeBoard
from node_draw_queue import NodeQueue
from path_finder import PathFinder
import random

from node_object import Node, DEFAULT_FLAG_VALUE
import color_constants
import config_constants

MazeFunction = Callable[[NodeBoard, NodeQueue], None]


# For DFS
WHITE = DEFAULT_FLAG_VALUE
GRAY = 1
BLACK = 2
# Lower bound of children added to search
_CHILDREN_LOWER_BOUND = 1


def randomized_dfs(board: NodeBoard, draw_queue: Optional[NodeQueue]) -> None:

    while True:

        # Set all nodes to walls
        board.map_nodes(lambda node: node.set_wall(update_screen=False))

        # Dfs through unvisited nodes
        _dfs_help(board, board.start_node, draw_queue)
        board.map_nodes(lambda node: _dfs_help(board, node, draw_queue))
        
        maze_finished = PathFinder(show_steps=False).start_search(board)

        board.clear_solution(update_screen=False)

        if maze_finished:
            break
        
        # Maze not found
        if draw_queue is not None:
            draw_queue.clear()
            # Reset flags
            board.map_nodes(lambda node: node.clear_flags())

    while not draw_queue.empty():
        # Prevent lag
        time.sleep(0.1)
        continue

    draw_queue.stop_visualizing()


def _dfs_help(board: NodeBoard, start_node: Node, draw_queue: Optional[NodeQueue]) -> None:

    if start_node.flag != WHITE:
        return

    # Help lambda function
    # get_children = lambda node: board.get_node_neighbours(node)
    get_children = lambda node: _node_children_dfs(board, node)

    children_left = get_children(start_node)

    # [(node, children left)]
    stack: List[Tuple[Node, List[Node]]] = [
        (start_node, children_left)
    ]

    while stack:

        node, children_left = stack[-1]

        if draw_queue is not None:
            draw_queue.push(node, config_constants.NODE_COLOR)

        node.unset_wall(update_screen=False)

        if node is board.end_node:
            node.flag = BLACK
            stack.pop()

            continue

        node.flag = GRAY

        # No children -> end node traversing
        if not children_left:
            node.flag = BLACK
            stack.pop()
            continue

        # Traverse child
        while children_left:

            child = children_left.pop()

            if child.flag == WHITE and child.is_wall():

                # Shuffle children
                child_children = get_children(child)

                stack.append((child, child_children))

                break

    # board.end_node.unset_wall(update_screen=False)


def _node_children_dfs(board: NodeBoard, node: Node) -> List[Node]:
    children: List[Node] = board.get_node_neighbours(node, lambda child: child.is_wall())
    # children: List[Node] = board.get_node_neighbours(node)

    # Choose random children of count from interval <_CHILDREN_LOWER_BOUND, children_count>
    out = random.sample(children, random.randint(min(_CHILDREN_LOWER_BOUND, len(children)), len(children)))

    for node in children:
        if node not in out:
            node.flag = BLACK

    return out


def _make_path_to_end(board: NodeBoard) -> None:

    get_children = \
        lambda node: random.sample((children := board.get_node_neighbours(node)), len(children))

    # get_children = lambda node: board.get_node_neighbours(node)

    children_left = get_children(board.end_node)

    # [(node, children left)]
    stack: List[Tuple[Node, List[Node]]] = [
        (board.end_node, children_left)
    ]

    while stack:

        node, children_left = stack[-1]

        # End if no children left or we found first node with no wall
        if node.flag == WHITE and not node.is_wall():
            break

        if not children_left:
            node.flag = BLACK
            stack.pop()

            continue

        node.unset_wall(update_screen=False)

        node.flag = GRAY

        # Traverse child
        while children_left:

            child = children_left.pop()

            if child.flag == WHITE:

                child_children = get_children(child)

                stack.append((child, child_children))
                break

    # Reset flags
    board.map_nodes(lambda node: node.clear_flags())