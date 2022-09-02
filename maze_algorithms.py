from typing import Callable, List, Tuple
from node_board_object import NodeBoard
import random

from node_object import Node, DEFAULT_FLAG_VALUE

MazeFunction = Callable[[NodeBoard], None]


# For DFS
_IS_WALL_ODD = 2
WHITE = DEFAULT_FLAG_VALUE
GRAY = 1
BLACK = 2

# Probably won't be working
def randomized_dfs(board: NodeBoard) -> None:

    # Set all nodes to walls
    board.map_nodes(lambda node: node.set_wall(update_screen=True))

    # Help lambda function
    get_children = lambda node: board.get_node_neighbours(node)

    children_left = get_children(board.start_node)
    random.shuffle(children_left)

    # [(node, children left)]
    stack: List[Tuple[Node, List[Node]]] = [
        (board.start_node, children_left)
    ]

    while stack:

        node, children_left = stack[-1]

        node.unset_wall(update_screen=True)

        if node is board.end_node:
            node.flag = BLACK
            stack.pop()

            # break

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
                random.shuffle(child_children)

                stack.append((child, child_children))
                break

    # Reset flags
    board.map_nodes(lambda node: node.clear_flags())
    board.start_node.draw_start_node()
    board.end_node.draw_end_node()


def _coin_flip(true_val: int, max_val: int) -> bool:
    return random.randrange(max_val) <= true_val - 1