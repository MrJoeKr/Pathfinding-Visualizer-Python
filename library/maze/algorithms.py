import time
from typing import Callable, Deque, List, Optional, Set, Tuple
from library.constants.color import Color
from library.node.board import NodeBoard
from library.node.draw_queue import NodeQueue
from library.pathfinding.pathfinder import PathFinder
import random

from library.node.node import Node, DEFAULT_FLAG_VALUE
import library.constants.color as color
import library.constants.config as config

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
        board.map_nodes(lambda node: node.set_wall(update_screen=True))

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

    _stop_queue_visualizing(draw_queue)

    board.end_node.unset_wall(update_screen=True)


def _dfs_help(board: NodeBoard, start_node: Node,
              draw_queue: Optional[NodeQueue]) -> None:

    if start_node.flag != WHITE:
        return

    # Help lambda function
    # get_children = lambda node: board.get_node_neighbours(node)
    def get_children(node): return _node_children_dfs(board, node)

    children_left = get_children(start_node)

    # [(node, children left)]
    stack: List[Tuple[Node, List[Node]]] = [
        (start_node, children_left)
    ]

    while stack:

        node, children_left = stack[-1]

        if draw_queue is not None:
            draw_queue.push(node, config.NODE_COLOR)

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


def _node_children_dfs(board: NodeBoard, node: Node) -> List[Node]:
    children: List[Node] = board.get_node_neighbours(
        node, lambda child: child.is_wall())
    # children: List[Node] = board.get_node_neighbours(node)

    # Choose random children of count from interval <_CHILDREN_LOWER_BOUND, children_count>
    out = random.sample(
        children, random.randint(
            min(_CHILDREN_LOWER_BOUND, len(children)),
            len(children)))

    for node in children:
        if node not in out:
            node.flag = BLACK

    return out


def _make_path_to_end(board: NodeBoard) -> None:

    def get_children(node): return random.sample(
        (children := board.get_node_neighbours(node)), len(children))

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


def _stop_queue_visualizing(draw_queue: Optional[NodeQueue]):
    if draw_queue is None:
        return

    while not draw_queue.empty():
        # Prevent lag
        time.sleep(0.1)

    draw_queue.stop_visualizing()


def recursive_division(
        board: NodeBoard, draw_queue: Optional[NodeQueue]) -> None:

    while True:

        board.clear_walls()
        board.update_screen()

        _help_division(board, 0, board.cols - 1, 0,
                       board.rows - 1, set(), draw_queue)

        maze_finished = PathFinder(show_steps=False).start_search(board)

        board.clear_solution(update_screen=False)

        # board.start_node.unset_wall(update_screen=True)
        # board.end_node.unset_wall(update_screen=True)

        if maze_finished:
            break

        # Maze not found
        if draw_queue is not None:
            draw_queue.clear()

    board.start_node.unset_wall(update_screen=True)
    board.end_node.unset_wall(update_screen=True)

    _stop_queue_visualizing(draw_queue)


def _help_division(
        board: NodeBoard, left: int, right: int, top: int, bottom: int,
        holes: Set[Tuple[int, int]],
        draw_queue: Optional[NodeQueue]) -> None:

    width = right - left + 1
    height = bottom - top + 1

    # print(top, left, width, height)

    if width <= 2 or height <= 2:
        return

    # Add / subtract one so a new wall is not on the edge
    x = random.randint(left + 1, right - 1)

    # x is on a hole
    def x_on_hole(x): return (x, top - 1) in holes or (x, bottom + 1) in holes

    if x_on_hole(x):
        x = left + 1
        while x < right - 1 and x_on_hole(x):
            x += 1

    y = random.randint(top + 1, bottom - 1)

    # y is on a hole
    def y_on_hole(y): return (left - 1, y) in holes or (right + 1, y) in holes

    if y_on_hole(y):
        y = top + 1
        while y < bottom - 1 and y_on_hole(y):
            y += 1

    # print(f"(y, x): {(top, left)} ; height: {height} ; width: {width} ; point: {(y, x)}")

    # Chamber is too small
    if x_on_hole(x) or y_on_hole(y):
        return

    # Four walls: left, right, top, bottom
    walls: List[List[Node]] = _draw_walls(
        board, x, y, left, right, top, bottom, draw_queue)

    no_holes = random.randrange(4)

    # Make holes
    for i, wall in enumerate(walls):
        if i == no_holes:
            continue

        node = random.choice(wall)
        node.unset_wall()

        holes.add((node.x, node.y))

        if draw_queue is not None:
            draw_queue.push(node, config.NODE_COLOR)

    # Top-left
    _help_division(board, left, x - 1, top, y - 1, holes, draw_queue)
    # Top-right
    _help_division(board, x + 1, right, top, y - 1, holes, draw_queue)
    # Bottom-right
    _help_division(board, x + 1, right, y + 1, bottom, holes, draw_queue)
    # Bottom-left
    _help_division(board, left, x - 1, y + 1, bottom, holes, draw_queue)


def _draw_walls(
        board: NodeBoard, x: int, y: int, left: int, right: int, top: int, bottom: int, draw_queue: Optional[NodeQueue]) -> List[List[Node]]:

    # Four walls: left, right, top, bottom
    walls: List[List[Node]] = [[] for _ in range(4)]

    # print(f"(y, x): {(top, left)} ; height: {height} ; width: {width} ; point: {(y, x)}")

    # Draw walls
    for x_wall in range(left, right + 1):
        # print(y, x_wall)
        node = board.get_node(y, x_wall)
        node.set_wall(update_screen=False)

        # Don't add intersection
        if x_wall < x:
            walls[0].append(node)
        elif x_wall > x:
            walls[1].append(node)

        if draw_queue is not None:
            draw_queue.push(node, config.WALL_COLOR)

    for y_wall in range(top, bottom + 1):
        node = board.get_node(y_wall, x)
        node.set_wall(update_screen=False)

        if y_wall < y:
            walls[2].append(node)
        elif y_wall > y:
            walls[3].append(node)

        if draw_queue is not None:
            draw_queue.push(node, config.WALL_COLOR)

    return walls
